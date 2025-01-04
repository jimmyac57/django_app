from django.contrib import admin
from .models import Rutina
from .models import Ejercicio
from .models import EjercicioRutina
# Register your models here.

admin.site.register(Rutina)
admin.site.register(Ejercicio)
admin.site.register(EjercicioRutina)
