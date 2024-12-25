from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasksCompleted, name='tasks_completed'),
    path('tasks/create/', views.createTasks, name='create_task'),
    path('tasks/<int:task_id>/', views.taskDetail, name='task_detail'),
    path('tasks/<int:task_id>/complete/', views.completeTask, name='complete_task'),
    path('tasks/<int:task_id>/detele/', views.deleteTask, name='delete_task'),
]
