from django import forms
from .models import Status, Type, Tasks

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['summary', 'description', 'status', 'types']
        widgets = {'types': forms.CheckboxSelectMultiple}
