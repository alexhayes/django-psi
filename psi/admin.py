from django.contrib import admin
from psi.models import PageInsight, RuleResult, Screenshot


class RuleResultsAdmin(admin.ModelAdmin):
    list_display = ('title', 'impact', 'page_insight')
    raw_id_fields = ('page_insight',)


class ScreenshotAdmin(admin.ModelAdmin):
    raw_id_fields = ('page_insight',)
    list_display = ('page_insight', 'width', 'height', 'image')


class PageInsightAdmin(admin.ModelAdmin):
    list_display = ('url', 'strategy', 'locale', 'status', 'title', 'score', 'response_code',
                    'number_resources', 'image_response_bytes', 'html_response_bytes',
                    'javascript_response_bytes')

admin.site.register(PageInsight, PageInsightAdmin)
admin.site.register(RuleResult, RuleResultsAdmin)
admin.site.register(Screenshot, ScreenshotAdmin)