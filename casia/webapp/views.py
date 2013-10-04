# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.views import login as django_login
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from casia.auth.forms import AuthenticationForm

def index(request):
    return TemplateResponse(request, 'webapp/index.html')

def login(request):
    if request.user.is_authenticated():
        return redirect('index')
    return django_login(request, template_name='webapp/login.html',
                        authentication_form=AuthenticationForm)
