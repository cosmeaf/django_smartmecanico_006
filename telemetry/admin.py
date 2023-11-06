from django.contrib import admin
from .models import TelemetryData



@admin.register(TelemetryData)
class TelemetryDataAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'engine_rpm', 'vehicle_speed', 'coolant_temp', 'fuel_level',)
    list_filter = ('vehicle__brand', 'vehicle__model', 'created_at')
    search_fields = ('vehicle__plate', 'vehicle__vin')
    readonly_fields = ('id', 'created_at', 'updated_at')
    autocomplete_fields = ['vehicle']

    fieldsets = (
        ('Vehicle Information', {
            'fields': ('vehicle',)
        }),
        ('Diagnostic Data', {
            'fields': ('dtcs', 'error_count', 'driving_time_since_last_error')
        }),
        ('Performance Data', {
            'fields': ('engine_rpm', 'vehicle_speed', 'coolant_temp', 'fuel_level', 'engine_load')
        }),
        ('Additional Data', {
            'fields': ('throttle_position', 'intake_air_temp', 'airflow_rate', 'fuel_pressure', 'intake_manifold_pressure', 
                       'timing_advance', 'oxygen_sensors_voltage', 'fuel_system_status', 'short_term_fuel_trim', 
                       'long_term_fuel_trim', 'ambient_air_temp', 'battery_voltage', 'fuel_trim', 
                       'emission_requirements', 'oil_temperature', 'tire_pressure', 'gear')
        }),
        ('Record Info', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def has_add_permission(self, request, obj=None):
        # Desativar a adição de novos registros
        return False

    def has_change_permission(self, request, obj=None):
        # Desativar a edição de registros existentes
        return False

    def has_delete_permission(self, request, obj=None):
        # Desativar a deleção de registros
        return False

