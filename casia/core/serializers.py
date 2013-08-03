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
from django.utils.translation import ugettext_lazy as _

from casia.core.utils import get_subclasses, get_field_value


class ModelFieldSerializer(object):
    @classmethod
    def to_html(cls, obj, field):
        return escape('%s' % get_field_value(field, obj))

    @classmethod
    def to_xml(cls, obj, field):
        e = Element('cas:' + field, attrib={'type': 'string'})
        e.text = '%s' % get_field_value(field, obj)
        return [e]


class BooleanFieldSerializer(ModelFieldSerializer):
    TRUE = _('true')
    FALSE = _('false')

    @classmethod
    def to_html(cls, obj, field):
        return cls.TRUE if get_field_value(field, obj) else cls.FALSE

    @classmethod
    def to_xml(cls, obj, field):
        e = Element('cas:' + field, attrib={'type': 'boolean'})
        e.text = 'true' if get_field_value(field, obj) else 'false'
        return [e]


class DateTimeFieldSerializer(ModelFieldSerializer):
    @classmethod
    def to_html(cls, obj, field):
        return escape(get_field_value(field, obj))

    @classmethod
    def to_xml(cls, obj, field):
        e = Element('cas:' + field, attrib={'type': 'dateTime'})
        e.text = get_field_value(field, obj).isoformat()
        return [e]


class RelatedFieldSerializer(ModelFieldSerializer):
    @classmethod
    def to_html(cls, obj, field):
        return '<ul>%s</ul>' % unordered_list(get_field_value(field, obj).all(),
                                              escape)

    @classmethod
    def to_xml(cls, obj, field):
        elements = []
        for i in get_field_value(field, obj).all():
            e = Element('cas:' + field, attrib={'type': 'string'})
            e.text = '%s' % i
            elements.append(e)
        return elements
