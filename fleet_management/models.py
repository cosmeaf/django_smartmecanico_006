# fleet_management/models.py

from django.db import models
from dashboard.models.base_model import Base
from dashboard.models.vehicle_model import Vehicle

class FleetVehicle(Vehicle):
    fleet_number = models.CharField(max_length=50, unique=True)
    assigned_driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True, blank=True)
    service_interval_km = models.IntegerField(help_text="Intervalo de serviço recomendado em quilômetros")
    next_service_date = models.DateField(help_text="Data do próximo serviço planejado")
    insurance_policy_number = models.CharField(max_length=255)
    insurance_expiry_date = models.DateField()
    registration_expiry_date = models.DateField()
    location = models.CharField(max_length=255, null=True, blank=True)
    mileage = models.IntegerField()
    tracker_device_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID do dispositivo de rastreamento GPS")
    equipment = models.JSONField(blank=True, null=True, help_text="Equipamentos adicionais e suas configurações em formato JSON")

    class Meta:
        verbose_name = "Veículo de Frota"
        verbose_name_plural = "Veículos de Frota"
        ordering = ['fleet_number']
        indexes = [
            models.Index(fields=['fleet_number']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return f"{self.fleet_number} - {self.brand} {self.model}"


class MaintenanceRecord(Base):
    vehicle = models.ForeignKey(FleetVehicle, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    service_date = models.DateField()
    details = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    performed_by = models.CharField(max_length=255)
    next_service_due = models.DateField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
          verbose_name = "Registro de Manutenção"
          verbose_name_plural = "Registros de Manutenção"
          indexes = [
              models.Index(fields=['vehicle']),
              models.Index(fields=['service_date']),
          ]
          ordering = ['-service_date', 'vehicle']

    def __str__(self):
        return f"Manutenção para {self.vehicle.fleet_number} em {self.service_date}"


class ExpenseRecord(Base):
    vehicle = models.ForeignKey(FleetVehicle, on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Registro de Despesa"
        verbose_name_plural = "Registros de Despesas"
        indexes = [
            models.Index(fields=['vehicle']),
            models.Index(fields=['date']),
        ]
        ordering = ['-date', 'vehicle']

    def __str__(self):
        return f"Despesa para {self.vehicle.fleet_number} em {self.date}"


class Driver(Base):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    driver_license_number = models.CharField(max_length=50)
    license_expiry_date = models.DateField()
    contact_info = models.JSONField(blank=True, null=True, help_text="Informações de contato do motorista em formato JSON")
    assigned_vehicles = models.ManyToManyField(FleetVehicle, blank=True, related_name='assigned_drivers')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Motorista"
        verbose_name_plural = "Motoristas"
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
        ]
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class TripLog(models.Model):
    vehicle = models.ForeignKey(FleetVehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    start_location = models.CharField(max_length=255, null=True, blank=True)
    end_location = models.CharField(max_length=255, null=True, blank=True)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Registro de Viagem"
        verbose_name_plural = "Registros de Viagem"
        indexes = [
            models.Index(fields=['start_time']),
        ]
        ordering = ['-start_time']


    def __str__(self):
        return f"{self.vehicle} - {self.start_time.strftime('%Y-%m-%d %H:%M')} a {self.end_time.strftime('%Y-%m-%d %H:%M') if self.end_time else 'em andamento'}"

