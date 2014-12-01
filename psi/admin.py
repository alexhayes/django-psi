from django.contrib import admin
from psi.models import PageInsight, RuleResult, Screenshot


class RuleResultsAdmin(admin.ModelAdmin):
    list_display = ('title', 'impact', 'page_insight')
    raw_id_fields = ('page_insight',)


class ScreenshotAdmin(admin.ModelAdmin):
    raw_id_fields = ('page_insight',)


class PageInsightAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'strategy', 'score', 'responseCode',
                    'numberResources', 'imageResponseBytes', 'htmlResponseBytes',
                    'javascriptResponseBytes')

admin.site.register(PageInsight, PageInsightAdmin)
admin.site.register(RuleResult, RuleResultsAdmin)
admin.site.register(Screenshot, ScreenshotAdmin)