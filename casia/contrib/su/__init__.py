# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.db.models.signals import post_syncdb
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models as auth_models, get_user_model, views
from django.contrib.auth.models import Permission
from django.shortcuts import redirect

from casia.template import menu, MenuItem


SU_SESSION_KEY = '_su_user_id'
SU_BACKEND_SESSION_KEY = '_su_user_backend'


def add_user_permissions(sender, **kwargs):
    user_type = ContentType.objects.get_for_model(get_user_model())
    _, _ = Permission.objects.get_or_create(codename='switch_user', name='Can switch user', content_type=user_type)
post_syncdb.connect(add_user_permissions, sender=auth_models)


old_logout_then_login = views.logout_then_login
def logout_then_login(request, *args, **kwargs):
    if SU_SESSION_KEY in request.session:
        del request.session[SU_SESSION_KEY]
        del request.session[SU_BACKEND_SESSION_KEY]
        return redirect('index')
    else:
        return old_logout_then_login(request, *args, **kwargs)
views.logout_then_login = logout_then_login

menu['navbar'].append(MenuItem('su:su', 'Switch user', lambda request: request.user.has_perm('auth.switch_user')))
