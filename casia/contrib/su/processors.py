# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

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