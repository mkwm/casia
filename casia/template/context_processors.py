# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.sites.models import get_current_site

from casia.template import MenuRegistryDictProxy, menu as menu_dict


def site(request):
    return {'site': get_current_site(request)}


def menu(request):
    _menu_dict = MenuRegistryDictProxy(menu_dict, request)
    return {'menu': _menu_dict}