from django.db import models
from dashboard.models.user_model import CustomUser
from dashboard.models.base_model import Base


class Employee(Base):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='employee')

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        indexes = [
                models.Index(fields=['user']),
            ]
    def __str__(self):
        return self.user.email
