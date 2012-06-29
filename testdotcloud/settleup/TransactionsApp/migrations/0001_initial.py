# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'users'
        db.create_table('TransactionsApp_users', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('outstanding', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('TransactionsApp', ['users'])

        # Adding model 'transactions'
        db.create_table('TransactionsApp_transactions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('user_paid', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions_set', to=orm['TransactionsApp.users'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('perpersoncost', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('TransactionsApp', ['transactions'])

        # Adding M2M table for field users_involved on 'transactions'
        db.create_table('TransactionsApp_transactions_users_involved', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('transactions', models.ForeignKey(orm['TransactionsApp.transactions'], null=False)),
            ('users', models.ForeignKey(orm['TransactionsApp.users'], null=False))
        ))
        db.create_unique('TransactionsApp_transactions_users_involved', ['transactions_id', 'users_id'])

        # Adding model 'quotes'
        db.create_table('TransactionsApp_quotes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('q', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('shown', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('TransactionsApp', ['quotes'])


    def backwards(self, orm):
        # Deleting model 'users'
        db.delete_table('TransactionsApp_users')

        # Deleting model 'transactions'
        db.delete_table('TransactionsApp_transactions')

        # Removing M2M table for field users_involved on 'transactions'
        db.delete_table('TransactionsApp_transactions_users_involved')

        # Deleting model 'quotes'
        db.delete_table('TransactionsApp_quotes')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'outstanding': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['TransactionsApp']