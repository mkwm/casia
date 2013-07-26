# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ServicePolicy.is_trusted'
        db.add_column(u'server_servicepolicy', 'is_trusted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ServicePolicy.is_trusted'
        db.delete_column(u'server_servicepolicy', 'is_trusted')


    models = {
        u'server.servicepolicy': {
            'Meta': {'object_name': 'ServicePolicy'},
            'allow_proxy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_single_login': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_single_logout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_trusted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'netloc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'scheme': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
    }

    complete_apps = ['server']