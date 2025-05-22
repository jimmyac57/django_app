from django.shortcuts import render,redirect
from .forms import CustomRegisterForm,CustomLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido de nuevo {user.username}!")
            return redirect('home')
        # No hace falta capturear aquí con messages.error, porque form.non_field_errors
        # ya mostrará tu mensaje en español si falla la autenticación.
    else:
        form = CustomLoginForm(request=request)

    return render(request, 'login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)  # Pasar datos POST al formulario
        if form.is_valid():  # Validar el formulario
            user = form.save()  # Guardar el nuevo usuario en la base de datos
            messages.success(request, f"Cuenta creada exitosamente para {user.username}. ¡Ahora puedes iniciar sesión!")
            return redirect('login')  # Redirigir al login después del registro
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CustomRegisterForm()  # Crear formulario vacío para GET
    return render(request, 'register.html', {'form': form})


