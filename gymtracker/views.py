from django.shortcuts import redirect, render
from .models import Workout, Exercise , ExerciseWorkout
from .forms import CreateWorkoutForm
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

def workout_view(request):
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'gymtracker/routines.html', {'workouts': workouts})

def create_workout(request):
    if request.method == 'POST':
        form = CreateWorkoutForm(request.POST)
        if form.is_valid():
            # Guardar el entrenamiento
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()

            # Manejar los ejercicios seleccionados
            exercise_ids = request.POST.getlist('ejercicios[]')  # IDs de los ejercicios seleccionados
            exercises = Exercise.objects.filter(id__in=exercise_ids)

            # Relacionar ejercicios con el entrenamiento
            for exercise in exercises:
                ExerciseWorkout.objects.create(workout=workout, exercise=exercise)

            messages.success(request, 'Workout created successfully.')
            return redirect('workouts')
        else:
            messages.error(request, 'Error creating your workout. Please check the form.')
    else:
        form = CreateWorkoutForm()

    # Obtener todos los ejercicios para mostrarlos en el modal
    exercises = Exercise.objects.all()

    # Obtener filtros dinámicos (por ejemplo, músculos únicos)
    muscles = Exercise.objects.values_list('primary_muscle', flat=True).distinct()

    return render(request, 'gymtracker/create_workout.html', {
        'form': form,
        'exercises': exercises,  # Pasar ejercicios al template
        'muscles': muscles,  # Pasar los filtros dinámicos
    })