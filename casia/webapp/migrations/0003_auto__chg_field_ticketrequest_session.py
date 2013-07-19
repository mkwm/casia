# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.conf import settings
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TicketRequest.session'
        db.alter_column(u'webapp_ticketrequest', 'session_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sessions.Session'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'TicketRequest.session'
        raise RuntimeError("Cannot reverse this migration. 'TicketRequest.session' and its values cannot be restored.")

    models = {
        settings.AUTH_USER_MODEL: {
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        },
        u'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        },
        u'webapp.ticketrequest': {
            'Meta': {'object_name': 'TicketRequest'},
            'id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True'}),
            'renewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sessions.Session']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s']" % settings.AUTH_USER_MODEL, 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['webapp']