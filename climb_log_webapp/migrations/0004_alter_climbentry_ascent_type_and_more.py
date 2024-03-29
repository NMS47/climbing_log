# Generated by Django 4.2.2 on 2023-07-22 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('climb_log_webapp', '0003_alter_climbentry_ascent_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='climbentry',
            name='ascent_type',
            field=models.CharField(blank=True, default='flash', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='climbentry',
            name='num_attempts',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True),
        ),
    ]
