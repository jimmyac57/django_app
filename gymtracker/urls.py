from django.urls import path
from . import views


urlpatterns = [
    path('workouts/', views.workout_view, name='rutinas'),
    path('workouts/create/', views.create_workout, name='crear_rutina'),
]
