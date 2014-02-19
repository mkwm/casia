# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.contenttypes.models import ContentType
from django.db import models


class ServicePermissionManager(models.Manager):
    def get_by_natural_key(self, codename, app_label, model):
        return self.get(
            codename=codename,
            content_type=ContentType.objects.get_by_natural_key(app_label,
                                                                model),
        )