# Generated by Django 5.2.3 on 2025-06-15 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='available_stock',
        ),
    ]
