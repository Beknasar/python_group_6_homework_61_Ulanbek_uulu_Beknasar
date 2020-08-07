from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Tasks
from django.views.generic import View, TemplateView

from django.http import HttpResponseNotAllowed
from .forms import TaskForm

class IndexView(View):
    def get(self, request, *args, **kwargs):
        data = Tasks.objects.all()
        return render(request, 'index.html', context={'tasks': data})

def task_view(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    context = {'task': task}
    return render(request, 'task_view.html', context)

def create_task_view(request):
    if request.method == 'GET':
        form = TaskForm()
        return render(request, 'task_create.html', context={
            'form': form
        })
    elif request.method == 'POST':
        #print(request.POST)
        form = TaskForm(data=request.POST)
        # date = request.POST.get('date')
        # if date == '':
        #     date = None
        if form.is_valid():
            task = Tasks.objects.create(
                title=form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                status = form.cleaned_data['status'],
                task_deadline = form.cleaned_data['task_deadline'])

            return redirect('task_view', pk=task.pk)
        else:
            return render(request, 'task_create.html', context={
                'form': form
            })
    else:
        return HttpResponseNotAllowed(
            permitted_methods=['GET', 'POST'])

def update_view(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    if request.method == "GET":
        form = TaskForm(initial={
            'title': task.title,
            'description': task.description,
            'task_deadline': task.task_deadline,
            'status': task.status
        })
        return render(request, 'task_update.html', context={
            'form': form,
            'task': task
        })
    elif request.method == "POST":
       form = TaskForm(data=request.POST)
       if form.is_valid():
            task.title = form.cleaned_data['title']
            task.description = form.cleaned_data['description']
            task.status = form.cleaned_data['status']
            task.task_deadline = form.cleaned_data['task_deadline']
            task.save()
            return redirect('task_view', pk=task.pk)
       else:
            return render(request, 'task_update.html', context={
                'task': task,
                'form': form
            })

    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])

def delete_view(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    if request.method == 'GET':
        return render(request, 'task_delete.html', context={'task': task})
    elif request.method == 'POST':
        task.delete()
        return redirect('index')