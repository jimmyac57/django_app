from django.shortcuts import redirect, render, get_object_or_404
from .models import Workout, Exercise , ExerciseWorkout, Set
from .forms import CreateWorkoutForm , SetForm , ExerciseWorkoutForm
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
                with transaction.atomic(): 
                    workout = form.save(commit=False)
                    workout.user = request.user
                    workout.save()

                    exercise_ids = request.POST.getlist('ejercicios[]')  
                    if not exercise_ids:
                        raise ValueError("You must select at least one exercise for the workout.")

                    exercises = Exercise.objects.filter(id__in=exercise_ids)

                    if not exercises.exists():
                        raise ValueError("The selected exercises do not exist.")

                    for order, exercise in enumerate(exercises, start=1):
                        exercise_workout = ExerciseWorkout.objects.create(
                        workout=workout,
                        exercise=exercise,
                        rest_time=timedelta(seconds=30), 
                        order=order
                        )

                    # Crear una serie por defecto
                        Set.objects.create(
                            workout_exercise=exercise_workout,
                            weight=0,
                            weight_unit='kg',
                            repetitions=0,
                            set_number=1  
                        )
                    messages.success(request, 'Workout created successfully.')
                    return redirect('workouts')
            else:
                messages.error(request, 'Error creating your workout. Please check the form.')

        form = CreateWorkoutForm()
        exercises = Exercise.objects.all()
        muscles = Exercise.objects.values_list('primary_muscle', flat=True).distinct()

        return render(request, 'gymtracker/create_workout.html', {
            'form': form,
            'exercises': exercises,  
            'muscles': muscles,  
        })
    except ValueError as e:
       
        messages.error(request, str(e))
        return redirect('workouts')
    except Exception as e:
       
        messages.error(request, 'An unexpected error occurred. Please try again.')
        return redirect('workouts')
    

def workout_detail(request, workout_id):
    workout = Workout.objects.get(id=workout_id)

   
    exercises_with_forms = []

    for exercise_workout in workout.exercise_workouts.all():
        set_forms = []
        for set_instance in exercise_workout.sets.all():
            form = SetForm(initial={
                'weight': set_instance.weight,
                'weight_unit': set_instance.weight_unit,
                'repetitions': set_instance.repetitions,
                'set_number': set_instance.set_number,
                'workout_exercise_id': exercise_workout.id,
            })
            set_forms.append({'form': form, 'set_id': set_instance.id})
        exercises_with_forms.append({'exercise_workout': exercise_workout, 'set_forms': set_forms})

    return render(request, 'gymtracker/workout_detail.html', {
        'workout': workout,
        'exercises_with_forms': exercises_with_forms,
    })

def update_set(request, set_id):
    set_instance = get_object_or_404(Set, id=set_id)
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            set_instance.weight = form.cleaned_data['weight']
            set_instance.weight_unit = form.cleaned_data['weight_unit']
            set_instance.repetitions = form.cleaned_data['repetitions']
            set_instance.set_number = form.cleaned_data['set_number']
            set_instance.save()
            messages.success(request, 'Set updated successfully.')
            return redirect('workout_detail', workout_id=set_instance.workout_exercise.workout.id)
        else:
            messages.error(request, 'There was an error updating the set. Please check the form.')
    else:
        form = SetForm(initial={
            'weight': set_instance.weight,
            'weight_unit': set_instance.weight_unit,
            'repetitions': set_instance.repetitions,
            'set_number': set_instance.set_number,
            'workout_exercise_id': set_instance.workout_exercise.id,
        })

    return render(request, 'gymtracker/update_set.html', {'form': form, 'set': set_instance})
