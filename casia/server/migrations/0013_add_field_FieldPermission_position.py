# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from casia.core.serializers import ModelFieldSerializer


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FieldPermission.position'
        db.add_column(u'server_fieldpermission', 'position',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FieldPermission.position'
        db.delete_column(u'server_fieldpermission', 'position')


    models = {
        u'server.fieldpermission': {
            'Meta': {'object_name': 'FieldPermission'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'serializer_name': ('casia.core.fields.SubclassField', [], {'max_length': '255', 'null': 'True', 'superclass': 'ModelFieldSerializer', 'blank': 'True'})
        },
    }

    complete_apps = ['server']