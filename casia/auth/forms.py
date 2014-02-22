# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.forms import (AuthenticationForm as DjangoAuthenticationForm,
    PasswordChangeForm as DjangoPasswordChangeForm)
from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit


class AuthenticationForm(DjangoAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'sr-only'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            PrependedText('username', '<span class="fa fa-fw fa-user"></span>',
                          placeholder=self.fields['username'].label),
            PrependedText('password', '<span class="fa fa-fw fa-key"></span>',
                          placeholder=self.fields['password'].label),
            Submit('log-in', _('Log in'), css_class='btn-lg btn-block'),
        )


class PasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            'old_password',
            'new_password1',
            'new_password2',
            Div(
                Submit('change-password', _('Change password'), css_class='btn-lg'),
                css_class='col-sm-offset-2 col-sm-8',
            ),
        )


class ReauthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        if ('data' in kwargs and
            kwargs['data']['username'] != kwargs['initial']['username']):
            kwargs['data'] = kwargs.get('data', {}).copy()
            kwargs['data']['username'] = kwargs['initial']['username']
        super(ReauthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = 'readonly'

    def clean_username(self):
        return self.initial['username']


class ReauthenticationFormWrapper(object):
    def __init__(self, user):
        self.username = user.get_username()

    def __call__(self, *args, **kwargs):
        kwargs['initial'] = kwargs.get('initial', {})
        kwargs['initial']['username'] = self.username
        return ReauthenticationForm(*args, **kwargs)
