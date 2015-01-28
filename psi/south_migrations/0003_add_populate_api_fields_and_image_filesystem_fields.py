# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PageInsight.locale'
        db.add_column(u'psi_pageinsight', 'locale',
                      self.gf('django.db.models.fields.CharField')(default='en_US', max_length=16),
                      keep_default=False)

        # Adding field 'PageInsight.status'
        db.add_column(u'psi_pageinsight', 'status',
                      self.gf('django.db.models.fields.CharField')(default='populated', max_length=32, db_index=True),
                      keep_default=False)

        # Adding field 'PageInsight.updated'
        db.add_column(u'psi_pageinsight', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, default=datetime.datetime(2014, 12, 2, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'PageInsight.created'
        db.alter_column(u'psi_pageinsight', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'PageInsight.url'
        db.alter_column(u'psi_pageinsight', 'url', self.gf('django.db.models.fields.URLField')(max_length=191))
        # Adding index on 'PageInsight', fields ['url']
        db.create_index(u'psi_pageinsight', ['url'])

        # Adding index on 'PageInsight', fields ['strategy']
        db.create_index(u'psi_pageinsight', ['strategy'])


        # Changing field 'PageInsight.json'
        db.alter_column(u'psi_pageinsight', 'json', self.gf('jsonfield.fields.JSONField')())
        # Deleting field 'Screenshot.data'
        db.delete_column(u'psi_screenshot', 'data')

        # Adding field 'Screenshot.image'
        db.add_column(u'psi_screenshot', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=255),
                      keep_default=False)


        # Changing field 'Screenshot.page_insight'
        db.alter_column(u'psi_screenshot', 'page_insight_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['psi.PageInsight']))
        # Adding unique constraint on 'Screenshot', fields ['page_insight']
        db.create_unique(u'psi_screenshot', ['page_insight_id'])


        # Changing field 'Screenshot.mime_type'
        db.alter_column(u'psi_screenshot', 'mime_type', self.gf('django.db.models.fields.CharField')(max_length=32))

    def backwards(self, orm):
        # Removing unique constraint on 'Screenshot', fields ['page_insight']
        db.delete_unique(u'psi_screenshot', ['page_insight_id'])

        # Removing index on 'PageInsight', fields ['strategy']
        db.delete_index(u'psi_pageinsight', ['strategy'])

        # Removing index on 'PageInsight', fields ['url']
        db.delete_index(u'psi_pageinsight', ['url'])

        # Deleting field 'PageInsight.locale'
        db.delete_column(u'psi_pageinsight', 'locale')

        # Deleting field 'PageInsight.status'
        db.delete_column(u'psi_pageinsight', 'status')

        # Deleting field 'PageInsight.updated'
        db.delete_column(u'psi_pageinsight', 'updated')


        # Changing field 'PageInsight.created'
        db.alter_column(u'psi_pageinsight', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'PageInsight.url'
        db.alter_column(u'psi_pageinsight', 'url', self.gf('django.db.models.fields.URLField')(max_length=200))

        # Changing field 'PageInsight.json'
        db.alter_column(u'psi_pageinsight', 'json', self.gf('django.db.models.fields.TextField')())
        # Adding field 'Screenshot.data'
        db.add_column(u'psi_screenshot', 'data',
                      self.gf('django.db.models.fields.TextField')(default=None),
                      keep_default=False)

        # Deleting field 'Screenshot.image'
        db.delete_column(u'psi_screenshot', 'image')


        # Changing field 'Screenshot.page_insight'
        db.alter_column(u'psi_screenshot', 'page_insight_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['psi.PageInsight']))

        # Changing field 'Screenshot.mime_type'
        db.alter_column(u'psi_screenshot', 'mime_type', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        u'psi.pageinsight': {
            'Meta': {'object_name': 'PageInsight'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'css_response_bytes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'html_response_bytes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_response_bytes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'javascript_response_bytes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'json': ('jsonfield.fields.JSONField', [], {}),
            'locale': ('django.db.models.fields.CharField', [], {'default': "'en_US'", 'max_length': '16'}),
            'number_css_resources': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number_hosts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number_js_resources': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number_resources': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number_static_resources': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'other_response_bytes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'response_code': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'strategy': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'total_request_bytes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '191', 'db_index': 'True'})
        },
        u'psi.ruleresult': {
            'Meta': {'object_name': 'RuleResult'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impact': ('django.db.models.fields.FloatField', [], {}),
            'page_insight': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rule_results'", 'to': u"orm['psi.PageInsight']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'psi.screenshot': {
            'Meta': {'object_name': 'Screenshot'},
            'height': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'page_insight': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'screenshot'", 'unique': 'True', 'to': u"orm['psi.PageInsight']"}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['psi']