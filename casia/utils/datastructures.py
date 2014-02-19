# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from bisect import bisect_right
from sys import maxint


class OrderedRegistry(object):
    def __init__(self):
        self.items = []
        self.keys = []

    def register(self, value, order=maxint):
        pos = bisect_right(self.keys, order)
        self.items.insert(pos, value)
        self.keys.insert(pos, order)
        return value

    def unregister(self, value):
        pos = self.items.index(value)
        del self.items[pos]
        del self.keys[pos]

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def register_decorator(self, order=maxint):
        def decorator(func):
            self.register(func, order)
            return func
        return decorator