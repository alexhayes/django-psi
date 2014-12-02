from optparse import make_option
from django.core.management import BaseCommand, CommandError
from django.conf import settings
from django.utils.translation import ugettext as _
from psi.models import PageInsight
from string import zfill
from django.template.defaultfilters import filesizeformat


class Command(BaseCommand):
    args = 'url'
    help = "Create PageSpeedInsights for a given URL."
    option_list = BaseCommand.option_list + (
        make_option("--strategy", "-s", action="store", dest="strategy", default="desktop", 
                    help="The strategy to use when analyzing the page. Valid values are desktop and mobile."),
        make_option("--locale", "-l", action="store", dest="locale", default="en_US",
                    help="The locale that results should be generated in. See the list of supported locales. If the specified locale is not supported, the default locale is used."),
        make_option("--quiet", "-q", action="store_true", default=False, dest="quiet",
                    help="Be quiet, don't output anything."),
        )

    def handle(self, *args, **options):
        urls = []

        if len(args) == 1:
            urls.append(args[0])
        else:
            urls = getattr(settings, 'PSI_URLS', [])
            if urls is None or len(urls) == 0:
                raise CommandError("No URLs provided. Please either pass a URL as an argument or define PSI_URLS in settings file.")

        for url in urls:
            page_insight = PageInsight.objects.create(url=url,
                                                      strategy=options.get('strategy'),
                                                      locale=options.get('locale'))
            page_insight.populate()

            if not options.get('quiet'):
                self._console_report(page_insight)

    def _console_report(self, page_insight):
        lines = []
        field_groups = (
            (None, (
                'url', 
                'strategy', 
                'score', 
                'locale', 
                'response_code', 
                'title',
                ),
            ),
            ('Weight', (
                'total_request_bytes',
                'html_response_bytes',
                'image_response_bytes',
                'javascript_response_bytes',
                'css_response_bytes',
                'other_response_bytes',
                ),
            ),
            ('Stats', (
                'number_hosts',
                'number_resources',
                'number_static_resources',
                'number_js_resources',
                'number_css_resources',
                )
            )
        )

        for title, fields in field_groups:
            if title is not None:
                lines.append('')
                lines.append('%s' % title)
                lines.append('-' * len(title))

            for field in fields:
                _field = page_insight._meta.get_field_by_name(field)[0]
                field_name = _field.verbose_name
                value = getattr(page_insight, 'get_%s_display' % field)() if _field.choices else getattr(page_insight, field)
                if 'Bytes' in field_name:
                    field_name = field_name.replace(' Bytes', ' Size')
                    value = filesizeformat(value)
                lines.append((field_name, value))

        lines.append('')
        lines.append('Rules')
        lines.append('-----')

        for result in page_insight.rule_results.all():
            lines.append((result.title, value))

        # Work out the max width
        width = max([len(line[0]) for line in lines if isinstance(line, tuple)]) + 4

        for line in lines:
            if isinstance(line, str):
                print(line)
            else:
                print('%s %s' % (('%s ' % line[0]).ljust(width, '.'), line[1]))
