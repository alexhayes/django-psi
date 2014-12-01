from __future__ import absolute_import

import json
import os
import shutil

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from psi.models import PageInsight


MEDIA_DIR = os.path.join(os.path.dirname(__file__), 'testapp', 'media')


class PageInsightTestCase(TestCase):

    def setUp(self):
        # Clean media directory
        p = os.path.join(settings.MEDIA_ROOT, settings.PSI_MEDIA_PATH)
        if os.path.exists(p):
            shutil.rmtree(p)

        # Clean database
        PageInsight.objects.all().delete()

    def test_save_json(self):
        page_insight = PageInsight.objects.create(url='http://example.com',
                                                  strategy=PageInsight.STRATEGY_DESKTOP)
        with open(os.path.join(os.path.dirname(__file__), 'data', 'examplecom-desktop.json')) as f:
            raw_json = f.read()
            data = json.loads(raw_json)
            page_insight.json = data
            page_insight.save()

        self.assertEqual(page_insight.json.get('id'), 'http://example.com/')

    def test_populate(self):
        page_insight = PageInsight.objects.create(url='http://example.com',
                                                  strategy=PageInsight.STRATEGY_DESKTOP)
        with open(os.path.join(os.path.dirname(__file__), 'data', 'examplecom-desktop.json')) as f:
            raw_json = f.read()
            data = json.loads(raw_json)
            page_insight.populate(data)

        self.assertEqual(page_insight.url, 'http://example.com/')
        self.assertEqual(page_insight.strategy, 'desktop')
        self.assertEqual(page_insight.locale, 'en_US')
        self.assertEqual(page_insight.status, PageInsight.STATUS_POPULATED)
        self.assertIsNotNone(page_insight.created)
        self.assertIsNotNone(page_insight.updated)
        self.assertEqual(page_insight.response_code, 200)
        self.assertEqual(page_insight.title, 'Example Domain')
        self.assertEqual(page_insight.score, 99)
        self.assertEqual(page_insight.number_resources, 1)
        self.assertEqual(page_insight.number_hosts, 1)
        self.assertEqual(page_insight.total_request_bytes, 33)
        self.assertEqual(page_insight.number_static_resources, 15)
        self.assertEqual(page_insight.html_response_bytes, 1571)
        self.assertEqual(page_insight.css_response_bytes, 160783)
        self.assertEqual(page_insight.image_response_bytes, 38054)
        self.assertEqual(page_insight.javascript_response_bytes, 627690)
        self.assertEqual(page_insight.other_response_bytes, 1573)
        self.assertEqual(page_insight.number_js_resources, 4)
        self.assertEqual(page_insight.number_css_resources, 1)

        self.assertEqual(page_insight.screenshot.width, 320)
        self.assertEqual(page_insight.screenshot.height, 240)
        self.assertEqual(page_insight.screenshot.mime_type, 'image/jpeg')
        # Until http://bugs.python.org/issue4963 is resolved we can't really determine the full extension
        self.assertIn('screenshot.jp', page_insight.screenshot.image.name)
