from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class SmartSecureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smart_secure'
    verbose_name = _('05 - segurança')