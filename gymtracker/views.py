from django.shortcuts import redirect, render
from .models import Workout, Exercise , ExerciseWorkout, Set
from .forms import CreateWorkoutForm
from django.contrib import messages
from django.db import transaction
from datetime import timedelta

# Create your views here.

def workout_view(request):
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'gymtracker/routines.html', {'workouts': workouts})


def create_workout(request):
    try:
        if request.method == 'POST':
            form = CreateWorkoutForm(request.POST)
            if form.is_valid():
                with transaction.atomic():  # Inicia la transacción
                    # Guardar el entrenamiento
                    workout = form.save(commit=False)
                    workout.user = request.user
                    workout.save()

                    # Manejar los ejercicios seleccionados
                    exercise_ids = request.POST.getlist('ejercicios[]')  # IDs de los ejercicios seleccionados
                    if not exercise_ids:
                        raise ValueError("You must select at least one exercise for the workout.")

                    exercises = Exercise.objects.filter(id__in=exercise_ids)

                    if not exercises.exists():
                        raise ValueError("The selected exercises do not exist.")

                    for order, exercise in enumerate(exercises, start=1):
                        exercise_workout = ExerciseWorkout.objects.create(
                        workout=workout,
                        exercise=exercise,
                        rest_time=timedelta(seconds=30),  # Ejemplo: 30 segundos de descanso por defecto
                        order=order
                        )

                    # Crear una serie por defecto
                        Set.objects.create(
                            workout_exercise=exercise_workout,
                            weight=0,
                            weight_unit='kg',
                            repetitions=0,
                            set_number=1  # Siempre 1 por defecto
                        )
                    messages.success(request, 'Workout created successfully.')
                    return redirect('workouts')
            else:
                messages.error(request, 'Error creating your workout. Please check the form.')

        # Si no es POST, inicializa el formulario
        form = CreateWorkoutForm()
        exercises = Exercise.objects.all()
        muscles = Exercise.objects.values_list('primary_muscle', flat=True).distinct()

        return render(request, 'gymtracker/create_workout.html', {
            'form': form,
            'exercises': exercises,  # Pasar ejercicios al template
            'muscles': muscles,  # Pasar los filtros dinámicos
        })
    except ValueError as e:
        # Error personalizado
        messages.error(request, str(e))
        return redirect('workouts')
    except Exception as e:
        # Manejo genérico de errores
        messages.error(request, 'An unexpected error occurred. Please try again.')
        return redirect('workouts')
    

def workout_detail(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    return render(request, 'gymtracker/workout_detail.html', {'workout': workout})