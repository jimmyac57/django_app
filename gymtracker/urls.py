from django.urls import path
from . import views


urlpatterns = [
    path('rutinas/', views.rutinas_view, name='rutinas'),
    path('rutina/crear/', views.crear_rutina, name='crear_rutina'),
    path('rutina/<int:id>/', views.detalle_rutina, name='detalle_rutina'),
    path('api/exercises/', views.get_exercises, name='get_exercises'),
]
