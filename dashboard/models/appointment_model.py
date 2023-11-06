from django.db import models
from dashboard.models.base_model import Base
from dashboard.models.user_model import CustomUser
from dashboard.models.address_model import Address
from dashboard.models.vehicle_model import Vehicle
from dashboard.models.services_model import Services
from dashboard.models.employee_model import Employee
from datetime import datetime
import uuid

def generate_protocol():
    current_date = datetime.now()
    year = current_date.strftime("%Y")
    month = current_date.strftime("%m")
    date_str = current_date.strftime("%d")
    uuid_str = str(uuid.uuid4())[:12].upper()
    return f'{year}{month}-{date_str}-{uuid_str}'


class Appointment(Base):
    user = models.ForeignKey(CustomUser, verbose_name='Usuário', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name='Endereço', on_delete=models.CASCADE, related_name='Appointment', related_query_name="schedule")
    vehicle = models.ForeignKey(Vehicle, verbose_name='Veículo', on_delete=models.CASCADE, related_name='Appointment', related_query_name="schedule")
    service = models.ForeignKey(Services, verbose_name='Serviço', on_delete=models.CASCADE, related_name='Appointment', related_query_name="schedule")
    time = models.CharField('Hora do Serviço', max_length=5, help_text='Formato: 00:00')
    date = models.DateField('Data do Serviço', help_text='Formato: YYYY-MM-DD')
    protocol = models.CharField('Protocolo', max_length=22, unique=True, default=generate_protocol)
    employee = models.ForeignKey(Employee, verbose_name='Mecânico', on_delete=models.CASCADE, null=True, blank=True)
    cancellation_reason = models.TextField(verbose_name='Justificativa para o cancelamento', blank=True, null=True)

    def clean_fields(self, exclude=None):
        # Validar e formatar o campo 'hour'
        if self.hour:
            try:
                # Tenta converter a hora para o formato desejado
                formatted_hour = datetime.strptime(self.hour, '%H:%M').strftime('%H:%M')
                self.hour = formatted_hour
            except ValueError:
                # Se a conversão falhar, defina a hora como vazia
                self.hour = ''

        # Validar e formatar o campo 'day'
        if self.day:
            try:
                # Converte a data em uma string no formato YYYY-MM-DD
                formatted_day = self.day.strftime('%Y-%m-%d')
                self.day = formatted_day
            except AttributeError:
                # Se a conversão falhar, defina o dia como vazio
                self.day = ''
                
        super().clean_fields(exclude)

    def save(self, *args, **kwargs):
        self.clean_fields()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f'{self.service}'