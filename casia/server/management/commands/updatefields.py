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
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from casia.server.models import FieldPermission


class Command(BaseCommand):
    help = 'Updates user profile fields (and properties) list'

    def handle(self, *args, **options):
        db_fields = set([f.field for f in FieldPermission.objects.all()])

        model = get_user_model()

        field_names = [f.name for f in model._meta.fields]
        property_names = [name for name in dir(model)
                          if isinstance(getattr(model, name), property)]
        code_fields = (set(field_names + property_names) -
                       set(settings.USER_MODEL_PROTECTED_FIELDS))

        to_create = code_fields - db_fields
        print 'Fields to create in database:'
        for i in to_create:
            print '-', i
        bulk_create = [FieldPermission(field=field,
                                       position=0) for field in to_create]
        FieldPermission.objects.bulk_create(bulk_create)

        print

        to_delete = db_fields - code_fields
        print 'Fields to delete from database:'
        for i in to_delete:
            print '-', i
        FieldPermission.objects.filter(field__in=to_delete).delete()

        print
