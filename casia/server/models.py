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
from django.db import models
from django.contrib.sessions.models import Session

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


class ServiceTicket(AbstractTicket):
    prefix = 'ST'
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    session = models.ForeignKey(Session)
