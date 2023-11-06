from django.db import models
from dashboard.models.vehicle_model import Vehicle
import uuid

class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)
    deleted_at = models.DateTimeField('Data de Exclusão', null=True, blank=True)

    class Meta:
        abstract = True

class TelemetryData(Base):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='telemetry_data')
    dtcs = models.JSONField(null=True, blank=True)  # Diagnostic Trouble Codes em formato JSON
    engine_rpm = models.IntegerField(null=True, blank=True)  # Revoluções Por Minuto do motor
    vehicle_speed = models.IntegerField(null=True, blank=True)  # Velocidade do veículo
    coolant_temp = models.IntegerField(null=True, blank=True)  # Temperatura do líquido de arrefecimento
    fuel_level = models.FloatField(null=True, blank=True)  # Nível de combustível
    throttle_position = models.FloatField(null=True, blank=True)  # Posição da borboleta do acelerador
    intake_air_temp = models.IntegerField(null=True, blank=True)  # Temperatura do ar admitido
    airflow_rate = models.FloatField(null=True, blank=True)  # Taxa de fluxo de ar
    fuel_pressure = models.IntegerField(null=True, blank=True)  # Pressão do combustível
    intake_manifold_pressure = models.IntegerField(null=True, blank=True)  # Pressão do coletor de admissão
    timing_advance = models.FloatField(null=True, blank=True)  # Avanço de ignição
    oxygen_sensors_voltage = models.JSONField(null=True, blank=True)  # Tensões dos sensores de oxigênio
    fuel_system_status = models.CharField(max_length=100, null=True, blank=True)  # Status do sistema de combustível
    short_term_fuel_trim = models.FloatField(null=True, blank=True)  # Correção de combustível a curto prazo
    long_term_fuel_trim = models.FloatField(null=True, blank=True)  # Correção de combustível a longo prazo
    engine_load = models.FloatField(null=True, blank=True)  # Carga do motor
    ambient_air_temp = models.IntegerField(null=True, blank=True)  # Temperatura do ar ambiente
    battery_voltage = models.FloatField(null=True, blank=True)  # Tensão da bateria
    error_count = models.IntegerField(null=True, blank=True)  # Contagem de erros
    driving_time_since_last_error = models.IntegerField(null=True, blank=True)  # Tempo de condução desde o último erro
    fuel_trim = models.FloatField(null=True, blank=True)  # Ajuste de combustível
    emission_requirements = models.CharField(max_length=100, null=True, blank=True)  # Requisitos de emissões atendidos
    oil_temperature = models.IntegerField(null=True, blank=True)  # Temperatura do óleo
    tire_pressure = models.JSONField(null=True, blank=True)  # Pressão dos pneus
    gear = models.CharField(max_length=10, null=True, blank=True)  # Marcha atual


    class Meta:
        verbose_name = "Telemetria"
        verbose_name_plural = "Telemetrias"
        ordering = ['-created_at'] 
        indexes = [
            models.Index(fields=['id']),
        ]

    def __str__(self):
        return f"Telemetry Data for {self.vehicle.plate}"
 

class VehicleLocation(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    recorded_at = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        verbose_name = "Localização do Veículo"
        verbose_name_plural = "Localizações dos Veículos"
        ordering = ['-recorded_at']  # Ordenação padrão por data de registro
        indexes = [
            models.Index(fields=['recorded_at']),
            models.Index(fields=['vehicle']),
        ]
        
    def __str__(self):
            return f"Localização para {self.vehicle} em {self.recorded_at.strftime('%Y-%m-%d %H:%M:%S')}"
