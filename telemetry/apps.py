from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class TelemetryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telemetry'
    verbose_name = _('02 - telemetria')