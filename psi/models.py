try:
    from io import BytesIO
except ImportError:
    BytesIO = None
    import StringIO
from base64 import b64decode
import collections
import json
import mimetypes

from apiclient.discovery import build
from apiclient.errors import HttpError
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield.fields import JSONField
from psi.settings import PsiAppConf


mimetypes.init()


class PageInsight(models.Model):
    STRATEGY_DESKTOP = 'desktop'
    STRATEGY_MOBILE = 'mobile'
    STRATEGY_CHOICES = (
        (STRATEGY_DESKTOP, 'Desktop'),
        (STRATEGY_MOBILE, 'Mobile'),
    )

    STATUS_PENDING = 'pending'
    STATUS_CONSUMING = 'consuming'
    STATUS_CONSUMED = 'consumed'
    STATUS_POPULATED = 'populated'
    STATUS_ERROR = 'error'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONSUMING, 'Consuming'),
        (STATUS_CONSUMED, 'Consumed'),
        (STATUS_POPULATED, 'Populated'),
        (STATUS_ERROR, 'Error'),
    )

    # Mandatory fields
    url = models.URLField(_('URL'), max_length=191, db_index=True)
    strategy = models.CharField(_('Strategy'), max_length=50, choices=STRATEGY_CHOICES, db_index=True)
    locale = models.CharField(_('Locale'), max_length=16, default='en_US')
    # Managed fields
    status = models.CharField(_('Status'), max_length=32, choices=STATUS_CHOICES, db_index=True)
    created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Date Updated'), auto_now_add=True, auto_now=True)
    # Populated fields
    response_code = models.IntegerField(_('Response Code'), default=0)
    title = models.CharField(_('Page Title'), max_length=255)
    score = models.IntegerField(_('Score'), default=0)
    number_resources = models.IntegerField(_('Number of Resources'), default=0)
    number_hosts = models.IntegerField(_('Number of Hosts'), default=0)
    total_request_bytes = models.IntegerField(_('Total Request Bytes'), default=0)
    number_static_resources = models.IntegerField(_('Number of Static Resources'), default=0)
    html_response_bytes = models.IntegerField(_('HTML Response Bytes'), default=0)
    css_response_bytes = models.IntegerField(_('CSS Response Bytes'), default=0)
    image_response_bytes = models.IntegerField(_('Image Response Bytes'), default=0)
    javascript_response_bytes = models.IntegerField(_('Javascript Response Bytes'), default=0)
    other_response_bytes = models.IntegerField(_('Other Response Bytes'), default=0)
    number_js_resources = models.IntegerField(_('Number of JS Resources'), default=0)
    number_css_resources = models.IntegerField(_('Number of CSS Resources'), default=0)
    json = JSONField(_('JSON Response'), load_kwargs={'object_pairs_hook': collections.OrderedDict})

    def __unicode__(self):
        return _('%s (%s)') % (self.url, self.created.date())

    def set_consuming(self):
        self.status = self.STATUS_CONSUMING
        self.save()

    def set_consumed(self):
        self.status = self.STATUS_CONSUMED
        self.save()

    def set_populated(self):
        self.status = self.STATUS_POPULATED
        self.save()

    def set_error(self):
        self.status = self.STATUS_ERROR
        self.save()

    def consume(self):
        """
        Retrieve the Google Page Insight data from the API.
        """
        try:
            self.set_consuming()

            # Ensure we have a valid url
            URLValidator(self.url)

            # Build api service
            service = build(serviceName='pagespeedonline', 
                            version='v1', 
                            developerKey=getattr(settings, 'GOOGLE_API_KEY', None))

            # Make request
            data = service.pagespeedapi().runpagespeed(url=self.url,
                                                       strategy=self.strategy,
                                                       locale=self.locale,
                                                       screenshot=settings.PSI_SCREENSHOT).execute()
            # Save json before we continue
            self.json = data
            self.set_consumed()
            return data

        except HttpError as e:
            self.json = json.loads(e.content)
            self.set_error()
            raise
        except Exception:
            self.set_error()
            raise

    def populate(self, data=None):
        """
        Populate this insight from the API.
        """
        if data is None:
            data = self.consume()

        self.response_code = data["responseCode"]
        self.title = data["title"]
        self.score = data["score"]
        self.url = data['id']
        self.number_resources = data['pageStats'].get("numberResources")
        self.number_hosts = data['pageStats']["numberHosts"]
        self.total_request_bytes = int(data['pageStats']["totalRequestBytes"])
        self.number_static_resources = data['pageStats'].get("numberStaticResources", 0)
        self.html_response_bytes = int(data['pageStats']["htmlResponseBytes"])
        self.css_response_bytes = int(data['pageStats'].get("cssResponseBytes", 0))
        self.image_response_bytes = int(data['pageStats'].get("imageResponseBytes", 0))
        self.javascript_response_bytes = int(data['pageStats'].get("javascriptResponseBytes", 0))
        self.other_response_bytes = int(data['pageStats'].get("otherResponseBytes", 0))
        self.number_js_resources = int(data['pageStats'].get("numberJsResources", 0))
        self.number_css_resources = int(data['pageStats'].get("numberCssResources", 0))
        self.save()

        if settings.PSI_SCREENSHOT and data.get('screenshot'):
            screenshot = Screenshot()
            screenshot.page_insight = self
            screenshot.width = data.get('screenshot').get('width')
            screenshot.height = data.get('screenshot').get('height')
            screenshot.mime_type = data.get('screenshot').get('mime_type')

            # Write file to memory
            if BytesIO:
                f = BytesIO(b64decode(data.get('screenshot').get('data').replace('_', '/').replace('-', '+')))
            else:
                f = StringIO.StringIO(b64decode(data.get('screenshot').get('data').replace('_', '/').replace('-', '+')))
            # Determine the file extension
            ext = mimetypes.guess_extension(screenshot.mime_type)
            # Save to disk
            screenshot.image.save('screenshot%s' % ext, ContentFile(f.read()))

            screenshot.save()

        # Save the rules
        for key, values in data.get('formattedResults').get('ruleResults').items():
            ruleResult = RuleResult()
            ruleResult.page_insight = self
            ruleResult.title = values.get('localizedRuleName')
            ruleResult.impact = values.get('ruleImpact')
            ruleResult.description = values.get('urlBlocks')[0]['header']['format']
            ruleResult.save()

        self.set_populated()


class RuleResult(models.Model):
    page_insight = models.ForeignKey(PageInsight, related_name='rule_results')
    title = models.CharField(_('Page Title'), max_length=255)
    impact = models.FloatField(_('Impact'))
    description = models.TextField(_('Description'), blank=True, null=True)

    class Meta:
        verbose_name_plural = _('Rule Results')

    def __unicode__(self):
        return self.title


def screenshot_upload_to(instance, filename):
    """
    Return the upload path for a screenshot.
    """
    return '%s/%s/%s' % (settings.PSI_MEDIA_PATH, instance.page_insight.pk, filename)


class Screenshot(models.Model):
    page_insight = models.OneToOneField(PageInsight, related_name='screenshot')
    width = models.IntegerField(_('Width'))
    height = models.IntegerField(_('Height'))
    mime_type = models.CharField(_('Mime Type'), max_length=32)
    image = models.ImageField(_('Image'), max_length=255, upload_to=screenshot_upload_to)

    def __unicode__(self):
        return _('Screenshot for %s') % self.page_insight
