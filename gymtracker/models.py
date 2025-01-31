from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.core.exceptions import ValidationError

class Workout(models.Model):
    name = models.CharField(max_length=100)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    exercises = models.ManyToManyField('Exercise', through='ExerciseWorkout')

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=100)  
    description = models.TextField(null=True, blank=True)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    primary_muscle = models.CharField(max_length=100, null=True, blank=True)
    secondary_muscle = models.CharField(max_length=100, null=True, blank=True)
    equipment = models.CharField(max_length=100, null=True, blank=True) 

    def __str__(self):
        return self.name
class ExerciseWorkout(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE,related_name="exercise_workouts")  
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True, blank=True)  
    rest_time = models.DurationField(default=timedelta(seconds=0), help_text="Rest time (HH:MM:SS)")  
    order = models.PositiveIntegerField(default=1, help_text="Order of the exercise in the workout")
    WEIGHT_UNITS = [
        ('kg', 'Kilograms'),
        ('lb', 'Pounds'),
    ] 
    weight_unit = models.CharField(max_length=2, choices=WEIGHT_UNITS, default='kg')  

    class Meta:
        verbose_name = "Workout Exercise"
        verbose_name_plural = "Workout Exercises"
        ordering = ['order'] 
    
    def save(self, *args, **kwargs):
        if not self.pk:
            last_order = ExerciseWorkout.objects.filter(workout=self.workout).aggregate(
                max_order=models.Max('order')
            )['max_order']
            self.order = (last_order or 0) + 1 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.exercise.name} in {self.workout.name}"
    


class Set(models.Model):
    workout_exercise = models.ForeignKey(
        ExerciseWorkout, 
        on_delete=models.CASCADE, 
        related_name="sets"
    ) 
    weight = models.FloatField(help_text="Weight used in this set")
    repetitions = models.PositiveIntegerField(help_text="Number of repetitions in this set")
    set_number = models.PositiveIntegerField(help_text="Set number (e.g., 1, 2, 3)")

    class Meta:
        verbose_name = "Set"
        verbose_name_plural = "Sets"
        ordering = ['set_number']

    def clean(self):
        if self.weight < 0:
            raise ValidationError({'weight': 'Weight cannot be negative.'})

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Set {self.set_number} - {self.repetitions} reps, {self.weight}"


class LoggedWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_workout = models.ForeignKey(
        Workout, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Rutina original"
    )
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True, verbose_name="Notas adicionales")

    def __str__(self):
        return f"{self.date} - {self.original_workout.name if self.original_workout else 'Custom Workout'}"

class LoggedExercise(models.Model):
    logged_workout = models.ForeignKey(
        LoggedWorkout, 
        on_delete=models.CASCADE,
        related_name='logged_exercises'
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ejercicio original"
    )
    exercise_name = models.CharField(max_length=100, verbose_name="Nombre del ejercicio")
    rest_time = models.DurationField(verbose_name="Tiempo de descanso")
    order = models.PositiveIntegerField(verbose_name="Orden en la rutina")
    weight_unit = models.CharField(
        max_length=2, 
        choices=ExerciseWorkout.WEIGHT_UNITS, 
        default='kg',
        verbose_name="Unidad de peso"
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.exercise_name} (Logged)"

class LoggedSet(models.Model):
    logged_exercise = models.ForeignKey(
        LoggedExercise, 
        on_delete=models.CASCADE,
        related_name='logged_sets'
    )
    weight = models.FloatField(verbose_name="Peso")
    repetitions = models.PositiveIntegerField(verbose_name="Repeticiones")
    set_number = models.PositiveIntegerField(verbose_name="Número de serie")

    class Meta:
        ordering = ['set_number']

    def __str__(self):
        return f"Logged Set {self.set_number}"