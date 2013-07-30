# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


from datetime import timedelta
import os

from django.contrib.messages import constants as message

import casia

# Default Casia settings. Override these with settings in the module
# pointed-to by the DJANGO_SETTINGS_MODULE environment variable.

TIME_ZONE = 'UTC'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'casia.urls'

WSGI_APPLICATION = 'casia.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli',
    'django.contrib.admin',
    'south',
    'casia.locale',
    'casia.server',
    'casia.assets.bootstrap',
    'casia.assets.font_awesome',
    'casia.assets.html5shiv',
    'casia.assets.jquery',
    'casia.webapp',
)

CONSUMABLE_LIFETIME = timedelta(minutes=5)

MESSAGE_TAGS = {
    message.INFO: 'alert-info',
    message.SUCCESS: 'alert-success',
    message.WARNING: '',
    message.ERROR: 'alert-error',
}

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'index'

POLICY_NETLOC_COMPONENTS = 5
POLICY_PATH_COMPONENTS = 5

USER_MODEL_PROTECTED_FIELDS = ('id', 'password', 'pk')
GRAPPELLI_ADMIN_TITLE = 'Casia'

LOCALE_PATHS = [os.path.join(os.path.dirname(casia.__file__), 'locale')]
