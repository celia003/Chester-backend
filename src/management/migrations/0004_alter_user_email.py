# Generated by Django 4.2.8 on 2024-01-25 16:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(unique=True, validators=[django.core.validators.EmailValidator(message='Invalid Email')]),
        ),
    ]
