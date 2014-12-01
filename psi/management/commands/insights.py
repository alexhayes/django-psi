from optparse import make_option
from django.core.management import BaseCommand, CommandError
from django.conf import settings
from django.utils.translation import ugettext as _
from psi.models import PageInsight


class Command(BaseCommand):
    help = "Create PageSpeedInsights for a given URL."
    option_list = BaseCommand.option_list + (
        make_option("--url", "-u", action="store", dest="url",
                    help="The URL of the page for which the PageSpeed Insights API should generate results."),
        make_option("--strategy", "-s", action="store", dest="strategy", default="desktop", 
                    help="The strategy to use when analyzing the page. Valid values are desktop and mobile."),
        make_option("--locale", "-l", action="store", dest="locale", default="en_US",
                    help="The locale that results should be generated in. See the list of supported locales. If the specified locale is not supported, the default locale is used."),
        make_option("--quiet", "-q", action="store_true", default=False, dest="quiet",
                    help="Be quiet, don't output anything."),
        )

    def handle(self, *args, **options):
        urls = []
        url = options.get('url')

        if url:
            urls.append(url)
        else:
            urls = getattr(settings, 'PSI_URLS', None)
            if urls is None:
                raise CommandError("No URLs provided. Please either pass a URL as an argument or define PSI_URLS in settings file.")

        for url in urls:
            page_insight = PageInsight.objects.create(url=url,
                                                      strategy=options.get('strategy'),
                                                      locale=options.get('locale'),
                                                      #rules=options.get('rule')
                                                      )
            page_insight.populate()

            if not options.get('quiet'):
                self._console_report(page_insight)

    def _console_report(self, page_insight):
        print "\n" + _("PageSpeed Insights")
        print "--------------------------------------------\n"
        print "URL: \t\t\t%s" % page_insight.url
        print "Strategy: \t\t%s" % page_insight.strategy
        print "Score: \t\t\t%s\n" % page_insight.score
        print "--------------------------------------------"
        print "\n"