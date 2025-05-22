# yourapp/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(
        label=_("Nombre de usuario"),
        widget=forms.TextInput(attrs={
            'autocomplete': 'username',
            'placeholder': _('ejemplo123'),
            'class': 'form-control'
        }),
        error_messages={
            'required': _('El nombre de usuario es obligatorio.'),
            'invalid': _('Nombre de usuario no válido.')
        }
    )
    email = forms.EmailField(
        label=_("Correo electrónico"),
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': _('tu@email.com'),
            'autocomplete': 'email',
            'class': 'form-control'
        }),
        error_messages={
            'required': _('El correo electrónico es obligatorio.'),
            'invalid': _('Correo electrónico no válido.')
        }
    )

    password1 = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(
            render_value=True,attrs={
            'placeholder': _('Mínimo 8 caracteres'),
            'autocomplete': 'new-password',
            'class': 'form-control'
        }),
        error_messages={
            'required': _('La contraseña es obligatoria.')
        }
    )
    password2 = forms.CharField(
        label=_("Confirmar contraseña"),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Repite tu contraseña'),
            'autocomplete': 'new-password',
            'class': 'form-control'
        }),
        error_messages={
            'required': _('Debes confirmar la contraseña.')
        }
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).exists():
            raise ValidationError(_("Este nombre de usuario ya está en uso."))
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Este correo electrónico ya está registrado."))
        return email

    # Ahora sí tu clean_password1 se ejecutará
    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        errores = []
        if len(password) < 8:
            errores.append("La contraseña debe tener al menos 8 caracteres.")
        if not any(c.isdigit() for c in password):
            errores.append("Debe contener al menos un número.")
        if not any(c.isupper() for c in password):
            errores.append("Debe incluir una letra mayúscula.")
        if not any(c in "!@#$%&*" for c in password):
            errores.append("Requiere al menos un símbolo (!@#$%&*).")
        if errores:
            raise ValidationError(errores)
        return password



class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Usuario"),
        widget=forms.TextInput(attrs={
            'autocomplete': 'username',
            'placeholder': _('Tu nombre de usuario'),
            'class': 'form-control',
            'id': 'id_username',
        }),
        error_messages={
            'required': _('Por favor ingresa tu nombre de usuario.'),
        }
    )

    # aquí el nombre debe seguir siendo `password`
    password = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(
            render_value=True,        
            attrs={
                'autocomplete': 'new-password',
                'placeholder': _('Tu contraseña'),
                'class': 'form-control',
                'id': 'id_password',
            }
        ),
        error_messages={
            'required': _('Por favor ingresa tu contraseña.'),
        }
    )

    error_messages = {
        'invalid_login': _("Credenciales inválidas. Verifica tus datos."),
        'inactive': _("Esta cuenta está desactivada."),
    }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(user)
            self.user_cache = user
        return cleaned_data
