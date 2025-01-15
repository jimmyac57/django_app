from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import localtime, now
from .models import TimeLogger
from .forms import ActivityForm

# Vista principal para gestionar actividades
def activityLogger(request):
    try:
        if request.method == 'POST':
            form = ActivityForm(request.POST)
            if form.is_valid():
                activity = form.save(commit=False)
                activity.user = request.user
                activity.save()

                # Depuración
                print("Hora guardada en UTC (time_start):", activity.time_start)
                print("Actividad creada:", activity.activity)

                messages.success(request, 'Activity log created successfully.')
                return redirect('activity_logger')
            else:
                messages.error(request, 'Error creating your activity log. Please check the form.')
        else:
            activities = TimeLogger.objects.filter(user=request.user, time_end__isnull=True)

            # Depuración
            print(f"Actividades activas encontradas: {activities.count()}")

            # Convertir `time_start` a la zona horaria local
            for activity in activities:
                activity.time_start = localtime(activity.time_start)
                print(f"Actividad: {activity.activity}, Hora local de inicio: {activity.time_start}")

            form = ActivityForm()
        return render(request, 'activitylogger.html', {'form': form, 'activity': activities})
    except Exception as e:
        # Depuración de errores
        print(f"Error en activityLogger: {e}")
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect('activity_logger')

# Vista para finalizar actividad
def endActivity(request, id):
    try:
        if request.method == 'POST':
            activity = get_object_or_404(TimeLogger, id=id, user=request.user)
            activity.time_end = now()  # Registrar hora de finalización en UTC
            activity_duration = localtime(activity.time_end) - localtime(activity.time_start)  # Duración en zona local

            # Depuración
            print("Hora de finalización en UTC (time_end):", activity.time_end)
            print("Duración de la actividad:", activity_duration)
            print(f"Actividad finalizada: {activity.activity}")

            activity.save()
            messages.success(request, f"La actividad '{activity.activity}' ha sido finalizada. Duración: {activity_duration}.")
            return redirect('activity_logger')
        else:
            messages.error(request, "Método no permitido.")
            return redirect('activity_logger')
    except TimeLogger.DoesNotExist:
        # Depuración de errores específicos
        print(f"Error: La actividad con ID {id} no existe o no pertenece al usuario.")
        messages.error(request, "The activity does not exist or you do not have permission to access it.")
        return redirect('activity_logger')
    except Exception as e:
        # Depuración de errores generales
        print(f"Error en endActivity: {e}")
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect('activity_logger')
    
def currentHour(request):
    # Obtener la fecha actual en la zona horaria local
    current_hour= localtime(now()).strftime('%H:%M:%S')
    return JsonResponse({'current_hour': current_hour})
