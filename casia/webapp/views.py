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
    login as django_login, logout_then_login as django_logout_then_login
)
from django.contrib.sites.models import get_current_site
from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from casia.auth.forms import AuthenticationForm

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
        return redirect('index')
    context = {
        'title': 'Log in'
    }
    return django_login(request, template_name='webapp/login.html',
                        authentication_form=AuthenticationForm,
                        extra_context=context)

def logout(request):
    messages.success(request, 'You have been logged out successfully')
    return django_logout_then_login(request)
