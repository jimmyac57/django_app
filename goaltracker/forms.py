from django import forms
from .models import Goal
from .models import Objective
from .models import ProgressRecord

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['desired_identity', 'desired_result', 'system', 'end_at']
        widgets = {
            'end_at': forms.DateInput(attrs={'type': 'date'}),
            'system': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }


class ObjectiveForm(forms.ModelForm):
    class Meta:
        model = Objective
        fields = ['name', 'type_period', 'value_by_period', 'unit_of_value', 'chart']

class ProgressForm(forms.ModelForm):
    class Meta:
        model = ProgressRecord
        fields = ['value', 'unit_of_value','record_date','notes']