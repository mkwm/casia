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
from django.conf.urls import patterns, include, url
from django.utils.importlib import import_module

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('')

for app in settings.INSTALLED_APPS:
    try:
        if app.startswith('casia.'):
            urls_module = import_module(app + '.urls')
            urlpatterns += getattr(urls_module, 'urlpatterns')
    except ImportError:
        pass

urlpatterns.extend([
    url(r'^admin/', include(admin.site.urls)),
])