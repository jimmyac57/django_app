from django.urls import path
from . import views


urlpatterns = [
    path('rutinas/', views.rutinas_view, name='rutinas'),
    path('workout/create/', views.crear_rutina, name='crear_rutina'),
    path('api/exercises/', views.get_exercises, name='get_exercises'),
]
