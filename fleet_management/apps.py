from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FleetManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fleet_management'
    verbose_name = _('03 - Gestão de Frota')
