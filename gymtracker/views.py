from django.shortcuts import redirect, render, get_object_or_404
from .models import Workout, Exercise, ExerciseWorkout, Set
from .forms import CreateWorkoutForm
from django.contrib import messages
from django.db import transaction
from datetime import timedelta
import json
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

@login_required
def workout_view(request):
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'gymtracker/routines.html', {'workouts': workouts})

@login_required
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
                        Set.objects.create(
                            workout_exercise=exercise_workout,
                            weight=0,
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
        messages.error(request, f"Validation error: {e}")
        return redirect('workouts')
    except ValidationError as e:
        messages.error(request, f"Validation error: {', '.join(e.messages)}")
        return redirect('workouts')
    except IntegrityError as e:
        messages.error(request, "Database integrity error. Please try again.")
        return redirect('workouts')
    except Exception as e:
        if settings.DEBUG:
            import traceback
            messages.error(request, f"Unexpected error: {e} - {traceback.format_exc()}")
        else:
            messages.error(request, 'An unexpected error occurred. Please try again later.')
        return redirect('workouts')

@login_required
def workout_detail(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    exercises_with_forms = []

    for exercise_workout in workout.exercise_workouts.all():
        set_forms = []
        for set_instance in exercise_workout.sets.all():
            set_forms.append({
                'set_id': set_instance.id,
                'set_number': set_instance.set_number,
                'weight': set_instance.weight,
                'repetitions': set_instance.repetitions,
            })
        rest_time = (
            f"{exercise_workout.rest_time.seconds // 3600:02}:{(exercise_workout.rest_time.seconds % 3600) // 60:02}"
            if exercise_workout.rest_time else "00:00"
        )
        exercises_with_forms.append({
            'exercise_workout': exercise_workout,
            'set_forms': set_forms,
            'rest_time': rest_time,
        })

    return render(request, 'gymtracker/workout_detail.html', {
        'workout': workout,
        'exercises_with_forms': exercises_with_forms,
    })


@login_required
@csrf_exempt
def update_exercises(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            workout_id = data.get("workout_id")
            if not workout_id:
                return JsonResponse({"error": "Workout ID not provided."}, status=400)

            try:
                workout = Workout.objects.get(id=workout_id)
            except Workout.DoesNotExist:
                return JsonResponse({"error": "The workout does not exist."}, status=400)

            deleted_sets = data.get("deleted_sets", [])
            if deleted_sets:
                Set.objects.filter(id__in=deleted_sets).delete()

            for exercise_data in data["exercises"]:
                try:
                    exercise_workout = ExerciseWorkout.objects.get(id=exercise_data["exercise_id"])
                except ExerciseWorkout.DoesNotExist:
                    continue

                rest_time_str = exercise_data["rest_time"]
                if rest_time_str:
                    hours, minutes = map(int, rest_time_str.split(":"))
                    exercise_workout.rest_time = timedelta(hours=hours, minutes=minutes)
                else:
                    exercise_workout.rest_time = timedelta()

                exercise_workout.weight_unit = exercise_data["weight_unit"]
                exercise_workout.save()

                for set_data in exercise_data["sets"]:
                    set_id = set_data.get("id")
                    set_number = set_data.get("set_number")
                    if not set_number:
                        continue

                    weight = float(set_data["weight"])
                    if weight < 0:
                        raise ValueError(f"Weight for set {set_number} in exercise {exercise_workout.exercise.name} cannot be negative.")

                    if set_id:
                        try:
                            set_instance = Set.objects.get(id=set_id)
                            set_instance.weight = weight
                            set_instance.repetitions = set_data["reps"]
                            set_instance.set_number = set_number
                            set_instance.save()
                        except Set.DoesNotExist:
                            continue
                    else:
                        Set.objects.create(
                            workout_exercise=exercise_workout,
                            weight=weight,
                            repetitions=set_data["reps"],
                            set_number=set_number,
                        )

                remaining_sets = exercise_workout.sets.order_by("set_number")
                if remaining_sets.exists():
                    for index, set_instance in enumerate(remaining_sets, start=1):
                        set_instance.set_number = index
                        set_instance.save()
                else:
                    exercise_workout.delete()

            if not workout.exercise_workouts.exists():
                workout.delete()
                return JsonResponse({"message": "Workout deleted because it has no remaining exercises."}, status=200)

            return JsonResponse({"message": "Exercises and sets updated successfully"}, status=200)

        except ValueError as ve:
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred."}, status=400)
