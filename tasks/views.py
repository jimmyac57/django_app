from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import Task
from django.contrib import messages
from django.utils import timezone

# Create your views here.
def tasks(request):
    tasks = Task.objects.filter(user=request.user , complete__isnull=True)
    return render(request, 'tasks/tasks.html', {'tasks': tasks})


def createTasks(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            tasks=form.save(commit=False)
            tasks.user = request.user
            form.save()
            messages.success(request, 'Task created successfully')
            return redirect('tasks')
        else:
            messages.error(request, 'Error creating your task')
    else:
        form = TaskForm()
        return render(request, 'tasks/createTask.html', {'form': form})
    
def taskDetail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully')
            return redirect('tasks')
        else:
            messages.error(request, 'Error updating your task')
        
    else:
        form=TaskForm(instance=task)

    return render(request, 'tasks/taskDetail.html', {'form': form , 'task': task})
    

def completeTask(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    print("Task object:", task)
    print("Task ID:", task.id)
    if request.method == 'POST':
        task.complete = timezone.now()
        task.save()
        return redirect('tasks')
    
def deleteTask(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    print("Task object:", task)
    print("Task ID:", task.id)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

def tasksCompleted(request):
    tasks = Task.objects.filter(user=request.user, complete__isnull=False)
    return render(request, 'tasks/tasks.html', {'tasks': tasks})