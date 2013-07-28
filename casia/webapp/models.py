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

from uuidfield import UUIDField

from casia.server.models import ServicePolicy


class TicketRequest(models.Model):
    id = UUIDField(auto=True, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    session = models.ForeignKey(Session, blank=True, null=True)
    url = models.TextField()
    policy = models.ForeignKey(ServicePolicy)
    renewed = models.BooleanField()

    def __unicode__(self):
        return self.url
