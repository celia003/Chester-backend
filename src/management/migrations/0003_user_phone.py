# Generated by Django 4.2.8 on 2024-01-20 00:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_useraccesstoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+0034999999999'. Up to 13 digits allowed.", regex='^00\\d{11}$')]),
        ),
    ]