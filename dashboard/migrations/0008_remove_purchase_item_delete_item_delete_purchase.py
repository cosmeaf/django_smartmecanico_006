# Generated by Django 4.2.7 on 2023-11-06 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_item_purchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='item',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='Purchase',
        ),
    ]
