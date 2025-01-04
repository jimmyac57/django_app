from django import forms
from .models import Rutina


class CrearRutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['nombre']