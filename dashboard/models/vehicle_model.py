from django.db import models
from dashboard.models.user_model import CustomUser
from dashboard.models.base_model import Base


class Vehicle(Base):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vehicles')
    brand = models.CharField('Marca', max_length=100)
    model = models.CharField('Modelo', max_length=100)
    fuel = models.CharField('Combustível', max_length=50)
    year = models.CharField('Ano', max_length=4)
    odometer = models.CharField('Hodometro', max_length=20)
    plate = models.CharField('Placa', max_length=15, unique=True)
    vin = models.CharField('Chassi', max_length=17, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ['-deleted_at', '-updated_at', 'year', 'brand', 'plate', 'vin']
        indexes = [
                models.Index(fields=['plate']),
            ]
    def __str__(self):
        return self.plate
