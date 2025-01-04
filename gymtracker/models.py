from django.db import models
from django.contrib.auth.models import User

class Rutina(models.Model):
    nombre = models.CharField(max_length=100)  
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    ejercicios = models.ManyToManyField('Ejercicio', through='EjercicioRutina')

# Ejercicios individuales que se pueden agregar a una rutina
class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100)  
    descripcion = models.TextField(null=True, blank=True)
    ruta_imagen= models.CharField(max_length=200, null=True, blank=True)
    primary_muscle = models.CharField(max_length=100, null=True, blank=True)
    secondary_muscle = models.CharField(max_length=100, null=True, blank=True)

# Ejercicios pertenecientes a una rutina
class EjercicioRutina(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)  
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE,null=True, blank=True)  
    orden = models.PositiveIntegerField()
    class Meta:
        verbose_name = "Ejercicio Rutina" 
        verbose_name_plural = "Ejercicios Rutinas"  

# Series de un ejercicio perteneciente a una rutina
class Serie(models.Model):
    UNIDADES_PESO = [
        ('kg', 'Kilogramos'),
        ('lb', 'Libras'),
    ]

    ejercicio_rutina = models.ForeignKey(
        'EjercicioRutina', 
        on_delete=models.CASCADE, 
        related_name="serie"
    ) 
    peso = models.FloatField()
    unidad_peso = models.CharField(max_length=2, choices=UNIDADES_PESO, default='kg')  # Opciones limitadas
    repeticiones = models.PositiveIntegerField()
    numero_serie = models.PositiveIntegerField()
    tiempo_descanso = models.DurationField() 

