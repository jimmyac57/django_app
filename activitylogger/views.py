from django.shortcuts import render
from .forms import ActivityForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import TimeLogger
from django.utils import timezone


# Create your views here.

def activityLogger(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        print(form)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            messages.success(request, 'activitylog created successfully')
            return redirect('activity_logger')
        else:
            messages.error(request, 'Error creating your activitylog')
    else:
        activity = TimeLogger.objects.filter(user=request.user, time_end__isnull=True)
        form = ActivityForm()
    return render(request, 'activitylogger.html', {'form': form, 'activity': activity})

def endActivity(request, id):
    if request.method == 'POST':
        activity = get_object_or_404(TimeLogger, id=id, user=request.user)
        activity.time_end = timezone.now() 
        print("se esta terminando la actividad",activity.time_end) 
        activity.save()
        messages.success(request, f"La actividad '{activity.activity}' ha sido finalizada.")
        return redirect('activity_logger')  
    else:
        messages.error(request, "Método no permitido.")
        return redirect('activity_logger')
