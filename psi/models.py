from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone


class PageInsight(models.Model):
    url = models.URLField(_('URL'))
    response_code = models.IntegerField(_('Response Code'), default=0)
    title = models.CharField(_('Page Title'), max_length=255)
    strategy = models.CharField(_('Strategy'), max_length=50)
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
    created = models.DateTimeField(_('Date Created'), default=timezone.now)
    json = models.TextField(_('JSON Response'))

    def __unicode__(self):
        return _('%s (%s)') % (self.url, self.created.date())

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        super(PageInsight, self).save(*args, **kwargs)


class RuleResult(models.Model):
    page_insight = models.ForeignKey(PageInsight)
    title = models.CharField(_('Page Title'), max_length=255)
    impact = models.FloatField(_('Impact'))
    description = models.TextField(_('Description'), blank=True, null=True)

    class Meta:
        verbose_name_plural = _('Rule Results')

    def __unicode__(self):
        return self.title


class Screenshot(models.Model):
    page_insight = models.ForeignKey(PageInsight)
    width = models.IntegerField(_('Width'))
    height = models.IntegerField(_('Height'))
    data = models.TextField(_('Image data'))
    mime_type = models.CharField(_('Mime Type'), max_length=255, blank=False, null=False)

    def __unicode__(self):
        return _('Screenshot for %s') % self.page_insight
