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
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.utils.module_loading import import_by_path


def load_backend(path):
    return import_by_path(path)()


def get_backends():
    backends = []
    for backend_path in settings.CAS_SERVICE_AUTHENTICATION_BACKENDS:
        backends.append(load_backend(backend_path))
    if not backends:
        raise ImproperlyConfigured('No CAS service authentication backends have been defined. Does CAS_SERVICE_AUTHENTICATION_BACKENDS contain anything?')
    return backends


def authenticate(**credentials):
    for backend in get_backends():
        try:
            service = backend.authenticate(**credentials)
        except TypeError:
            continue
        except PermissionDenied:
            return None
        if service is None:
            continue
        return service