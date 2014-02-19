# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from collections import defaultdict
from sys import maxint

from casia.utils.datastructures import OrderedRegistry

from django.utils.html import escape
from django.utils.safestring import mark_safe


class MenuItem(object):
    def __init__(self, name, text, url_generator, condition, attrs):
        self.name = name
        self.text = text
        self.url_generator = url_generator
        self.condition = condition
        self.attrs = attrs


class MenuRegistry(object):
    def __init__(self, text=None, condition=None):
        self.text = text
        if condition is None:
            condition = lambda request: True
        self.condition = condition
        self._registry = OrderedRegistry()

    def register(self, name, text, url_generator, order=maxint, condition=None, attrs=None):
        if condition is None:
            condition = lambda _: True

        if attrs is None:
            attrs = {}

        menu_item = MenuItem(name, text, url_generator, condition, attrs)
        self._registry.register(menu_item, order)

    def register_decorator(self, text, url_generator, order=maxint, attrs=None):
        def decorator(view_func):
            name = view_func.__name__
            suffix_to_remove = '_view'
            if name.endswith(suffix_to_remove):
                name = name[:-len(suffix_to_remove)]
            if hasattr(view_func, 'condition'):
                condition = view_func.condition
            else:
                condition = lambda request: True
            self.register(name, text, url_generator, order, condition, attrs)
            return view_func
        return decorator

    def unregister(self, name):
        for item in self._registry:
            if item.name == name:
                self._registry.unregister(item)
                break

    def template_context(self, request):
        if not self.condition(request):
            return []

        context_items = []
        for item in self._registry:
            if item.condition(request):
                attrs_str = ' '.join(['%s="%s"' % (escape(k), escape(v)) for (k, v) in item.attrs.items()])
                attrs_str = mark_safe(attrs_str)
                context_items.append(dict(url=item.url_generator(request), text=item.text, attrs=attrs_str))
        return context_items


class MenuRegistryDictProxy(object):
    def __init__(self, obj, context):
        self._obj = obj
        self._context = context

    def __getitem__(self, item):
        return self._obj[item].template_context(self._context)


menu = defaultdict(MenuRegistry)