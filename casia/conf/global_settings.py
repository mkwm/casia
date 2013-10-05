# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

# Default Casia settings. Override these with settings in the module
# pointed-to by the DJANGO_SETTINGS_MODULE environment variable.

from datetime import timedelta

from django.contrib.messages import constants as message

TIME_ZONE = 'UTC'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'casia.conf.urls'

WSGI_APPLICATION = 'casia.core.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'south',
    'casia.auth',
    'casia.assets.bootstrap',
    'casia.assets.fontawesome',
    'casia.assets.html5shiv',
    'casia.assets.jquery',
    'casia.assets.respondjs',
    'casia.cas',
    'casia.webapp',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

MESSAGE_TAGS = {
    message.INFO: 'alert-info',
    message.SUCCESS: 'alert-success',
    message.WARNING: 'alert-warning',
    message.ERROR: 'alert-danger',
}

SITE_ID = 1

CONSUMABLE_LIFETIME = timedelta(minutes=5)
