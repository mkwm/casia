# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from casia.template import menu as casia_menu
from casia.utils.datastructures import ContextDict


def menu(request):
    context_menu = ContextDict(casia_menu, lambda context, x: not (x.condition and not x.condition(context)), request)
    return {'menu': context_menu}