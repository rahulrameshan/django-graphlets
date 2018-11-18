import datetime

from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

STEP_DAY = 'd'
STEP_MONTH = 'm'
STEP_YEAR = 'y'


class Chart(models.Model):

    TYPE_CHOICES = (
        ('line', _('Line')),
        ('bar', _('Bar')),
        ('pie', _('Pie')),
        ('area-spline', _('Area')),
        ('scatter', _('Scatter')),
        ('donut', _('Donut')),
    )

    UNTIL_CHOICES = (
        ('t', _('This day/week/month/year')),
        ('y', _('Last day/week/month/year')),
        ('s', _('Specific Date')),
    )

    STEP_CHOICES = (
        (STEP_DAY, _('Days')),
        (STEP_MONTH, _('Months')),
        (STEP_YEAR, _('Years')),
    )
    title = models.CharField(max_length=200)
    chart_type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, default='line')
    until_type = models.CharField(
        max_length=1, choices=UNTIL_CHOICES, default='t')
    until_date = models.DateField(default=timezone.now)
    period_count = models.IntegerField()
    period_step = models.CharField(
        max_length=1, choices=STEP_CHOICES, default=STEP_DAY)

    def get_end_date(self):
        """Returns the date after the last period"""
        if self.until_type in ('t', 'y'):
            date = timezone.now().date()
            if self.until_type == 'y':
                date = date - self.move_delta()
            if self.period_step == STEP_MONTH:
                if date.month >= 12:
                    return datetime.date(date.year+1, 1, 1)
                return datetime.date(date.year, date.month+1, 1)
            if self.period_step == STEP_YEAR:
                return datetime.date(date.year+1, 1, 1)
            return date + datetime.timedelta(days=1)
        return self.until_date + datetime.timedelta(days=1)

    def move_delta(self, amount=1):
        if self.period_step == STEP_YEAR:
            return relativedelta(years=amount)
        if self.period_step == STEP_MONTH:
            return relativedelta(months=amount)
        return relativedelta(days=amount)

    def dates(self):
        end = self.get_end_date()
        reverse_dates = []
        delta = self.move_delta()
        for _i in range(self.period_count):
            end = end - delta
            reverse_dates.append(end)
        return reversed(reverse_dates)

    def span(self):
        end = self.get_end_date()
        start = end - self.move_delta(self.period_count)
        return start, end

    def __str__(self):
        return self.title


class Criteria(models.Model):

    SIDE_CHOICES = (('l', _('Left')), ('r', _('Right')))

    chart = models.ForeignKey(
        Chart, on_delete=models.CASCADE, related_name='criteria')
    stats_key = models.CharField(max_length=200)
    side = models.CharField(
        max_length=1, choices=SIDE_CHOICES, default='l')

    def __str__(self):
        return self.stats_key
