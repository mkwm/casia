# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.conf import settings
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ServiceTicket.user'
        db.add_column(u'server_serviceticket', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm[settings.AUTH_USER_MODEL]),
                      keep_default=False)

        # Adding field 'ServiceTicket.session'
        db.add_column(u'server_serviceticket', 'session',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sessions.Session']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ServiceTicket.user'
        db.delete_column(u'server_serviceticket', 'user_id')

        # Deleting field 'ServiceTicket.session'
        db.delete_column(u'server_serviceticket', 'session_id')


    models = {
        settings.AUTH_USER_MODEL: {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        },
        u'server.serviceticket': {
            'Meta': {'object_name': 'ServiceTicket'},
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sessions.Session']"}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s']" % settings.AUTH_USER_MODEL})
        },
        u'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        }
    }

    complete_apps = ['server']
