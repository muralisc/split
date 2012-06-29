# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'users.name'
        db.alter_column('TransactionsApp_users', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

    def backwards(self, orm):

        # Changing field 'users.name'
        db.alter_column('TransactionsApp_users', 'name', self.gf('django.db.models.fields.CharField')(max_length=10))

    models = {
        'TransactionsApp.quotes': {
            'Meta': {'object_name': 'quotes'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'q': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'shown': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'TransactionsApp.transactions': {
            'Meta': {'object_name': 'transactions'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'perpersoncost': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user_paid': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions_set'", 'to': "orm['TransactionsApp.users']"}),
            'users_involved': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'transactions_set1'", 'symmetrical': 'False', 'to': "orm['TransactionsApp.users']"})
        },
        'TransactionsApp.users': {
            'Meta': {'object_name': 'users'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'outstanding': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['TransactionsApp']