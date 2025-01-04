from django.shortcuts import render
from .forms import GoalForm, ObjectiveForm, ProgressForm

# Create your views here.

def goals_view(request):
    return render(request, 'goaltracker/goals.html')

def create_goal(request):
    form=GoalForm()
    return render(request, 'goaltracker/create_goal.html',{'form':form})