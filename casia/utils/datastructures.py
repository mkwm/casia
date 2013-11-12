# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from itertools import ifilter


class ContextDict(object):
    def __init__(self, obj, predicate, context):
        self._obj = obj
        self._predicate = predicate
        self._context = context

    def __getitem__(self, item):
        return ifilter(lambda x: self._predicate(self._context, x), self._obj[item])