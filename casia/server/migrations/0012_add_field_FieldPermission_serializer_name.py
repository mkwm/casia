# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from casia.core.serializers import ModelFieldSerializer


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FieldPermission.serializer_name'
        db.add_column(u'server_fieldpermission', 'serializer_name',
                      self.gf('casia.core.fields.SubclassField')(max_length=255, null=True, superclass=ModelFieldSerializer, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FieldPermission.serializer_name'
        db.delete_column(u'server_fieldpermission', 'serializer_name')


    models = {
        u'server.fieldpermission': {
            'Meta': {'object_name': 'FieldPermission'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'serializer_name': ('casia.core.fields.SubclassField', [], {'max_length': '255', 'null': 'True', 'superclass': 'ModelFieldSerializer', 'blank': 'True'})
        },
    }

    complete_apps = ['server']