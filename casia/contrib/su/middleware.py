# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django

# This module is based on oioioi.su from OIOIOI by SIO2 Project
# https://github.com/sio2project/oioioi

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