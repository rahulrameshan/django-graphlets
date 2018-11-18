from django.contrib import admin

from . import models


class PageViewAdmin(admin.ModelAdmin):

    list_display = ['ip_address', 'date']
    list_filter = ['ip_address']


admin.site.register(models.PageView, PageViewAdmin)
