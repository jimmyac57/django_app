from django.shortcuts import redirect, render
from .models import Rutina, Ejercicio
from .forms import CrearRutinaForm
from django.http import JsonResponse

# Create your views here.

def rutinas_view(request):
    rutinas = Rutina.objects.filter(usuario=request.user)
    return render(request, 'gymtracker/routines.html', {'rutinas': rutinas})

def crear_rutina(request):
    form = CrearRutinaForm()
    ejercicios = Ejercicio.objects.all()
    if request.method == 'POST':
        form = CrearRutinaForm(request.POST)
        if form.is_valid():
            rutina = form.save(commit=False)
            rutina.usuario = request.user
            print(form)
            return redirect('rutinas')
        else:
            return render(request, 'gymtracker/workout_create.html',{'form': form, 'ejercicios': ejercicios})
    else:
        return render(request, 'gymtracker/workout_create.html',{'form': form, 'ejercicios': ejercicios})
    

def get_exercises(request):
    exercises = Ejercicio.objects.values('id', 'nombre','descripcion','primary_muscle','secondary_muscle','ruta_imagen')
    data = list(exercises)
    return JsonResponse(data, safe=False)
    