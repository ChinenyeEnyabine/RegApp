from django.apps import AppConfig


class CarbookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carbook'
    def ready(self):
        import carbook.signals  # Import the signals module
