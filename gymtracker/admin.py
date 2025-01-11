from django.contrib import admin
from .models import Rutina
from .models import Ejercicio
from .models import EjercicioRutina
# Register your models here.

admin.site.register(Rutina)
@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'primary_muscle', 'secondary_muscle')
    list_filter = ('primary_muscle',)

admin.site.register(EjercicioRutina)
