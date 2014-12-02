
# Django-PSI

Performance is a feature&mdash;integrate Google PageSpeed Insights into your Django project's development workflow and continuously work towards improving the performance of your user's experience.

Django-PSI provides both command line reporting and database archiving of PSI results for analysis. Django-PSI also provides the admin views for reviewing the results by default.


## Install

Inside your project's virtualenv...

```bash
$ pip install django-psi
```

Next, add django-psi to your `INSTALLED_APPS` settings configuration.

```python
INSTALLED_APPS = (
	...
    'psi',
)
```

Execute migrations to create `psi` tables.

```python
./manage.py migrate psi
```

You're all set! 

## Optional Settings

These project settings.py values are not required, but are available to reduce having to provide them when executing the management command. You can always override these settings.py values when executing the management command by supplying their matching arguments.

### GOOGLE_API_KEY

TYPE: String

The [Google developer API](https://code.google.com/apis/console/) key used when making the request. Unless Specified defaults to use the free tier on PageSpeed Insights. 

Example:

```python
GOOGLE_API_KEY = "SOME%GOOG*&API*KEY"
````

### PSI_URLS

TYPE: tuple

A collection of URLs to be iterated over during execution.

Example:

```python
PSI_URLS = (
    'http://www.djangoproject.com',
    'http://www.djangocon.us',
    'http://www.djangocon.eu'
)
```

### PSI_SCREENSHOT

TYPE: Boolean

If True (default) screenshots will be saved to the file system.

### PSI_MEDIA_PATH

TYPE: String

A path that will be appended to your MEDIA_ROOT that defines where downloaded screenshots will be saved.

### PSI_CELERY_QUEUE

Type: String

A queue name that will be used to process celery tasks (see below). Defaults to 'default'.


## Management Command

Getting started is easy. Execute the below to create entries in the database, and also produce a console report.

```python
./manage.py insights http://www.djangoproject.com
```

The above informs `psi` to run PageSpeed Insights on the provided URL, and also prints results to the console.

### Options

### url

Type: String

The URL of the page for which the PageSpeed Insights API should generate results.

If no url is provided, command will attempt to retrieve `PSI_URLS` from the project's settings conf.

### strategy

Type: String
Default: 'desktop'

The strategy to use when analyzing the page. Valid values are "desktop" and "mobile".

### locale

Type: String
Default: 'en_US'

The locale that results should be generated in. See the list of supported locales. If the specified locale is not supported, the default locale is used.

### quiet

Type: Boolean
Default: False

Be quiet, don't output anything.


## Usage

Programmatic use is as follows;

```python
from psi.models import PageInsight

# First create an instance of PageInsight
page_insight = PageInsight.objects.create(url='http://example.com',
                                          strategy=PageInsight.STRATEGY_DESKTOP)

# Then populate from Google's PageSpeed Insights API 
page_insight.populate()
```

## Celery

For those that want to populate in the background using celery you can do the following;

```python
from psi.models import PageInsight
from psi.tasks import populate_page_insight

# First create an instance of PageInsight
page_insight = PageInsight.objects.create(url='http://example.com')

# Then populate Google's PageSpeed Insights API using Celery in the background
populate_page_insight.delay(page_insight.pk)
```


## Roadmap/Ideas

* ~~PEP8~~
* ~~Tests~~
* Maybe add support for rules back in?
* Ensure i18ln properly
* Better handling of 400, 404, and 500 responses.
* Some rules provide identifiers in the description (e.g. $1) for interpolating values that are helpful in diagnosing opportunity. Use these.
* More robust PSI_URLS configuration to support grouping, and defining strategy per URL.
* ~~Better console report display.~~ 
* Provide a default, custom admin view charting example, using something like http://dimplejs.org/
* There are some arguments not currently supported (userIP and http). Will eventually add support.
* Progress bar during execution... maybe.
* Simple JSON API.
* Generate link to preview full JSON response since we store it.
* Generate link to view resulting screenshot if one exists.







