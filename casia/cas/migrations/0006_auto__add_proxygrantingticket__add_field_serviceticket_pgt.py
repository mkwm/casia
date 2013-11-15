# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.conf import settings
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProxyGrantingTicket'
        db.create_table(u'cas_proxygrantingticket', (
            ('ticket', self.gf('django.db.models.fields.CharField')(max_length=256, primary_key=True)),
            ('iou', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('url', self.gf('django.db.models.fields.TextField')()),
            ('st', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cas.ServiceTicket'], unique=True)),
        ))
        db.send_create_signal(u'cas', ['ProxyGrantingTicket'])

        # Adding field 'ServiceTicket.pgt'
        db.add_column(u'cas_serviceticket', 'pgt',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['cas.ProxyGrantingTicket']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ProxyGrantingTicket'
        db.delete_table(u'cas_proxygrantingticket')

        # Deleting field 'ServiceTicket.pgt'
        db.delete_column(u'cas_serviceticket', 'pgt_id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        settings.AUTH_USER_MODEL: {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
        },
        u'cas.proxygrantingticket': {
            'Meta': {'object_name': 'ProxyGrantingTicket'},
            'iou': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'st': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['cas.ServiceTicket']", 'unique': 'True'}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        u'cas.service': {
            'Meta': {'object_name': 'Service'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_trusted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'netloc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'scheme': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'cas.serviceticket': {
            'Meta': {'object_name': 'ServiceTicket'},
            'consumed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'pgt': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['cas.ProxyGrantingTicket']"}),
            'renewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cas.Service']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sessions.Session']"}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s']" % settings.AUTH_USER_MODEL})
        },
        u'cas.ticketrequest': {
            'Meta': {'object_name': 'TicketRequest'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'renewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cas.Service']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sessions.Session']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s']" % settings.AUTH_USER_MODEL, 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        }
    }

    complete_apps = ['cas']
