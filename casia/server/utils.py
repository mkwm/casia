# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


from urlparse import urlparse, urlunparse

from django.conf import settings
from django.http import HttpResponseRedirect, QueryDict
from django.utils.crypto import get_random_string

from casia.server.exceptions import InvalidRequest


def generate_ticket(prefix, length):
    return prefix + '-' + get_random_string(length)


def validate_ticket(request):
    from casia.server.models import ServiceTicket

    service = request.GET.get('service')
    ticket = request.GET.get('ticket')
    renew = 'renew' in request.GET

    if not service or not ticket:
        raise InvalidRequest("'service' and 'ticket' parameters are both "
                             "required.")

    return ServiceTicket.consumable.validate(service, ticket, renew)


def update_url(url, url_vars):
    url_parts = list(urlparse(url))
    qs = QueryDict(url_parts[4], mutable=True)
    qs.update(url_vars)
    url_parts[4] = qs.urlencode(safe='/')
    return urlunparse(url_parts)


def issue_ticket(ticket_request):
    from casia.server.models import ServiceTicket

    st = ServiceTicket(user=ticket_request.user,
                       session=ticket_request.session,
                       url=ticket_request.url,
                       renewed=ticket_request.renewed,
                       policy=ticket_request.policy)
    st.save()

    target = update_url(ticket_request.url, {'ticket': st.ticket})

    # TODO: Remove validated ticket request from database
    return HttpResponseRedirect(target)


def get_url_netloc_patterns(url, count=settings.POLICY_NETLOC_COMPONENTS):
    patterns = []
    pattern = ''
    netloc = url[1].rsplit('.', count)
    for component in reversed(netloc[1:]):
        pattern = component + '.' + pattern
        patterns.append(pattern[:-1])
    return patterns


def get_url_path_patterns(url, count=settings.POLICY_PATH_COMPONENTS):
    patterns = []
    pattern = ''
    path = url[2].split('/', count)
    for component in path[:-1]:
        pattern += component + '/'
        patterns.append(pattern)
    if url[2].endswith('/'):
        pattern += path[-1]
        patterns.append(pattern)
    else:
        tmp = path[-1].rsplit('/', 1)
        if len(tmp) > 1:
            pattern += tmp[0] + '/'
            patterns.append(pattern)
            pattern += tmp[1]
            patterns.append(pattern)
        else:
            pattern += tmp[0]
            patterns.append(pattern)
    return patterns
