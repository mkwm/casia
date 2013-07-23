# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^cas/validate$',
        'casia.server.views.validate',
        name='cas_validate'),
    url(r'^cas/serviceValidate$',
        'casia.server.views.service_validate',
        name='cas_service_validate'),
    url(r'^cas/proxyValidate$',
        'casia.server.views.service_validate',
        {'require_st': False},
        name='cas_proxyvalidate'),
)
