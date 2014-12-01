from psi.models import PageInsight
from celery import task


@task(ignore_result=True)
def populate_page_insight(pk):
    page_insight = PageInsight.objects.get(pk=pk)
    page_insight.populate()