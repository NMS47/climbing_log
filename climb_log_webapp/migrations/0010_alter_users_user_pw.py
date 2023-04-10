# Generated by Django 4.1.7 on 2023-04-10 01:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('climb_log_webapp', '0009_alter_users_user_pw'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_pw',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(6)]),
        ),
    ]
