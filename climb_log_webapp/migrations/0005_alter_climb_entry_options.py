# Generated by Django 4.1.7 on 2023-05-01 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climb_log_webapp', '0004_alter_climb_entry_place_coord'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='climb_entry',
            options={'ordering': ['date_of_climb']},
        ),
    ]
