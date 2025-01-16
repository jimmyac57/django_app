import django.forms as forms
from .models import TimeLogger

class ActivityForm(forms.ModelForm):
    class Meta:
        model = TimeLogger
        fields = ['activity']
        widgets = {
            'activity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter activity name'}),
        }