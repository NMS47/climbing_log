# Generated by Django 4.1.7 on 2023-04-09 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('climb_log_webapp', '0005_remove_climb_entry_id_alter_climb_entry_entry_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='creation_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
