from django.contrib.admin import AdminSite
from django.test import TestCase

import django_graphlets.admin
import django_graphlets.models


class MockSuperUser:

    is_active = True
    is_staff = True

    @staticmethod
    def has_perm(_perm):
        return True


class MockRequest:

    def __init__(self, method, parameters=None):
        self.method = method
        self.user = MockSuperUser()
        self.GET = {}
        self.POST = {}
        if parameters is not None:
            if method == 'POST':
                self.POST = parameters
            else:
                self.GET = parameters
        self.META = {'SCRIPT_NAME': ''}


class AdminTests(TestCase):
    """Test NotificationAdmin"""

    fixtures = ['demo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_class = django_graphlets.models.Chart
        self.admin = django_graphlets.admin.ChartAdmin(
            self.model_class, AdminSite())

    def test_chart(self):
        obj = self.model_class.objects.get(pk=2)
        request = MockRequest('GET', {})
        response = self.admin.view_chart(request, str(obj.id))
        assert response.status_code == 200
        assert '<td>3</td>' in response.rendered_content
