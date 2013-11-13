# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django

# This module is based on oioioi.su from OIOIOI by SIO2 Project
# https://github.com/sio2project/oioioi

from django.contrib import auth
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.decorators import permission_required
from django.contrib.sites.models import get_current_site
from django.template.response import TemplateResponse
from django.shortcuts import redirect

from casia.contrib.su.forms import SwitchUserForm
from casia.contrib.su import SU_SESSION_KEY, SU_BACKEND_SESSION_KEY


def get_user(request, user_id, backend_path):
    backend = auth.load_backend(backend_path)
    user = backend.get_user(user_id)
    user.backend = backend_path
    return user


@permission_required('auth.switch_user', raise_exception=True)
def index(request):
    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': 'Switch user'
    }

    if request.method == 'POST':
        form = SwitchUserForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            if user.is_superuser:
                raise SuspiciousOperation('Tried to switch user to account with superuser status')

            su_to_user(request, user, form.cleaned_data['backend'])

            return redirect('index')
    else:
        form = SwitchUserForm()

    context['form'] = form
    return TemplateResponse(request, 'webapp/su.html', context)


def su_to_user(request, user, backend_path=None):
    if not backend_path:
        backend_path = request.user.backend

    request.session[SU_SESSION_KEY] = user.id
    request.session[SU_BACKEND_SESSION_KEY] = backend_path

    request.real_user = request.user
    request.user = get_user(request, user.id, backend_path)