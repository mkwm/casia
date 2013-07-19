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
from django.contrib import messages
from django.contrib.auth import (login as auth_login, logout as auth_logout,
                                 REDIRECT_FIELD_NAME)
from django.shortcuts import redirect, resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.debug import sensitive_post_parameters

from casia.webapp.forms import AuthenticationForm, ReauthenticationForm


@sensitive_post_parameters()
def relogin(request, template_name='webapp/relogin.html',
            redirect_field_name=REDIRECT_FIELD_NAME,
            reauthentication_form=ReauthenticationForm):
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = reauthentication_form(data=request.POST,
                                    initial={'username': request.user})
        if form.is_valid():
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            auth_login(request, form.get_user())

            return redirect(redirect_to)
    else:
        form = reauthentication_form(request,
                                     initial={'username': request.user})
    context = {
        'form': form,
        redirect_field_name: redirect_to,
    }
    return TemplateResponse(request, template_name, context)


@sensitive_post_parameters()
def login(request):
    if not request.user.is_authenticated():
        from django.contrib.auth.views import login
        return login(request, template_name='webapp/login.html',
                          authentication_form=AuthenticationForm)
    else:
        return relogin(request)


def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)
        messages.success(request, 'You have been logged out successfully.')
    else:
        messages.error(request, 'You have to be logged in to log out. '
                       'Please log in to log out.')
    return redirect('login')


def cas_login(request):
    raise NotImplementedError()
