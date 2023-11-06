from django.core.validators import RegexValidator
from django.db import models
from dashboard.models.user_model import CustomUser
from dashboard.models.base_model import Base
import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('icon', filename)


class Services(Base):
    image = models.ImageField('Image', upload_to=get_file_path, null=True, blank=True)
    user = models.ForeignKey(CustomUser, verbose_name='Usuário', on_delete=models.CASCADE)
    name = models.CharField('Titulo', max_length=255)
    description = models.TextField('Descrição')

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

        indexes = [
                  models.Index(fields=['name']),
              ]
    
    def __str__(self):
        return f'{self.name}'

    def delete_old_image(self):
        try:
            old_service = Services.objects.get(pk=self.pk)
            if old_service.image and old_service.image.name != self.image.name and os.path.isfile(old_service.image.path):
                os.remove(old_service.image.path)
        except Services.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        if self.pk:
            self.delete_old_image()

        super().save(*args, **kwargs)


class HourService(Base):
    user = models.ForeignKey(CustomUser, verbose_name='Usuário', on_delete=models.CASCADE, related_name='hour_service')
    hour = models.CharField(
        'Hora Serviço', 
        max_length=5, 
        validators=[
            RegexValidator(
                regex=r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$',
                message='Hora deve estar no formato HH:MM',
            ),
        ],
    )

    class Meta:
        verbose_name = 'Horário de Atendimento'
        verbose_name_plural = 'Horários de Atendimento'

        indexes = [
                  models.Index(fields=['hour']),
              ]
    
    def __str__(self):
        return f'{self.hour}'




