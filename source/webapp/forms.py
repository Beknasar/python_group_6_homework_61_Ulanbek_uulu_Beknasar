from django import forms
# from .models import STATUS_CHOICES
#
# default_status = STATUS_CHOICES[0][0]

class TaskForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label='Название')
    description = forms.CharField(max_length=500, required=True, label='Описание', widget=forms.Textarea)
    #status = forms.ChoiceField(choices=STATUS_CHOICES, required=True, label='Статус',
                               #initial=default_status)
    task_deadline = forms.DateTimeField(required=False, label='Дата выполнения', widget=forms.DateInput(attrs={'type': 'date'}))

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)