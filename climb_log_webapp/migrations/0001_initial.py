# Generated by Django 4.1.7 on 2023-04-06 00:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Climb_entry',
            fields=[
                ('user_id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('date', models.DateField()),
                ('place_name', models.CharField(max_length=40)),
                ('place_coord', models.CharField(max_length=30)),
                ('enviroment', models.CharField(max_length=20)),
                ('climb_style', models.CharField(max_length=15)),
                ('multipitches', models.BooleanField()),
                ('num_pitches', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(15)])),
                ('grade', models.CharField(max_length=6)),
                ('climber_position', models.CharField(max_length=15)),
                ('ascent_type', models.CharField(max_length=20)),
                ('num_attempts', models.PositiveSmallIntegerField()),
                ('notes', models.TextField(max_length=400)),
                ('entry_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=30, unique=True, validators=[django.core.validators.EmailValidator])),
                ('age', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(100)])),
                ('gender', models.CharField(max_length=7)),
                ('user_pw', models.CharField(max_length=100)),
            ],
        ),
    ]
