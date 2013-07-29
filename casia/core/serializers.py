# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


from xml.etree.ElementTree import Element

from django.template.defaultfilters import unordered_list
from django.utils.html import escape

from casia.core.utils import get_subclasses


class ModelFieldSerializer(object):
    @classmethod
    def to_html(cls, obj, attr):
        return escape('%s' % getattr(obj, attr))

    @classmethod
    def to_xml(cls, obj, attr):
        e = Element('cas:' + attr, attrib={'type': 'string'})
        e.text = '%s' % getattr(obj, attr)
        return [e]


class BooleanFieldSerializer(ModelFieldSerializer):
    TRUE = 'true'
    FALSE = 'false'

    @classmethod
    def to_html(cls, obj, attr):
        return cls.TRUE if getattr(obj, attr) else cls.FALSE

    @classmethod
    def to_xml(cls, obj, attr):
        e = Element('cas:' + attr, attrib={'type': 'boolean'})
        e.text = 'true' if getattr(obj, attr) else 'false'
        return [e]


class DateTimeFieldSerializer(ModelFieldSerializer):
    @classmethod
    def to_html(cls, obj, attr):
        return escape(getattr(obj, attr))

    @classmethod
    def to_xml(cls, obj, attr):
        e = Element('cas:' + attr, attrib={'type': 'dateTime'})
        e.text = getattr(obj, attr).isoformat()
        return [e]


class RelatedFieldSerializer(ModelFieldSerializer):
    @classmethod
    def to_html(cls, obj, attr):
        return '<ul>%s</ul>' % unordered_list(getattr(obj, attr).all(), escape)

    @classmethod
    def to_xml(cls, obj, attr):
        elements = []
        for i in getattr(obj, attr).all():
            e = Element('cas:' + attr, attrib={'type': 'string'})
            e.text = '%s' % i
            elements.append(e)
        return elements
