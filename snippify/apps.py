from django.apps import AppConfig


class SnippifyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'snippify'

    def ready(self):
        import snippify.signals
