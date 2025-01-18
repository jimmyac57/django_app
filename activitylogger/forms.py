import django.forms as forms
from .models import TimeLogger, Activity

class TimeLoggerForm(forms.ModelForm):
    class Meta:
        model = TimeLogger
        fields = ['activity']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['activity'].queryset = Activity.objects.filter(user=user)
        else:
            
            self.fields['activity'].queryset = Activity.objects.none()

    
        self.fields['activity'].empty_label = "Seleccione una actividad"

    def clean_activity(self):
        activity = self.cleaned_data.get('activity')
        if not activity:  
            raise forms.ValidationError("Debe seleccionar una actividad válida.")
        return activity




class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name']