# Generated by Django 4.2.7 on 2023-11-07 22:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_remove_purchase_item_delete_item_delete_purchase'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('rating', models.PositiveIntegerField(default=5)),
                ('content', models.TextField()),
                ('author_name', models.CharField(max_length=255)),
                ('author_title', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='testimonials/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testimonial', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Depoimento',
                'verbose_name_plural': 'Depoimentos',
                'indexes': [models.Index(fields=['author_name'], name='dashboard_t_author__232cce_idx')],
            },
        ),
    ]
