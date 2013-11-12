# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django import forms
from django.contrib.auth import get_backends
from django.contrib.auth.models import User

from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit


def authentication_backends():
    for backend in get_backends():
        yield ("%s.%s" % (backend.__module__, backend.__class__.__name__),
                getattr(backend, 'description', backend.__class__.__name__))


class SwitchUserForm(forms.Form):
    user = forms.CharField(label="User")
    backend = forms.ChoiceField(label="Authentication backend", required=False, choices=authentication_backends())

    def __init__(self, *args, **kwargs):
        super(SwitchUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'hide'
        self.helper.field_class = 'col-sm-offset-4 col-sm-4'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            PrependedText('user', '<span class="fa fa-fw fa-user"></span>',
                          placeholder=self.fields['user'].label),
            PrependedText('backend', '<span class="fa fa-fw fa-key"></span>',
                          placeholder=self.fields['backend'].label),
            Div(
                Submit('su', 'Switch user', css_class='btn-lg'),
                css_class='text-center'
            ),
        )

    def clean_user(self):
        username = self.cleaned_data['user']
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid username.")