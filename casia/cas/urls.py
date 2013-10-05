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
    url(r'^validate$', 'casia.cas.views.validate', name='cas_validate'),
    url(r'^serviceValidate$', 'casia.cas.views.service_validate', name='cas_service_validate'),
    url(r'^login$', 'casia.cas.views.login', name='cas_login'),
    url(r'^issue/(?P<ticket_request_id>.*?)$', 'casia.cas.views.issue', name='cas_issue'),
)
