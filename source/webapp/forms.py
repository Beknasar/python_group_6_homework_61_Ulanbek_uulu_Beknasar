from django import forms
from django.core.exceptions import ValidationError

from .models import Status, Type, Tasks

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['summary', 'description', 'status', 'types']
        widgets = {'types': forms.CheckboxSelectMultiple}

    def clean(self):
        cleaned_data = super().clean()
        summary = cleaned_data.get('summary')
        description = cleaned_data.get('description')
        if summary and description and summary == description:
            raise ValidationError("Text of task should not dublicate it is title!")
        return cleaned_data