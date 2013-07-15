# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.conf import settings
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ServiceTicket.url'
        db.add_column(u'server_serviceticket', 'url',
                      self.gf('django.db.models.fields.TextField')(default='http://localhost/'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ServiceTicket.url'
        db.delete_column(u'server_serviceticket', 'url')


    models = {
        settings.AUTH_USER_MODEL: {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        },
        u'server.serviceticket': {
            'Meta': {'object_name': 'ServiceTicket'},
            'consumed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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