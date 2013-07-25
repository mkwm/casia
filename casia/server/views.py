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

from django.http import HttpResponse

from casia.server.exceptions import Error
from casia.server.http import XMLResponse
from casia.server.models import ProxyGrantingTicket
from casia.server.utils import issue_proxy_ticket, validate_ticket


# CAS 1.0 validation
def validate(request):
    st = None
    try:
        st = validate_ticket(request)
    except Error:
        pass
    return HttpResponse('yes\n%s\n' % st.user if st else 'no\n\n')


# CAS 2.0 validation
def service_validate(request, require_st=True):
    response = Element('cas:serviceResponse',
                       attrib={'xmlns:cas': 'http://www.yale.edu/tp/cas'})
    try:
        st = validate_ticket(request, require_st)
        auth_success = SubElement(response, 'cas:authenticationSuccess')
        user = SubElement(auth_success, 'cas:user')
        user.text = st.user.get_username()

        if st.policy.allow_proxy:
            pgt = ProxyGrantingTicket.objects.create_for_request(request)
            if pgt:
                pgt_iou = SubElement(auth_success, 'cas:proxyGrantingTicket')
                pgt_iou.text = pgt.iou

            if st.pgt:
                proxies = SubElement(auth_success, 'cas:proxies')
                current = st
                while current.pgt:
                    proxy = SubElement(proxies, 'cas:proxy')
                    proxy.text = current.pgt.url
                    current = current.pgt.st
    except Error as ex:
        auth_failure = SubElement(response, 'cas:authenticationFailure',
                                  attrib={'code': ex.code})
        auth_failure.text = ex.msg
    return XMLResponse(response)


def proxy(request):
    response = Element('cas:serviceResponse',
                       attrib={'xmlns:cas': 'http://www.yale.edu/tp/cas'})
    try:
        proxy_success = SubElement(response, 'cas:proxySuccess')
        pt = issue_proxy_ticket(request)
        proxy_ticket = SubElement(proxy_success, 'cas:proxyTicket')
        proxy_ticket.text = pt.ticket
    except Error as ex:
        proxy_failure = SubElement(response, 'cas:proxyFailure',
                                   attrib={'code': ex.code})
        proxy_failure.text = ex.msg
    return XMLResponse(response)
