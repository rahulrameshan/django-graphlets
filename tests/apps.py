from django.apps import AppConfig
from django.core.management import call_command

try:
    from django.test.utils import setup_databases
except ImportError:  # workaround for django 1.10
    from django.test.runner import setup_databases


class TestConfig(AppConfig):
    name = 'tests'
    verbose_name = 'TrackStats Admin Test'

    def ready(self):
        setup_databases(verbosity=3, interactive=False)


class DemoConfig(AppConfig):
    name = 'tests'
    verbose_name = 'TrackStats Admin Demo'

    def ready(self):
        setup_databases(verbosity=3, interactive=False)
        # add notification objects
        call_command('loaddata', 'demo')
