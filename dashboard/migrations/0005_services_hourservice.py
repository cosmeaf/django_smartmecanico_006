# Generated by Django 4.2.7 on 2023-11-05 18:49

import dashboard.models.services_model
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_vehicle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('image', models.ImageField(blank=True, null=True, upload_to=dashboard.models.services_model.get_file_path, verbose_name='Image')),
                ('name', models.CharField(max_length=255, verbose_name='Titulo')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Serviço',
                'verbose_name_plural': 'Serviços',
                'indexes': [models.Index(fields=['name'], name='dashboard_s_name_2a1c97_idx')],
            },
        ),
        migrations.CreateModel(
            name='HourService',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('hour', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(message='Hora deve estar no formato HH:MM', regex='^([0-1][0-9]|2[0-3]):[0-5][0-9]$')], verbose_name='Hora Serviço')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hour_service', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Horário de Atendimento',
                'verbose_name_plural': 'Horários de Atendimento',
                'indexes': [models.Index(fields=['hour'], name='dashboard_h_hour_507df3_idx')],
            },
        ),
    ]
