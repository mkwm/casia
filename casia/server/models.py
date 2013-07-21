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

from casia.server.managers import (ConsumableManager, ServiceTicketManager,
                                   ServicePolicyManager)
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

    prefix = 'ST'

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    session = models.ForeignKey(Session)
    # IE is not able to handle GET requests to URLs longer than 2083 bytes
    # Apache is known to have troubles with URLs longer than 4000 bytes
    # nginx supports 8192 bytes in URLs by default
    # For that reasons, its safer to use TextField insted of CharField
    url = models.TextField()
    policy = models.ForeignKey('ServicePolicy')
    renewed = models.BooleanField()


class ServicePolicy(models.Model):
    objects = ServicePolicyManager()

    name = models.CharField(max_length=256, blank=True)
    scheme = models.CharField(max_length=16)
    netloc = models.CharField(max_length=256, blank=True)
    path = models.CharField(max_length=256, blank=True)
    priority = models.PositiveIntegerField(blank=True)
    is_active = models.BooleanField()

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
