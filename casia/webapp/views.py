# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    login as django_login, logout_then_login as django_logout_then_login,
    password_change as django_password_change,
    password_change_done as django_password_change_done
)
from django.contrib.sites.models import get_current_site
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse

# Monkey patch authentication and password change forms
import casia.auth.forms

@login_required
def index(request):
    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': 'Logged in'
    }
    return TemplateResponse(request, 'webapp/index.html', context)

def login(request):
    if request.user.is_authenticated():
        print dir(request.user)
        return redirect('index')
    context = {
        'title': 'Log in'
    }
    return django_login(request, template_name='webapp/login.html',
                        extra_context=context)

def logout(request):
    if request.user.is_authenticated():
        messages.success(request, 'You have been logged out successfully')
    else:
        messages.error(request, 'You were not logged in')
    return django_logout_then_login(request)

@login_required
def password_change(request):
    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': 'Password change'
    }
    post_change_redirect = reverse('password_change_done')
    return django_password_change(request,
        template_name='webapp/password_change.html', extra_context=context,
        post_change_redirect=post_change_redirect)

@login_required
def password_change_done(request):
    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': 'Password changed'
    }
    return django_password_change_done(request,
        template_name='webapp/password_change_done.html', extra_context=context)
