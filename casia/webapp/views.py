# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth import BACKEND_SESSION_KEY, load_backend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    login as django_login, logout_then_login as django_logout_then_login,
    password_change as django_password_change,
    password_change_done as django_password_change_done
)
from django.contrib.sites.models import get_current_site
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _

from casia.auth.forms import AuthenticationForm, ReauthenticationFormWrapper

@login_required
def index(request):
    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Logged in')
    }
    return TemplateResponse(request, 'webapp/index.html', context)

def login(request):
    if not request.user.is_authenticated():
        template_name = 'webapp/login.html'
        form = AuthenticationForm
        context = {
            'title': _('Log in')
        }
    else:
        template_name = 'webapp/relogin.html'
        form = ReauthenticationFormWrapper(user=request.user)
        context = {
            'title': _('Log in again')
        }
    return django_login(request, template_name, authentication_form=form,
                        extra_context=context)

def logout(request):
    if request.user.is_authenticated():
        messages.success(request, _('You have been logged out successfully'))
    else:
        messages.error(request, _('You were not logged in'))
    return django_logout_then_login(request)

@login_required
def password_change(request):
    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Password change')
    }
    backend_path = request.session[BACKEND_SESSION_KEY]
    backend = load_backend(backend_path)
    if hasattr(backend, 'password_change_form'):
        password_change_form = backend.password_change_form
    else:
        raise Http404
    post_change_redirect = reverse('password_change_done')
    return django_password_change(request,
        template_name='webapp/password_change.html', extra_context=context,
        password_change_form=password_change_form,
        post_change_redirect=post_change_redirect)

@login_required
def password_change_done(request):
    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Password changed')
    }
    return django_password_change_done(request,
        template_name='webapp/password_change_done.html', extra_context=context)
