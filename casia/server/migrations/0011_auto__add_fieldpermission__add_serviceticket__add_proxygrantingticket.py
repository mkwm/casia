# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FieldPermission'
        db.create_table(u'server_fieldpermission', (
            ('field', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
        ))
        db.send_create_signal(u'server', ['FieldPermission'])

        # Adding M2M table for field field_permissions on 'ServicePolicy'
        m2m_table_name = db.shorten_name(u'server_servicepolicy_field_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('servicepolicy', models.ForeignKey(orm[u'server.servicepolicy'], null=False)),
            ('fieldpermission', models.ForeignKey(orm[u'server.fieldpermission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['servicepolicy_id', 'fieldpermission_id'])


    def backwards(self, orm):
        # Deleting model 'FieldPermission'
        db.delete_table(u'server_fieldpermission')

        # Removing M2M table for field field_permissions on 'ServicePolicy'
        db.delete_table(db.shorten_name(u'server_servicepolicy_field_permissions'))


    models = {
        u'server.fieldpermission': {
            'Meta': {'object_name': 'FieldPermission'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        },
        u'server.servicepolicy': {
            'Meta': {'object_name': 'ServicePolicy'},
            'allow_proxy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_single_login': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_single_logout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'field_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['server.FieldPermission']", 'symmetrical': 'False', 'blank': 'True'}),
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
        u'server.serviceticket': {
            'Meta': {'object_name': 'ServiceTicket'},
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
        },
    }

    complete_apps = ['server']