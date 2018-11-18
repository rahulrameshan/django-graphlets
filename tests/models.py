from django.db import models
from trackstats.models import Domain, Metric, Period, StatisticByDate

from django_graphlets.registry import register_metric, register_model

Domain.objects.PAGES = Domain.objects.register(
    ref='page', name='Page Stats')

Metric.objects.PAGE_VIEWS = Metric.objects.register(
    ref='view', domain=Domain.objects.PAGES, name='Page views')


class PageView(models.Model):

    ip_address = models.GenericIPAddressField()
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # auto-generate trackstats stats
        today = self.date.date()
        count = PageView.objects.filter(
            date__year=today.year,
            date__month=today.month,
            date__day=today.day,
        ).count()
        StatisticByDate.objects.record(
            metric=Metric.objects.PAGE_VIEWS,
            value=count,
            period=Period.DAY,
            date=today
        )


register_metric(Metric.objects.PAGE_VIEWS)
register_model(PageView)
