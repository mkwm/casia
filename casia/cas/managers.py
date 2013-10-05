# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from urlparse import urlparse

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.timezone import now

from casia.cas.exceptions import InvalidService, InvalidTicket
from casia.cas.utils import get_url_netloc_patterns, get_url_path_patterns

class ConsumableManager(models.Manager):
    def get_query_set(self):
        return (super(ConsumableManager, self).get_query_set()
                .filter(consumed_at=None)
                .filter(created_at__gte=now() - settings.CONSUMABLE_LIFETIME))

    def get_and_consume(self, *args, **kwargs):
        obj = super(ConsumableManager, self).get(*args, **kwargs)
        obj.consumed_at = now()
        obj.save()
        return obj

class ServiceTicketManager(ConsumableManager):
    def validate(self, service, ticket):
        try:
            st = self.get_and_consume(ticket=ticket)
        except self.model.DoesNotExist:
            raise InvalidTicket("Ticket '%s' not recognized" % ticket)

        if st.url != service:
            raise InvalidService("Ticket '%s' does not match supplied service "
                                 "- the original service was '%s' and the "
                                 "supplied service was '%s'" %
                                 (st, st.url, service))

        return st

class ServiceManager(models.Manager):
    def get_by_url(self, url):
        # urlparse returns named tuple
        # However, we need to edit it. Therefore we cast it to list.
        # [0] = scheme, [1] = netloc, [2] = path, [4] = query
        url = list(urlparse(url))

        filters = Q(scheme__exact=url[0])

        if not url[4]:
            url[4] = '/'

        values = ['']
        if url[4]:
            values.append(url[2] + '?' + url[4])
        values += get_url_path_patterns(url)
        path_filter = Q(netloc__exact=url[1]) & Q(path__in=values)

        values = ['']
        values += get_url_netloc_patterns(url)
        netloc_filter = Q(netloc__in=values) & Q(path__exact='')

        filters = filters & (path_filter | netloc_filter)

        return self.filter(filters).order_by('-priority')[:1].get()
