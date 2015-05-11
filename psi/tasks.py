from psi.models import PageInsight
from celery import task
from django.conf import settings


@task(queue=settings.PSI_CELERY_QUEUE)
def populate_page_insight(pk):
    page_insight = PageInsight.objects.get(pk=pk)
    page_insight.populate()