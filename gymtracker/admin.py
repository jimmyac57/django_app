from django.contrib import admin
from .models import Workout
from .models import Exercise
from .models import ExerciseWorkout
# Register your models here.

admin.site.register(Workout)
@admin.register(Exercise)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_muscle', 'secondary_muscle')
    list_filter = ('primary_muscle',)

admin.site.register(ExerciseWorkout)
