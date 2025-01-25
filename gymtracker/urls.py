from django.urls import path
from . import views


urlpatterns = [
    path('workouts/', views.workout_view, name='workouts'),
    path('workouts/create/', views.create_workout, name='create_workout'),
    path('workouts/detail/<int:workout_id>/', views.workout_detail, name='workout_detail'),
    path('update_exercises/', views.update_exercises, name='update_exercises'),
]
