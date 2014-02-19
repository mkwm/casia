# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin

from casia.cas.models import (ProxyGrantingTicket, ServiceURL, ServiceTicket,
                              TicketRequest)


class ProxyGrantingTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'iou', 'st', 'url')


class ServiceURLAdmin(admin.ModelAdmin):
    list_display = ('service', '__unicode__')


class ServiceTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'url', 'is_consumable')


class TicketRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'session', 'user')


admin.site.register(ProxyGrantingTicket, ProxyGrantingTicketAdmin)
admin.site.register(ServiceURL, ServiceURLAdmin)
admin.site.register(ServiceTicket, ServiceTicketAdmin)
admin.site.register(TicketRequest, TicketRequestAdmin)
