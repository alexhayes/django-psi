# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column(u'psi_ruleresult', 'pageInsight_id', 'page_insight_id')

        db.rename_column(u'psi_pageinsight', 'responseCode', 'response_code')
        db.rename_column(u'psi_pageinsight', 'otherResponseBytes', 'other_response_bytes')
        db.rename_column(u'psi_pageinsight', 'numberResources', 'number_resources')
        db.rename_column(u'psi_pageinsight', 'numberCssResources', 'number_css_resources')
        db.rename_column(u'psi_pageinsight', 'totalRequestBytes', 'total_request_bytes')
        db.rename_column(u'psi_pageinsight', 'cssResponseBytes', 'css_response_bytes')
        db.rename_column(u'psi_pageinsight', 'javascriptResponseBytes', 'javascript_response_bytes')
        db.rename_column(u'psi_pageinsight', 'imageResponseBytes', 'image_response_bytes')
        db.rename_column(u'psi_pageinsight', 'numberHosts', 'number_hosts')
        db.rename_column(u'psi_pageinsight', 'numberStaticResources', 'number_static_resources')
        db.rename_column(u'psi_pageinsight', 'htmlResponseBytes', 'html_response_bytes')
        db.rename_column(u'psi_pageinsight', 'created_date', 'created')
        db.rename_column(u'psi_pageinsight', 'numberJsResources', 'number_js_resources')

        db.rename_column(u'psi_screenshot', 'pageInsight_id', 'page_insight_id')


    def backwards(self, orm):
        db.rename_column(u'psi_ruleresult', 'page_insight_id', 'pageInsight_id')

        db.rename_column(u'psi_pageinsight', 'response_code', 'responseCode')
        db.rename_column(u'psi_pageinsight', 'other_response_bytes', 'otherResponseBytes')
        db.rename_column(u'psi_pageinsight', 'number_resources', 'numberResources')
        db.rename_column(u'psi_pageinsight', 'number_css_resources', 'numberCssResources')
        db.rename_column(u'psi_pageinsight', 'total_request_bytes', 'totalRequestBytes')
        db.rename_column(u'psi_pageinsight', 'css_response_bytes', 'cssResponseBytes')
        db.rename_column(u'psi_pageinsight', 'javascript_response_bytes', 'javascriptResponseBytes')
        db.rename_column(u'psi_pageinsight', 'image_response_bytes', 'imageResponseBytes')
        db.rename_column(u'psi_pageinsight', 'number_hosts', 'numberHosts')
        db.rename_column(u'psi_pageinsight', 'number_static_resources', 'numberStaticResources')
        db.rename_column(u'psi_pageinsight', 'html_response_bytes', 'htmlResponseBytes')
        db.rename_column(u'psi_pageinsight', 'created', 'created_date')
        db.rename_column(u'psi_pageinsight', 'number_js_resources', 'numberJsResources')

        db.rename_column(u'psi_screenshot', 'page_insight_id', 'pageInsight_id')


    models = {
        u'psi.pageinsight': {
            'Meta': {'object_name': 'PageInsight'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'css_response_bytes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'html_response_bytes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_response_bytes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'javascript_response_bytes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'json': ('django.db.models.fields.TextField', [], {}),
            'number_css_resources': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number_hosts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number_js_resources': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number_resources': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number_static_resources': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'other_response_bytes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'response_code': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'strategy': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'total_request_bytes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'psi.ruleresult': {
            'Meta': {'object_name': 'RuleResult'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impact': ('django.db.models.fields.FloatField', [], {}),
            'page_insight': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['psi.PageInsight']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'psi.screenshot': {
            'Meta': {'object_name': 'Screenshot'},
            'data': ('django.db.models.fields.TextField', [], {}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'page_insight': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['psi.PageInsight']"}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['psi']