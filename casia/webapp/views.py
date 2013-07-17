# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import View

from casia.webapp.forms import AuthenticationForm, ReauthenticationForm


class LoginView(View):
    template_name = 'webapp/login.html'

    def get_form_class(self, request):
        if not request.user.is_authenticated():
            return AuthenticationForm
        else:
            return ReauthenticationForm

    def get(self, request):
        if request.user.is_authenticated():
            return render(request, 'webapp/logged_in.html')

        form_class = self.get_form_class(request)
        form = form_class(request)

        request.session.set_test_cookie()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form_class = self.get_form_class(request)
        form = form_class(data=request.POST)

        if form.is_valid():
            auth_login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return redirect('login')

        request.session.set_test_cookie()

        return render(request, self.template_name, {'form': form})

    @method_decorator(sensitive_post_parameters())
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated():
            messages.success(request, 'You have been logged out successfully.')
            auth_logout(request)
        else:
            messages.error(request, 'You have to be logged in to log out. '
                           'Please log in to log out.')
        return redirect('login')
