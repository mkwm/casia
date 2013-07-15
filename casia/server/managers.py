# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


from django.conf import settings
from django.db import models
from django.utils.timezone import now


class ConsumableManager(models.Manager):
    def get_query_set(self):
        return (super(ConsumableManager, self).get_query_set()
                .filter(validated_at=None)
                .filter(issued_at__gte=now() - settings.CONSUMABLE_LIFETIME))

    def get_and_consume(self, *args, **kwargs):
        obj = super(ConsumableManager, self).get(*args, **kwargs)
        obj.consumed_at = now()
        obj.save()
        return obj
