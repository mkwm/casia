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
    url(r'^login$',
        'casia.webapp.views.login',
        name='login'),
    url(r'^logout$',
        'casia.webapp.views.logout',
        name='logout'),
    url(r'^password_change/$',
        'django.contrib.auth.views.password_change',
        name='password_change'),
    url(r'^password_change/done/$',
        'django.contrib.auth.views.password_change_done',
        name='password_change_done'),
)
