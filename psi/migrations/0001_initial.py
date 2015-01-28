# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import psi.models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageInsight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=191, verbose_name='URL', db_index=True)),
                ('strategy', models.CharField(db_index=True, max_length=50, verbose_name='Strategy', choices=[(b'desktop', b'Desktop'), (b'mobile', b'Mobile')])),
                ('locale', models.CharField(default=b'en_US', max_length=16, verbose_name='Locale')),
                ('status', models.CharField(db_index=True, max_length=32, verbose_name='Status', choices=[(b'pending', b'Pending'), (b'consuming', b'Consuming'), (b'consumed', b'Consumed'), (b'populated', b'Populated'), (b'error', b'Error')])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated', auto_now_add=True)),
                ('response_code', models.IntegerField(default=0, verbose_name='Response Code')),
                ('title', models.CharField(max_length=255, verbose_name='Page Title')),
                ('score', models.IntegerField(default=0, verbose_name='Score')),
                ('number_resources', models.IntegerField(default=0, verbose_name='Number of Resources')),
                ('number_hosts', models.IntegerField(default=0, verbose_name='Number of Hosts')),
                ('total_request_bytes', models.IntegerField(default=0, verbose_name='Total Request Bytes')),
                ('number_static_resources', models.IntegerField(default=0, verbose_name='Number of Static Resources')),
                ('html_response_bytes', models.IntegerField(default=0, verbose_name='HTML Response Bytes')),
                ('css_response_bytes', models.IntegerField(default=0, verbose_name='CSS Response Bytes')),
                ('image_response_bytes', models.IntegerField(default=0, verbose_name='Image Response Bytes')),
                ('javascript_response_bytes', models.IntegerField(default=0, verbose_name='Javascript Response Bytes')),
                ('other_response_bytes', models.IntegerField(default=0, verbose_name='Other Response Bytes')),
                ('number_js_resources', models.IntegerField(default=0, verbose_name='Number of JS Resources')),
                ('number_css_resources', models.IntegerField(default=0, verbose_name='Number of CSS Resources')),
                ('json', jsonfield.fields.JSONField(verbose_name='JSON Response')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RuleResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Page Title')),
                ('impact', models.FloatField(verbose_name='Impact')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('page_insight', models.ForeignKey(related_name='rule_results', to='psi.PageInsight')),
            ],
            options={
                'verbose_name_plural': 'Rule Results',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('width', models.IntegerField(verbose_name='Width')),
                ('height', models.IntegerField(verbose_name='Height')),
                ('mime_type', models.CharField(max_length=32, verbose_name='Mime Type')),
                ('image', models.ImageField(upload_to=psi.models.screenshot_upload_to, max_length=255, verbose_name='Image')),
                ('page_insight', models.OneToOneField(related_name='screenshot', to='psi.PageInsight')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
