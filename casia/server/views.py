# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


from django.http import HttpResponse

from casia.server.exceptions import ValidationError
from casia.server.utils import validate_ticket


# CAS 1.0 validation
def validate(request):
    st = None
    try:
        st = validate_ticket(request)
    except ValidationError:
        pass
    return HttpResponse('yes\n%s\n' % st.user if st else 'no\n\n')
