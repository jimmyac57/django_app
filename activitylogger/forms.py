import django.forms as forms
from .models import TimeLogger

class ActivityForm(forms.ModelForm):
    class Meta:
        model = TimeLogger
        fields = ['activity']