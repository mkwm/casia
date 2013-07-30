# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


class ProfileGenerator(object):
    def __init__(self, user, fields):
        self.user = user
        self.fields = fields

    def items(self):
        for f in self.fields:
            try:
                key = self.user._meta.get_field_by_name(f.field)[0].verbose_name
                value = f.serializer.to_html(self.user, f.field)
                yield key, value
            except AttributeError:
                # TODO: Should it be ignored?
                pass
