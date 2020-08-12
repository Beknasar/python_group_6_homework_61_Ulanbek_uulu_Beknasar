from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from webapp.models import Tasks
from django.views.generic import View, TemplateView, FormView

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

class TaskCreateView(FormView):
    template_name = 'task_create.html'
    form_class = TaskForm

    def form_valid(self, form):
        self.task = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.task.pk})

class UpdateView(FormView):
    template_name = 'task_update.html'
    form_class = TaskForm

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Tasks, pk=pk)

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.task
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        return context

    def form_valid(self, form):
        self.task = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.task.pk})

class DeleteView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        task = get_object_or_404(Tasks, pk=pk)
        return render(request, 'task_delete.html', context={'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Tasks, pk=pk)
        task.delete()
        return redirect('index')