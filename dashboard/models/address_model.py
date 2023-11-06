from django.db import models
from dashboard.models.user_model import CustomUser
from dashboard.models.base_model import Base


class Address(Base):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='address')
    cep = models.CharField(max_length=10)
    logradouro = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=100)
    localidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
        indexes = [
                models.Index(fields=['cep']),
            ]
    def __str__(self):
        return self.cep
