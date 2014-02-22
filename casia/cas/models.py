# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from urlparse import urlparse
from uuid import uuid4
from xml.etree.ElementTree import Element, SubElement, tostring

from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.utils.timezone import now

from casia.cas.managers import (ConsumableManager, ProxyGrantingTicketManager,
                                ServiceTicketManager, ServiceURLManager)
from casia.cas.tasks import logout as logout_task
from casia.cas.utils import generate_ticket
from casia.core.models import Service, LoginHistoryEntry


class AbstractTicket(models.Model):
    length = 32
    ticket = models.CharField(primary_key=True, max_length=256, editable=False)

    def save(self):
        if not self.ticket:
            self.ticket = generate_ticket(self.prefix, self.length)
        super(AbstractTicket, self).save()

    def __unicode__(self):
        return self.ticket

    class Meta:
        abstract = True


class AbstractConsumable(models.Model):
    objects = models.Manager()
    consumable = ConsumableManager()

    created_at = models.DateTimeField(auto_now_add=True)
    consumed_at = models.DateTimeField(blank=True, null=True)

    def is_consumable(self):
        return (self.consumed_at is None and
                self.created_at >= now() - settings.CONSUMABLE_LIFETIME)
    is_consumable.boolean = True

    class Meta:
        abstract = True


class ServiceTicket(AbstractTicket, AbstractConsumable):
    objects = models.Manager()
    consumable = ServiceTicketManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    session = models.ForeignKey(Session)
    # IE is not able to handle GET requests to URLs longer than 2083 bytes
    # Apache is known to have troubles with URLs longer than 4000 bytes
    # nginx supports 8192 bytes in URLs by default
    # For that reasons, its safer to use TextField insted of CharField
    url = models.TextField()
    service = models.ForeignKey(Service)
    renewed = models.BooleanField()
    pgt = models.ForeignKey('ProxyGrantingTicket', blank=True, null=True,
                            related_name='+')

    def save(self, *args, **kwargs):
        if not self.pgt:
            self.prefix = 'ST'
        else:
            self.prefix = 'PT'
        super(ServiceTicket, self).save(*args, **kwargs)


class ServiceURL(models.Model):
    objects = ServiceURLManager()

    service = models.ForeignKey(Service)
    scheme = models.CharField(max_length=16)
    netloc = models.CharField(max_length=255, blank=True)
    path = models.CharField(max_length=255, blank=True)
    priority = models.PositiveIntegerField(blank=True)

    def save(self, *args, **kwargs):
        if not self.priority:
            priority = 0
            if self.netloc:
                priority += 10
            if self.path:
                priority += 20
            self.priority = priority
        super(ServiceURL, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.scheme + '://' + self.netloc + self.path


class ProxyGrantingTicket(AbstractTicket):
    objects = ProxyGrantingTicketManager()

    prefix = 'PGT'

    iou = models.CharField(max_length=255, unique=True)
    url = models.TextField()
    st = models.OneToOneField('ServiceTicket')


@receiver(post_delete, sender=ServiceTicket)
def st_post_delete(sender, instance, **kwargs):
    urlparts = urlparse(instance.url)
    if urlparts.scheme in ('http', 'https'):
        time = now()
        instant = time.isoformat()
        if time.microsecond:
            instant = instant[:23] + instant[26:]
        if instant.endswith('+00:00'):
            instant = instant[:-6] + 'Z'
        request = Element('samlp:LogoutRequest',
                          attrib={'ID': str(uuid4()),
                                  'IssueInstant': instant,
                                  'Version': '2.0'})
        name_id = SubElement(request, 'saml:NameID')
        name_id.text = instance.user.get_username()
        session_index = SubElement(request, 'samlp:SessionIndex')
        session_index.text = instance.ticket
        try:
            logout_task.delay(instance.url, tostring(request))
        except:
            pass


class SharedSecret(models.Model):
    service = models.OneToOneField(Service, primary_key=True, related_name='cas_shared_secret')
    secret = models.CharField(max_length=255)


class CASLoginHistoryEntry(LoginHistoryEntry):
    renewed = models.BooleanField(default=False)
    used_at = models.DateTimeField(blank=True, null=True)