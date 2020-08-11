from django import forms
from .models import Status, Type
#
# default_status = STATUS_CHOICES[0][0]

class TaskForm(forms.Form):
    summary = forms.CharField(max_length=200, required=True, label='Название')
    description = forms.CharField(max_length=2000, required=True, label='Описание', widget=forms.Textarea)
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    types = forms.ModelMultipleChoiceField(required=False, queryset=Type.objects.all(), widget=forms.CheckboxSelectMultiple, label='Типы')

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)