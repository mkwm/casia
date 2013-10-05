# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import models
from django.utils.timezone import now
from django_extensions.db.fields import UUIDField

from casia.cas.managers import (ConsumableManager, ProxyGrantingTicketManager,
                                ServiceTicketManager, ServiceManager)
from casia.cas.utils import generate_ticket

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
    service = models.ForeignKey('Service')
    renewed = models.BooleanField()
    pgt = models.ForeignKey('ProxyGrantingTicket', blank=True, null=True,
                            related_name='+')

    def save(self, *args, **kwargs):
        if not self.pgt:
            self.prefix = 'ST'
        else:
            self.prefix = 'PT'
        super(ServiceTicket, self).save(*args, **kwargs)

class TicketRequest(models.Model):
    id = UUIDField(auto=True, primary_key=True)
    url = models.TextField()
    service = models.ForeignKey('Service')
    renewed = models.BooleanField()
    session = models.ForeignKey(Session, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def __unicode__(self):
        return self.url

class Service(models.Model):
    objects = ServiceManager()

    scheme = models.CharField(max_length=16)
    netloc = models.CharField(max_length=255, blank=True)
    path = models.CharField(max_length=255, blank=True)
    priority = models.PositiveIntegerField(blank=True)
    is_active = models.BooleanField()
    is_trusted = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.priority:
            priority = 0
            if self.netloc:
                priority += 10
            if self.path:
                priority += 20
            self.priority = priority
        super(Service, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.scheme + '://' + self.netloc + self.path

    def has_perm(self, perm, obj=None):
        return (self.is_active and self.is_trusted)

class ProxyGrantingTicket(AbstractTicket):
    objects = ProxyGrantingTicketManager()

    prefix = 'PGT'

    iou = models.CharField(max_length=255, unique=True)
    url = models.TextField()
    st = models.OneToOneField('ServiceTicket')
