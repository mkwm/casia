# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, include, url

cas_urlpatterns = patterns('casia.cas.views',
    url(r'^validate$', 'validate', name='validate'),
    url(r'^serviceValidate$', 'service_validate', name='service_validate'),
    url(r'^login$', 'login', name='login'),
    url(r'^issue$', 'issue', name='issue'),
    url(r'^logout$', 'logout', name='logout'),
    url(r'^proxyValidate$', 'service_validate', {'require_st': False}, name='proxy_validate'),
    url(r'^proxy$', 'proxy', name='proxy'),
)

urlpatterns = patterns('',
    url(r'^cas/', include(cas_urlpatterns, 'cas')),
)