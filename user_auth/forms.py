from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está registrado. Por favor, utiliza otro.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado. Por favor, utiliza otro.")
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errores = []

        if len(password1) < 8:
            errores.append("La contraseña debe tener al menos 8 caracteres.")

        if not any(char.isdigit() for char in password1):
            errores.append("La contraseña debe contener al menos un número.")

        if not any(char.isalpha() for char in password1):
            errores.append("La contraseña debe contener al menos una letra.")

        if not any(char.isupper() for char in password1):
            errores.append("La contraseña debe contener al menos una letra mayúscula.")

        if not any(char.islower() for char in password1):
            errores.append("La contraseña debe contener al menos una letra minúscula.")

        if not any(char in "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~" for char in password1):
            errores.append("La contraseña debe contener al menos un símbolo especial (!@#$%^&*...).")

        if any(char.isspace() for char in password1):
            errores.append("La contraseña no puede contener espacios.")

        if errores:
            raise forms.ValidationError(errores)

        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden. Por favor, verifica e inténtalo de nuevo.")
        
        return cleaned_data