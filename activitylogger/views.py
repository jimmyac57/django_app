from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import localtime, now
from .models import TimeLogger
from .forms import ActivityForm

def activityLogger(request):
    try:
        if request.method == 'POST':
            form = ActivityForm(request.POST)
            if form.is_valid():
                activity = form.save(commit=False)
                activity.user = request.user
                activity.save()

                messages.success(request, 'Activity log created successfully.')
                return redirect('activity_logger')
            else:
                messages.error(request, 'Error creating your activity log. Please check the form.')
        else:
            activities = TimeLogger.objects.filter(user=request.user, time_end__isnull=True)

            for activity in activities:
                activity.time_start = localtime(activity.time_start)

            form = ActivityForm()
        return render(request, 'activitylogger.html', {'form': form, 'activity': activities})
    
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect('activity_logger')

def endActivity(request, id):
    try:
        if request.method == 'POST':
            activity = get_object_or_404(TimeLogger, id=id, user=request.user)
            activity.time_end = now() 
            activity_duration = localtime(activity.time_end) - localtime(activity.time_start) 
            activity.save()
            messages.success(request, f"La actividad '{activity.activity}' ha sido finalizada. Duración: {activity_duration}.")
            return redirect('activity_logger')
        else:
            messages.error(request, "Método no permitido.")
            return redirect('activity_logger')
        
    except TimeLogger.DoesNotExist:
        messages.error(request, "The activity does not exist or you do not have permission to access it.")
        return redirect('activity_logger')
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect('activity_logger')
    
def currentHour(request):
    current_dt = localtime(now())
    return JsonResponse({'current_hour': current_dt.isoformat()})

def finishedActivities(request):
    finished_activities = TimeLogger.objects.filter(user=request.user, time_end__isnull=False).order_by('-time_start')
    return render(request, 'finished_activities.html', {'activities': finished_activities})