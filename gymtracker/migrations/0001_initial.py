# Generated by Django 5.1.5 on 2025-01-24 16:10

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('image_path', models.CharField(blank=True, max_length=255, null=True)),
                ('primary_muscle', models.CharField(blank=True, max_length=100, null=True)),
                ('secondary_muscle', models.CharField(blank=True, max_length=100, null=True)),
                ('equipment', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseWorkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rest_time', models.DurationField(default=datetime.timedelta(0), help_text='Rest time (HH:MM:SS)')),
                ('order', models.PositiveIntegerField(default=1, help_text='Order of the exercise in the workout')),
                ('weight_unit', models.CharField(choices=[('kg', 'Kilograms'), ('lb', 'Pounds')], default='kg', max_length=2)),
                ('exercise', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gymtracker.exercise')),
            ],
            options={
                'verbose_name': 'Workout Exercise',
                'verbose_name_plural': 'Workout Exercises',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(help_text='Weight used in this set')),
                ('repetitions', models.PositiveIntegerField(help_text='Number of repetitions in this set')),
                ('set_number', models.PositiveIntegerField(help_text='Set number (e.g., 1, 2, 3)')),
                ('workout_exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets', to='gymtracker.exerciseworkout')),
            ],
            options={
                'verbose_name': 'Set',
                'verbose_name_plural': 'Sets',
                'ordering': ['set_number'],
            },
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('exercises', models.ManyToManyField(through='gymtracker.ExerciseWorkout', to='gymtracker.exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='exerciseworkout',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_workouts', to='gymtracker.workout'),
        ),
    ]
