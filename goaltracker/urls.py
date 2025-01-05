from django.urls import path
from . import views


urlpatterns = [
    path('goals/', views.goals_view, name='goals'),
    path('goals/create', views.create_goal, name='create_goal'),
    path('goals/<int:goal_id>/', views.goal_detail, name='goal_detail'),
    path('goals/<int:goal_id>/objectives/create', views.create_objective, name='create_objective'),
]