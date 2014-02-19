# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServicePermission'
        db.create_table(u'core_servicepermission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('codename', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['ServicePermission'])

        # Adding unique constraint on 'ServicePermission', fields ['content_type', 'codename']
        db.create_unique(u'core_servicepermission', ['content_type_id', 'codename'])

        # Adding model 'Service'
        db.create_table(u'core_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_trusted', self.gf('django.db.models.fields.BooleanField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'core', ['Service'])

        # Adding M2M table for field service_permissions on 'Service'
        m2m_table_name = db.shorten_name(u'core_service_service_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('service', models.ForeignKey(orm[u'core.service'], null=False)),
            ('servicepermission', models.ForeignKey(orm[u'core.servicepermission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['service_id', 'servicepermission_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ServicePermission', fields ['content_type', 'codename']
        db.delete_unique(u'core_servicepermission', ['content_type_id', 'codename'])

        # Deleting model 'ServicePermission'
        db.delete_table(u'core_servicepermission')

        # Deleting model 'Service'
        db.delete_table(u'core_service')

        # Removing M2M table for field service_permissions on 'Service'
        db.delete_table(db.shorten_name(u'core_service_service_permissions'))


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.service': {
            'Meta': {'object_name': 'Service'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'is_trusted': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'service_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'service_set'", 'blank': 'True', 'to': u"orm['core.ServicePermission']"})
        },
        u'core.servicepermission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'ServicePermission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['core']