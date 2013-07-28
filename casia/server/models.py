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
import requests
from uuid import uuid4
from xml.etree.ElementTree import Element, SubElement, tostring

from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.utils.timezone import now

from casia.core.fields import SubclassField
from casia.core.serializers import ModelFieldSerializer
from casia.core.utils import get_class_by_dotted_name
from casia.server.managers import (ConsumableManager,
                                   ProxyGrantingTicketManager,
                                   ServiceTicketManager, ServicePolicyManager)
from casia.server.utils import generate_ticket


# Monkey patch which makes it possible to distinguish sessions in admin panel
Session.__unicode__ = lambda self: self.session_key


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
    policy = models.ForeignKey('ServicePolicy')
    renewed = models.BooleanField()
    pgt = models.ForeignKey('ProxyGrantingTicket', blank=True, null=True,
                            related_name='+')

    def save(self, *args, **kwargs):
        if not self.pgt:
            self.prefix = 'ST'
        else:
            self.prefix = 'PT'
        super(ServiceTicket, self).save(*args, **kwargs)


class ServicePolicy(models.Model):
    objects = ServicePolicyManager()

    name = models.CharField(max_length=255, blank=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    scheme = models.CharField(max_length=16)
    netloc = models.CharField(max_length=255, blank=True)
    path = models.CharField(max_length=255, blank=True)
    priority = models.PositiveIntegerField(blank=True)
    is_active = models.BooleanField()
    is_trusted = models.BooleanField()
    allow_proxy = models.BooleanField()
    allow_single_login = models.BooleanField()
    allow_single_logout = models.BooleanField()
    field_permissions = models.ManyToManyField('FieldPermission', blank=True)

    def save(self, *args, **kwargs):
        if not self.priority:
            priority = 0
            if self.name:
                priority += 40
            if self.netloc:
                priority += 10
            if self.path:
                priority += 20
            self.priority = priority
        super(ServicePolicy, self).save(*args, **kwargs)


class ProxyGrantingTicket(AbstractTicket):
    objects = ProxyGrantingTicketManager()

    prefix = 'PGT'

    iou = models.CharField(max_length=255, unique=True)
    url = models.TextField()
    st = models.OneToOneField('ServiceTicket')


class FieldPermission(models.Model):
    field = models.CharField(max_length=255, primary_key=True)
    serializer_name = SubclassField(superclass=ModelFieldSerializer,
                                    blank=True, null=True)

    @property
    def serializer(self):
        if self.serializer_name:
            return get_class_by_dotted_name(self.serializer_name)
        else:
            return ModelFieldSerializer

    def __unicode__(self):
        return self.field


@receiver(post_delete, sender=ServiceTicket)
def _st_post_delete(sender, instance, **kwargs):
    if instance.policy.allow_single_logout:
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
                requests.post(instance.url,
                              data={'logoutRequest': tostring(request)})
            except:
                pass
