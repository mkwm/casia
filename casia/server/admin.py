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

from casia.server.models import (FieldPermission, ServiceTicket, ServicePolicy,
                                 ProxyGrantingTicket)


class ServiceTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'created_at', 'is_consumable')


class ServicePolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'scheme', 'netloc', 'path', 'priority',
                    'is_active')
    filter_horizontal = ('field_permissions', )


class ProxyGrantingTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'iou', 'url', 'st')


admin.site.register(FieldPermission)
admin.site.register(ServiceTicket, ServiceTicketAdmin)
admin.site.register(ServicePolicy, ServicePolicyAdmin)
admin.site.register(ProxyGrantingTicket, ProxyGrantingTicketAdmin)
