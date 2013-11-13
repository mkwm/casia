# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django

# This module is based on oioioi.su from OIOIOI by SIO2 Project
# https://github.com/sio2project/oioioi

from django.contrib.auth.models import AnonymousUser

from casia.contrib.su import SU_SESSION_KEY


def real_user(request):
    if not hasattr(request, 'real_user'):
        return {
            'real_user': getattr(request, 'user', AnonymousUser()),
            'is_under_su': False,
        }
    else:
        return {
            'real_user': request.real_user,
            'is_under_su': SU_SESSION_KEY in request.session,
        }