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
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.base import View


class LoginView(TemplateView):
    template_name = 'webapp/login.html'


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated():
            messages.success(request, 'You have been logged out successfully.')
            auth_logout(request)
        else:
            messages.error(request, 'You have to be logged in to log out. '
                           'Please log in to log out.')
        return redirect('login')
