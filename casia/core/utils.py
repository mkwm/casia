# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


from django.contrib.admin.util import lookup_field


def get_subclasses(cls):
    subclasses = []

    for scls in cls.__subclasses__():
        subclasses.append(scls)
        subclasses.extend(get_subclasses(scls))

    return subclasses


def get_class_by_dotted_name(name):
    try:
        module, obj = name.rsplit('.', 1)
        return getattr(__import__(module, fromlist=[obj]), obj)
    except:
        raise ImportError


def get_field_value(field, obj):
    f, attr, value = lookup_field(field, obj)
    return value

