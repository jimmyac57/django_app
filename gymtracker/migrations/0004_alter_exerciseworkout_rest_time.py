# Generated by Django 5.1.5 on 2025-01-21 03:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymtracker', '0003_exercise_equipment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseworkout',
            name='rest_time',
            field=models.DurationField(default=datetime.timedelta(0), help_text='Rest time (HH:MM:SS)'),
        ),
    ]
