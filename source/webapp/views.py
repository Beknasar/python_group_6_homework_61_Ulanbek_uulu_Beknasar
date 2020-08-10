from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Tasks
from django.views.generic import View, TemplateView

from django.http import HttpResponseNotAllowed
from .forms import TaskForm

class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tasks']=Tasks.objects.all()

        search = self.request.GET.get('search')
        if search:
            context['tasks'] = Tasks.objects.filter(summary__icontains=search)
        return context


class TaskView(TemplateView):
    template_name = 'task_view.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        task = get_object_or_404(Tasks, pk=pk)

        context['task'] = task
        return context

class TaskCreateView(View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'task_create.html', context={
            'form': form
        })
    def post(self, request):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            data= {}
            for key, value in form.cleaned_data.items():
                if value is not None:
                    data[key] = value
            task=Tasks.objects.create(**data)
            return redirect('task_view', pk=task.pk)
        else:
            return render(request, 'task_create.html', context={
                'form': form
            })

class UpdateView(TemplateView):
    template_name = 'task_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        task = get_object_or_404(Tasks, pk=pk)

        initial = {}
        for key in 'summary', 'description', 'type', 'status':
            initial[key] = getattr(task, key)
        form = TaskForm(initial=initial)
        context['task'] = task
        context['form'] = form
        return context

    def post(self, request, pk):
       form = TaskForm(data=request.POST)
       task = get_object_or_404(Tasks, pk=pk)
       if form.is_valid():
            for key, value in form.cleaned_data.items():
                if value is not None:
                    setattr(task, key, value)
            task.save()
            return redirect('task_view', pk=task.pk)
       else:
            return self.render_to_response(context={
                'task': task,
                'form': form
            })


class DeleteView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        task = get_object_or_404(Tasks, pk=pk)
        return render(request, 'task_delete.html', context={'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Tasks, pk=pk)
        task.delete()
        return redirect('index')