from django.apps import AppConfig


class Config(AppConfig):
    name = 'django_graphlets'
    verbose_name = 'Statistics Charting'

    def ready(self):
        pass
