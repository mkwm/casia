# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.http.response import HttpResponse

from casia.cas.exceptions import Error
from casia.cas.utils import validate_ticket

def validate(request):
    st = None
    try:
        st = validate_ticket(request)
    except Error:
        pass
    return HttpResponse('yes\n%s\n' % st.user if st else 'no\n\n')
