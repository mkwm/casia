# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServiceTicket'
        db.create_table(u'server_serviceticket', (
            ('ticket', self.gf('django.db.models.fields.CharField')(max_length=256, primary_key=True)),
        ))
        db.send_create_signal(u'server', ['ServiceTicket'])


    def backwards(self, orm):
        # Deleting model 'ServiceTicket'
        db.delete_table(u'server_serviceticket')


    models = {
        u'server.serviceticket': {
            'Meta': {'object_name': 'ServiceTicket'},
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'})
        }
    }

    complete_apps = ['server']