# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit

AuthenticationForm.helper = FormHelper()
AuthenticationForm.helper.form_class = 'form-horizontal'
AuthenticationForm.helper.label_class = 'hide'
AuthenticationForm.helper.field_class = 'col-sm-offset-4 col-sm-4'
AuthenticationForm.helper.html5_required = True
AuthenticationForm.helper.layout = Layout(
    PrependedText('username', '<span class="icon-fixed-width icon-user"></span>'),
    PrependedText('password', '<span class="icon-fixed-width icon-key"></span>'),
    Div(
        Submit('sign-in', 'Sign in', css_class='btn-lg'),
        css_class='text-center'
    ),
)
