# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServicePolicy'
        db.create_table(u'server_servicepolicy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('scheme', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('netloc', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('priority', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'server', ['ServicePolicy'])

        # Adding field 'ServiceTicket.policy'
        db.add_column(u'server_serviceticket', 'policy',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['server.ServicePolicy']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ServicePolicy'
        db.delete_table(u'server_servicepolicy')

        # Deleting field 'ServiceTicket.policy'
        db.delete_column(u'server_serviceticket', 'policy_id')


    models = {
        u'server.servicepolicy': {
            'Meta': {'object_name': 'ServicePolicy'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'netloc': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'scheme': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'server.serviceticket': {
            'Meta': {'object_name': 'ServiceTicket'},
            'policy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.ServicePolicy']"}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
       },
    }

    complete_apps = ['server']