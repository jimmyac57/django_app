from django.shortcuts import redirect, render
from .models import Rutina, Ejercicio , EjercicioRutina
from .forms import CrearRutinaForm
from django.http import JsonResponse

# Create your views here.

def rutinas_view(request):
    rutinas = Rutina.objects.filter(usuario=request.user)
    return render(request, 'gymtracker/routines.html', {'rutinas': rutinas})

def crear_rutina(request):
    ejercicios = Ejercicio.objects.all()

    if request.method == 'POST':
        form = CrearRutinaForm(request.POST)

        # 1) Obtener la lista de ejercicios enviada
        ejercicios_ids = request.POST.getlist('ejercicios[]')  # ['1', '2', '3', ...]

        # 2) Validar que haya al menos un ejercicio
        if not ejercicios_ids:
            # Error: el usuario no envió ni un solo ejercicio
            return render(request, 'gymtracker/workout_create.html', {
                'form': form,
                'ejercicios': ejercicios,
                'error': 'Debes seleccionar al menos un ejercicio.'
            })

        # 3) Verificar que todos los IDs existan en la base de datos
        valid_exercises = Ejercicio.objects.filter(pk__in=ejercicios_ids)
        
        # Si la cantidad de ejercicios validos es menor a la cantidad que envió el usuario,
        # significa que hubo IDs inválidos
        if len(valid_exercises) < len(ejercicios_ids):
            return render(request, 'gymtracker/workout_create.html', {
                'form': form,
                'ejercicios': ejercicios,
                'error': 'Algunos ejercicios seleccionados no existen. Inténtalo de nuevo.'
            })

        # (Opcional) Exigir que los ejercicios válidos sean por lo menos 1
        if len(valid_exercises) == 0:
            return render(request, 'gymtracker/workout_create.html', {
                'form': form,
                'ejercicios': ejercicios,
                'error': 'Debes seleccionar al menos un ejercicio válido.'
            })

        # 4) Ahora que sabemos que el form y los ejercicios son "potencialmente válidos",
        #    validamos el form de la Rutina
        if form.is_valid():
            # 4a) Guardamos la rutina (sin crear otra, ojo)
            rutina = form.save(commit=False)
            rutina.usuario = request.user
            rutina.save()

            # 4b) Crear la relación en EjercicioRutina con el orden que prefieras
            for index, e_id in enumerate(ejercicios_ids, start=1):
                EjercicioRutina.objects.create(
                    rutina=rutina,
                    ejercicio_id=e_id,
                    orden=index
                )

            return redirect('rutinas')
        else:
            # Si el form no es válido (ejemplo: el campo nombre está vacío)
            return render(request, 'gymtracker/workout_create.html', {
                'form': form,
                'ejercicios': ejercicios
            })

    else:
        # GET: mostrar form vacío
        form = CrearRutinaForm()
        return render(request, 'gymtracker/workout_create.html', {
            'form': form,
            'ejercicios': ejercicios
        })
    
def detalle_rutina(request, id):
    rutina = Rutina.objects.get(pk=id)
    print(rutina.nombre)
    ejercicios = EjercicioRutina.objects.filter(rutina=rutina)
    print(ejercicios)
    return render(request, 'gymtracker/routines_details.html', {'rutina': rutina, 'ejercicios': ejercicios})

def get_exercises(request):
    exercises = Ejercicio.objects.values('id', 'nombre','descripcion','primary_muscle','secondary_muscle','ruta_imagen')
    data = list(exercises)
    return JsonResponse(data, safe=False)
    