from django.shortcuts import get_object_or_404, redirect, render
from .forms import GoalForm, ObjectiveForm, ProgressForm
from .models import Goal, Objective, ProgressRecord
from django.contrib import messages

# Create your views here.

def goals_view(request):
    goals=Goal.objects.filter(user=request.user)
    return render(request, 'goaltracker/goals.html',{'goals':goals})

def create_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal created successfully')
            return redirect('goals')
        else:
            messages.error(request, 'Error creating your Goal')
    form=GoalForm()
    return render(request, 'goaltracker/create_goal.html',{'form':form})

def goal_detail(request,goal_id):
    goal = get_object_or_404(Goal, pk=goal_id, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goal updated successfully')
            return redirect('goals')
        else:
            messages.error(request, 'Error updating your Goal')
        
    else:
        form=GoalForm(instance=goal)

    return render(request, 'goaltracker/goal_detail.html', {'form': form , 'goal': goal})
    