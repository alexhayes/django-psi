from optparse import make_option
from django.core.management import BaseCommand, CommandError
from django.core.validators  import URLValidator
from django.conf import settings
from django.utils.translation import ugettext as _
from apiclient.discovery import build
from apiclient.errors import HttpError
from psi.models import PageInsight, RuleResult, Screenshot
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "Create PageSpeedInsights for a given URL."
    option_list = BaseCommand.option_list + (
        make_option("--url", "-u", action="store", dest="url",
                    help="The URL of the page for which the PageSpeed Insights API should generate results."),
        make_option("--strategy", "-s", action="store", dest="strategy", default="desktop", 
                    help="The strategy to use when analyzing the page. Valid values are desktop and mobile."),
        make_option("--locale", "-l", action="store", dest="locale", default="en_US",
                    help="The locale that results should be generated in. See the list of supported locales. If the specified locale is not supported, the default locale is used."),
        make_option("--rule", "-r", action="store", dest="rule",
                    help="The PageSpeed rules to run. Can be specified multiple times (for example, &rule=AvoidBadRequests&rule=MinifyJavaScript) to request multiple rules. If unspecified, all rules for the current strategy are used. Most users of the API should not need to specify this parameter."),
        make_option("--key", "-k", action="store", dest="key",
                    help="The Google developer API key used when making the request. Unless Specified defaults to use the free tier on PageSpeed Insights. Good for getting a feel for how well this tool works for you."),
        make_option("--console", "-c", action="store_true", default=False, dest="console",
                    help="Output the results to the console."),
        make_option("--screenshot", "-i", action="store_true", default=False, dest="screenshot",
                    help="Indicates if binary data containing a screenshot should be included."),
        )

    def _processScreenshot(self, data, page_insight):
        screenshot = Screenshot()
        screenshot.width = data.get('width', 0)
        screenshot.height = data.get('height', 0)
        screenshot.mime_type = data.get('mime_type', None)
        screenshot.data = data.get('data', None)
        screenshot.page_insight = page_insight
        screenshot.save()

    def _processRules(self, data, page_insight):
        for key in data:
            ruleResult = RuleResult()
            ruleResult.title = data[key]['localizedRuleName']
            ruleResult.impact = data[key]['ruleImpact']
            ruleResult.description = data[key]['urlBlocks'][0]['header']['format']
            ruleResult.page_insight = page_insight
            ruleResult.save()

    def _processPageInsight(self, data):
        page_insight = PageInsight()
        page_insight.json = data
        page_insight.response_code = data["responseCode"]
        page_insight.title = data["title"]
        page_insight.score = data["score"]
        page_insight.url = data['id']
        page_insight.number_resources = data['pageStats']["numberResources"]
        page_insight.number_hosts = data['pageStats']["numberHosts"]
        page_insight.total_request_bytes = int(data['pageStats']["totalRequestBytes"])
        page_insight.number_static_resources = data['pageStats']["numberStaticResources"]
        page_insight.html_response_bytes = int(data['pageStats']["htmlResponseBytes"])
        page_insight.css_response_bytes = int(data['pageStats'].get("cssResponseBytes", 0))
        page_insight.image_response_bytes = int(data['pageStats'].get("imageResponseBytes", 0))
        page_insight.javascript_response_bytes = int(data['pageStats'].get("javascriptResponseBytes", 0))
        page_insight.other_response_bytes = int(data['pageStats'].get("otherResponseBytes", 0))
        page_insight.number_js_resources = int(data['pageStats'].get("numberJsResources", 0))
        page_insight.number_css_resources = int(data['pageStats'].get("numberCssResources", 0))
        page_insight.screenshot = data.get('screenshot', None)
        page_insight.strategy = self.strategy
        page_insight.save()
        return page_insight

    def _process_results(self, data):
        page_insight = self._processPageInsight(data)
        self._processRules(data['formattedResults']['ruleResults'], page_insight)
        if self.screenshot:
            self._processScreenshot(data['screenshot'], page_insight)
        if self.console:
            self._console_report(page_insight)

    def _console_report(self, page_insight):
        print "\n" + _("PageSpeed Insights")
        print "--------------------------------------------\n"
        print "URL: \t\t\t%s" % page_insight.url
        print "Strategy: \t\t%s" % page_insight.strategy
        print "Score: \t\t\t%s\n" % page_insight.score
        print "--------------------------------------------"
        for field in page_insight._meta.get_all_field_names():
            if field not in ('json', 'ruleresult', 'screenshot', 'score', 'url', 'strategy', 'id', 'title', 'created_date'):
                print "%s\t\t\t%s" % (field, page_insight._meta.get_field(field).value_from_object(page_insight))
        print "--------------------------------------------\n"
        for result in page_insight.ruleresult_set.all():
            print "%s\t\t\t%s" % (result.title, result.impact)
        print "\n"

    def handle(self, *args, **options):
        try:
            urls = []
            url = options.get('url')

            if url:
                urls.append(url)
            else:
                surls = getattr(settings, 'PSI_URLS', None)
                if surls:
                    for url in surls:
                        urls.append(url)
                else:
                    raise BaseException("No URLs provided. Please either pass a URL as an argument or define PSI_URLS in settings file.")

            self.console = options.get('console')
            self.screenshot = options.get('screenshot')
            self.strategy = options.get('strategy')
            locale = options.get('locale')
            rule = options.get('rule')
            key = options.get('key')

            if options.get('key', False):
                key = getattr(settings, 'GOOGLE_API_KEY', None)

            service = build(serviceName='pagespeedonline', version='v1', developerKey=key)
            for url in urls:
                try:
                    URLValidator(url)
                except ValidationError, e:
                    raise e
                results = service.pagespeedapi().runpagespeed(url=url, strategy=self.strategy, locale=locale, rule=rule, screenshot=self.screenshot).execute()
                self._process_results(results)
        except HttpError, e:
            raise e