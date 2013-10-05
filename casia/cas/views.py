# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from xml.etree.ElementTree import Element, SubElement

from django.http.response import HttpResponse

from casia.cas.exceptions import Error
from casia.cas.utils import validate_ticket
from casia.http.response import XMLResponse

def validate(request):
    st = None
    try:
        st = validate_ticket(request)
    except Error:
        pass
    return HttpResponse('yes\n%s\n' % st.user if st else 'no\n\n')

def service_validate(request):
    response = Element('cas:serviceResponse',
                       attrib={'xmlns:cas': 'http://www.yale.edu/tp/cas'})
    try:
        st = validate_ticket(request)
        auth_success = SubElement(response, 'cas:authenticationSuccess')
        user = SubElement(auth_success, 'cas:user')
        user.text = st.user.get_username()
    except Error as ex:
        auth_failure = SubElement(response, 'cas:authenticationFailure',
                                  attrib={'code': ex.code})
        auth_failure.text = ex.msg
    return XMLResponse(response)
