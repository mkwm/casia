# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


from django.contrib.auth.forms import (AuthenticationForm
                                       as DjangoAuthenticationForm)


class AuthenticationForm(DjangoAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = (
            self.fields['username'].label)
        self.fields['password'].widget.attrs['placeholder'] = (
            self.fields['password'].label)
        if self.fields['username'].required:
            self.fields['username'].widget.attrs['required'] = 'required'
        if self.fields['password'].required:
            self.fields['password'].widget.attrs['required'] = 'required'


class ReauthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(ReauthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = 'readonly'
