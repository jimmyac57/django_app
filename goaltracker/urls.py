from django.urls import path
from . import views


urlpatterns = [
    path('goals/', views.goals_view, name='goals'),
    path('goals/create', views.create_goal, name='create_goal'),
]