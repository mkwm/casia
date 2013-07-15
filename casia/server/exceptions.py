# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


class ValidationError(Exception):
    def __str__(self):
        return self.msg


class InvalidRequest(ValidationError):
    def __init__(self, msg):
        self.code = 'INVALID_REQUEST'
        self.msg = msg


class InvalidTicket(ValidationError):
    def __init__(self, msg):
        self.code = 'INVALID_TICKET'
        self.msg = msg


class InvalidService(ValidationError):
    def __init__(self, msg):
        self.code = 'INVALID_SERVICE'
        self.msg = msg
