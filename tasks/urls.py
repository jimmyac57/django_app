from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasks, name='tasks'),
    path('completed/', views.tasksCompleted, name='tasks_completed'),
    path('create/', views.createTasks, name='create_task'),
    path('<int:task_id>/', views.taskDetail, name='task_detail'),
    path('<int:task_id>/complete/', views.completeTask, name='complete_task'),
    path('<int:task_id>/detele/', views.deleteTask, name='delete_task'),
]
