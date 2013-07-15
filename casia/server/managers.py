# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


from django.conf import settings
from django.db import models
from django.utils.timezone import now

from casia.server.exceptions import InvalidService, InvalidTicket


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
    def validate(self, service, ticket, renew):
        try:
            st = self.get_and_consume(ticket=ticket)
        except self.model.DoesNotExist:
            raise InvalidTicket("Ticket '%s' not recognized." % ticket)

        if st.url != service:
            raise InvalidService("Ticket '%s' does not match supplied service"
                                 "- the original service was '%s' and the"
                                 "supplied service was '%s'." %
                                 (st, st.url, service))

        if renew and not st.renewed:
            raise InvalidTicket("Ticket '%s' does not match validation"
                                "specification - was issued from single"
                                "sign-on session, but renew was requested." %
                                ticket)

        return st
