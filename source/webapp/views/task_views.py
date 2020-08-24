from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from webapp.models import Tasks, Project
from django.views.generic import View, TemplateView, FormView, ListView, CreateView

from webapp.forms import TaskForm, SearchForm
from django.db.models import Q, F


class TaskListView(ListView):
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10
    paginate_orphans = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        form = SearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            kwargs['search'] = search
        kwargs['form'] = form
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        data = Tasks.objects.all()

        form = SearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(summary__icontains=search) | Q(description__icontains=search))

        return data.order_by('-task_create')


class TaskView(TemplateView):
    template_name = 'task/task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        task = get_object_or_404(Tasks, pk=pk)

        context['task'] = task
        return context


class TaskCreateView(CreateView):
    template_name = 'task/task_create.html'
    form_class = TaskForm
    model = Tasks

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        task.save()
        return redirect('project_view', pk=project.pk)


class UpdateView(FormView):
    template_name = 'task/task_update.html'
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
        return render(request, 'task/task_delete.html', context={'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Tasks, pk=pk)
        task.delete()
        return redirect('index')