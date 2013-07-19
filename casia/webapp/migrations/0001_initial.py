# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.conf import settings
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TicketRequest'
        db.create_table(u'webapp_ticketrequest', (
            ('id', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[settings.AUTH_USER_MODEL], null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.TextField')()),
            ('renewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'webapp', ['TicketRequest'])


    def backwards(self, orm):
        # Deleting model 'TicketRequest'
        db.delete_table(u'webapp_ticketrequest')


    models = {
        settings.AUTH_USER_MODEL: {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        },
        u'webapp.ticketrequest': {
            'Meta': {'object_name': 'TicketRequest'},
            'id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True'}),
            'renewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s']" % settings.AUTH_USER_MODEL, 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['webapp']