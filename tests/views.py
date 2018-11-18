from django.shortcuts import render

from . import models


def index(request):
    models.PageView.objects.create(ip_address=request.META['REMOTE_ADDR'])
    context = {'count': models.PageView.objects.count()}
    return render(request, 'tests/index.txt', context)
