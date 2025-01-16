from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import Task
from django.contrib import messages
from django.utils import timezone

# Create your views here.
def tasks(request):
    try:
        tasks = Task.objects.filter(user=request.user, complete__isnull=True)
        return render(request, 'tasks/tasks.html', {'tasks': tasks})
    except Exception as e:
        messages.error(request, f'Error loading tasks: {e}')
        return redirect('home')


def createTasks(request):
    try:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                tasks = form.save(commit=False)
                tasks.user = request.user
                tasks.save()
                messages.success(request, 'Task created successfully')
                return redirect('tasks')
            else:
                messages.error(request, 'Error creating your task. Please check the form and try again.')
        else:
            form = TaskForm()
        return render(request, 'tasks/createTask.html', {'form': form})
    except Exception as e:
        messages.error(request, f'Error creating task: {e}')
        return redirect('tasks')


def taskDetail(request, task_id):
    try:
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                messages.success(request, 'Task updated successfully')
                return redirect('tasks')
            else:
                messages.error(request, 'Error updating your task. Please check the form and try again.')
        else:
            form = TaskForm(instance=task)
        return render(request, 'tasks/taskDetail.html', {'form': form, 'task': task})
    except Exception as e:
        messages.error(request, f'Error loading task details: {e}')
        return redirect('tasks')


def completeTask(request, task_id):
    try:
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        if request.method == 'POST':
            task.complete = timezone.now()
            task.save()
            messages.success(request, 'Task marked as complete')
            return redirect('tasks')
    except Exception as e:
        messages.error(request, f'Error completing task: {e}')
        return redirect('tasks')


def deleteTask(request, task_id):
    try:
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        if request.method == 'POST':
            task.delete()
            messages.success(request, 'Task deleted successfully')
            return redirect('tasks')
    except Exception as e:
        messages.error(request, f'Error deleting task: {e}')
        return redirect('tasks')


def tasksCompleted(request):
    try:
        tasks = Task.objects.filter(user=request.user, complete__isnull=False)
        return render(request, 'tasks/tasks.html', {'tasks': tasks})
    except Exception as e:
        messages.error(request, f'Error loading completed tasks: {e}')
        return redirect('tasks')


def mark_incomplete(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        if task.complete:
            task.complete = None
            task.save()
            messages.success(request, 'Task marked as incomplete')
        return redirect('tasks')
    except Exception as e:
        messages.error(request, f'Error marking task as incomplete: {e}')
        return redirect('tasks')
