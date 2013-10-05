# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.utils.crypto import get_random_string

from casia.cas.exceptions import InvalidRequest

def generate_ticket(prefix, length):
    return prefix + '-' + get_random_string(length)

def validate_ticket(request):
    from casia.cas.models import ServiceTicket

    service = request.GET.get('service')
    ticket = request.GET.get('ticket')

    if not service or not ticket:
        raise InvalidRequest("'service' and 'ticket' parameters are both "
                             "required.")

    return ServiceTicket.consumable.validate(service, ticket)
