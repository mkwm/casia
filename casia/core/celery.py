# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

from celery import Celery
from django.conf import settings


app = Celery('casia')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS, related_name='tasks')