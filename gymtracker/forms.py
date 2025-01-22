from django import forms
from .models import Workout, Set


class CreateWorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name']

class SetForm(forms.Form):
    weight = forms.FloatField()
    weight_unit = forms.ChoiceField(choices=Set.WEIGHT_UNITS)
    repetitions = forms.IntegerField()
    set_number = forms.IntegerField()
    workout_exercise_id = forms.IntegerField(widget=forms.HiddenInput())  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['weight'].label = 'Weight (kg)'
        self.fields['repetitions'].label = 'Repetitions'
        self.fields['set_number'].label = 'Set Number'
        self.fields['workout_exercise_id'].widget.attrs.update({'class': 'workout-exercise-id'})  
        self.fields['workout_exercise_id'].widget.attrs.update({'readonly': 'readonly'}) 
        self.fields['workout_exercise_id'].widget.attrs.update({'style': 'display:none'}) 

    def clean(self):
        cleaned_data = super().clean()
        weight = cleaned_data.get('weight')
        repetitions = cleaned_data.get('repetitions')

        if weight <= 0:
            self.add_error('weight', 'Weight must be greater than 0.')
        if repetitions <= 0:
            self.add_error('repetitions', 'Repetitions must be greater than 0.')
        return cleaned_data
    
class ExerciseWorkoutForm(forms.Form):
    exercise_id = forms.IntegerField(widget=forms.HiddenInput())
    rest_time = forms.DurationField()
    order = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exercise_id'].widget.attrs.update({'class': 'exercise-id'})