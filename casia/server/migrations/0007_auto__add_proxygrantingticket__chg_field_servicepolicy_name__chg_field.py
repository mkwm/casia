# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.conf import settings
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProxyGrantingTicket'
        db.create_table(u'server_proxygrantingticket', (
            ('ticket', self.gf('django.db.models.fields.CharField')(max_length=256, primary_key=True)),
            ('iou', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('url', self.gf('django.db.models.fields.TextField')()),
            ('st', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['server.ServiceTicket'], unique=True)),
        ))
        db.send_create_signal(u'server', ['ProxyGrantingTicket'])


        # Changing field 'ServicePolicy.name'
        db.alter_column(u'server_servicepolicy', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'ServicePolicy.netloc'
        db.alter_column(u'server_servicepolicy', 'netloc', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'ServicePolicy.path'
        db.alter_column(u'server_servicepolicy', 'path', self.gf('django.db.models.fields.CharField')(max_length=255))
        # Adding field 'ServiceTicket.pgt'
        db.add_column(u'server_serviceticket', 'pgt',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['server.ProxyGrantingTicket']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ProxyGrantingTicket'
        db.delete_table(u'server_proxygrantingticket')


        # Changing field 'ServicePolicy.name'
        db.alter_column(u'server_servicepolicy', 'name', self.gf('django.db.models.fields.CharField')(max_length=256))

        # Changing field 'ServicePolicy.netloc'
        db.alter_column(u'server_servicepolicy', 'netloc', self.gf('django.db.models.fields.CharField')(max_length=256))

        # Changing field 'ServicePolicy.path'
        db.alter_column(u'server_servicepolicy', 'path', self.gf('django.db.models.fields.CharField')(max_length=256))
        # Deleting field 'ServiceTicket.pgt'
        db.delete_column(u'server_serviceticket', 'pgt_id')


    models = {
        settings.AUTH_USER_MODEL: {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        },
        u'server.proxygrantingticket': {
            'Meta': {'object_name': 'ProxyGrantingTicket'},
            'iou': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'st': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['server.ServiceTicket']", 'unique': 'True'}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        u'server.servicepolicy': {
            'Meta': {'object_name': 'ServicePolicy'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'netloc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'scheme': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'server.serviceticket': {
            'Meta': {'object_name': 'ServiceTicket'},
            'consumed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'pgt': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['server.ProxyGrantingTicket']"}),
            'policy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['server.ServicePolicy']"}),
            'renewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sessions.Session']"}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s']" % settings.AUTH_USER_MODEL})
        },
        u'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        }
    }

    complete_apps = ['server']