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

from casia.cas.models import Service, ServiceTicket, TicketRequest

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', )

class ServiceTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'url', 'is_consumable')

class TicketRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'session', 'user')

admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceTicket, ServiceTicketAdmin)
admin.site.register(TicketRequest, TicketRequestAdmin)
