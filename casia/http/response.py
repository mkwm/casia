# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from xml.etree.ElementTree import tostring

from django.http.response import HttpResponse

class XMLResponse(HttpResponse):
    def __init__(self, obj):
        content = tostring(obj)
        super(XMLResponse, self).__init__(content,
                                          content_type='application/xhtml+xml')
