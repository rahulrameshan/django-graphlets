import collections

import django.http
from django import forms
from django.conf.urls import url
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from . import models, registry


class CriteriaForm(forms.ModelForm):
    stats_key = forms.ChoiceField(choices=registry.REGISTRY.choices())


class CriteriaInline(admin.TabularInline):
    form = CriteriaForm
    model = models.Criteria
    min_num = 1
    extra = 0


class ChartAdmin(admin.ModelAdmin):
    change_form_template = 'django_graphlets/chart/change_form.html'
    inlines = [CriteriaInline]
    list_display = ('title', 'chart_type', 'show_action_links')
    list_filter = ('chart_type',)
    chart_template = 'django_graphlets/chart/chart.html'

    class Media:
        js = ('django_graphlets/chart_form.js',)

    def get_urls(self):
        return [
            url(
                r'^(?P<chart_id>\w+)/chart$',
                self.admin_site.admin_view(self.view_chart),
                name='django_graphlets_chart'),
            ] + super().get_urls()

    def show_action_links(self, obj):
        return format_html(
            '<a href="{url}">{text}</a>',
            text=_('Show Chart'), url='{}/chart'.format(obj.pk))
    show_action_links.short_description = _('Actions')

    def view_chart(self, request, chart_id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        chart = self.get_object(request, chart_id)  # type: models.Chart
        if chart is None:
            raise django.http.Http404()
        if request.method != 'GET':
            return django.http.HttpResponseNotAllowed(('GET',))

        chart_header = list(chart.dates())
        chart_rows = collections.OrderedDict()
        for criteria in chart.criteria.all():
            row = [0] * len(chart_header)

            for date, count in registry.REGISTRY.count(criteria).items():
                try:
                    date_idx = chart_header.index(date)
                    row[date_idx] = count
                except ValueError:
                    pass
            label = registry.REGISTRY[criteria.stats_key].label
            chart_rows[label] = row

        context = {
            'title': _('View Chart: %s') % chart.title,
            'media': self.media,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'chart': chart,
            'header': chart_header,
            'rows': chart_rows,
            'save_as': False,
            'show_save': True,
        }
        context.update(self.admin_site.each_context(request))
        request.current_app = self.admin_site.name
        return TemplateResponse(request, self.chart_template, context)


admin.site.register(models.Chart, ChartAdmin)
