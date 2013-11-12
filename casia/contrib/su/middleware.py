# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth import get_user
from django.contrib import auth

from casia.contrib.su import SU_SESSION_KEY, SU_BACKEND_SESSION_KEY


def get_user(request, user_id, backend_path):
    backend = auth.load_backend(backend_path)
    user = backend.get_user(user_id)
    user.backend = backend_path
    return user


class SwitchUserMiddleware(object):
    def process_request(self, request):
        request.real_user = request.user
        if SU_SESSION_KEY in request.session:
            request.user = get_user(request, request.session[SU_SESSION_KEY], request.session[SU_BACKEND_SESSION_KEY])