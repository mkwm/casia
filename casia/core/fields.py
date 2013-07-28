# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


from south.modelsinspector import add_introspection_rules

from django.db import models

from casia.core.utils import get_subclasses


class SubclassField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, superclass, *args, **kwargs):
        self.superclass = superclass
        kwargs['max_length'] = 255
        kwargs['choices'] = self._choices()
        models.CharField.__init__(self, *args, **kwargs)

    def _choices(self):
        subclasses = get_subclasses(self.superclass)
        for subclass in subclasses:
            label = '%s.%s' % (subclass.__module__, subclass.__name__)
            yield label, label

    def validate(self, value, model_instance):
        pass

add_introspection_rules([
    (
        [SubclassField],
        [],
        {
            "superclass": ["superclass", {}],
        },
    ),
], ["^casia\.core\.fields\.SubclassField"])
