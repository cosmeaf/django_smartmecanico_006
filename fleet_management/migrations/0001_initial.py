# Generated by Django 4.2.7 on 2023-11-06 11:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0008_remove_purchase_item_delete_item_delete_purchase'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('driver_license_number', models.CharField(max_length=50)),
                ('license_expiry_date', models.DateField()),
                ('contact_info', models.JSONField(blank=True, help_text='Informações de contato do motorista em formato JSON', null=True)),
            ],
            options={
                'verbose_name': 'Motorista',
                'verbose_name_plural': 'Motoristas',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='FleetVehicle',
            fields=[
                ('vehicle_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.vehicle')),
                ('fleet_number', models.CharField(max_length=50, unique=True)),
                ('service_interval_km', models.IntegerField(help_text='Intervalo de serviço recomendado em quilômetros')),
                ('next_service_date', models.DateField(help_text='Data do próximo serviço planejado')),
                ('insurance_policy_number', models.CharField(max_length=255)),
                ('insurance_expiry_date', models.DateField()),
                ('registration_expiry_date', models.DateField()),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('mileage', models.IntegerField()),
                ('tracker_device_id', models.CharField(blank=True, help_text='ID do dispositivo de rastreamento GPS', max_length=255, null=True)),
                ('equipment', models.JSONField(blank=True, help_text='Equipamentos adicionais e suas configurações em formato JSON', null=True)),
                ('assigned_driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fleet_management.driver')),
            ],
            options={
                'verbose_name': 'Veículo de Frota',
                'verbose_name_plural': 'Veículos de Frota',
                'ordering': ['fleet_number'],
            },
            bases=('dashboard.vehicle',),
        ),
        migrations.CreateModel(
            name='ExpenseRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('expense_type', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vendor', models.CharField(blank=True, max_length=255, null=True)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet_management.fleetvehicle')),
            ],
            options={
                'verbose_name': 'Registro de Despesa',
                'verbose_name_plural': 'Registros de Despesas',
                'ordering': ['-date', 'vehicle'],
            },
        ),
        migrations.AddField(
            model_name='driver',
            name='assigned_vehicles',
            field=models.ManyToManyField(blank=True, related_name='assigned_drivers', to='fleet_management.fleetvehicle'),
        ),
        migrations.CreateModel(
            name='TripLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('start_location', models.CharField(blank=True, max_length=255, null=True)),
                ('end_location', models.CharField(blank=True, max_length=255, null=True)),
                ('distance_km', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fleet_management.driver')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet_management.fleetvehicle')),
            ],
            options={
                'verbose_name': 'Registro de Viagem',
                'verbose_name_plural': 'Registros de Viagem',
                'ordering': ['-start_time'],
                'indexes': [models.Index(fields=['start_time'], name='fleet_manag_start_t_d43d9f_idx')],
            },
        ),
        migrations.CreateModel(
            name='MaintenanceRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('service_type', models.CharField(max_length=100)),
                ('service_date', models.DateField()),
                ('details', models.TextField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('performed_by', models.CharField(max_length=255)),
                ('next_service_due', models.DateField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fleet_management.fleetvehicle')),
            ],
            options={
                'verbose_name': 'Registro de Manutenção',
                'verbose_name_plural': 'Registros de Manutenção',
                'ordering': ['-service_date', 'vehicle'],
                'indexes': [models.Index(fields=['vehicle'], name='fleet_manag_vehicle_2c3a16_idx'), models.Index(fields=['service_date'], name='fleet_manag_service_79e085_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='fleetvehicle',
            index=models.Index(fields=['fleet_number'], name='fleet_manag_fleet_n_aac9a2_idx'),
        ),
        migrations.AddIndex(
            model_name='fleetvehicle',
            index=models.Index(fields=['location'], name='fleet_manag_locatio_b7607d_idx'),
        ),
        migrations.AddIndex(
            model_name='expenserecord',
            index=models.Index(fields=['vehicle'], name='fleet_manag_vehicle_61456a_idx'),
        ),
        migrations.AddIndex(
            model_name='expenserecord',
            index=models.Index(fields=['date'], name='fleet_manag_date_c78556_idx'),
        ),
        migrations.AddIndex(
            model_name='driver',
            index=models.Index(fields=['last_name', 'first_name'], name='fleet_manag_last_na_eacd8f_idx'),
        ),
    ]