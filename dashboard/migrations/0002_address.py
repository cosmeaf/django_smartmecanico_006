# Generated by Django 4.2.7 on 2023-11-05 18:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('cep', models.CharField(max_length=10)),
                ('logradouro', models.CharField(max_length=255)),
                ('complemento', models.CharField(blank=True, max_length=255, null=True)),
                ('bairro', models.CharField(max_length=100)),
                ('localidade', models.CharField(max_length=100)),
                ('uf', models.CharField(max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Endereço',
                'verbose_name_plural': 'Endereços',
            },
        ),
    ]
