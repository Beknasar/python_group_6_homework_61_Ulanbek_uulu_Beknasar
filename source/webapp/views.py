from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from webapp.models import Tasks, Project
from django.views.generic import View, TemplateView, FormView, ListView, DetailView, CreateView

from django.http import HttpResponseNotAllowed
from .forms import TaskForm, SearchForm, ProjectForm
from django.db.models import Q, F


class IndexView(ListView):
    template_name = 'project/index.html'
    context_object_name = 'projects'
    paginate_by = 5
    paginate_orphans = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        form = SearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            kwargs['search'] = search
        kwargs['form'] = form
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        data = Project.objects.all()

        # form = SearchForm(data=self.request.GET)
        # if form.is_valid():
        #     search = form.cleaned_data['search']
        #     if search:
        #         data = data.filter(Q(summary__icontains=search) | Q(description__icontains=search))

        return data.order_by('-date_start')


class ProjectView(DetailView):
    template_name = 'project/project_view.html'
    model = Project
    paginate_tasks_by = 5
    paginate_tasks_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks, page, is_paginated = self.paginate_tasks(self.object)
        context['tasks'] = tasks
        context['page_obj'] = page
        context['is_paginated'] = is_paginated

        return context

    def paginate_tasks(self, project):
        tasks = project.tasks.all().order_by('-task_create')
        if tasks.count() > 0:
            paginator = Paginator(tasks, self.paginate_tasks_by, orphans=self.paginate_tasks_orphans)
            page_number = self.request.GET.get('page', 1)
            page = paginator.get_page(page_number)
            is_paginated = paginator.num_pages > 1  # page.has_other_pages()
            return page.object_list, page, is_paginated
        else:
            return tasks, None, False


class ProjectCreateView(CreateView):
    template_name = 'project/project_create.html'
    form_class = ProjectForm
    model = Project

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class TaskView(TemplateView):
    template_name = 'task/task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        task = get_object_or_404(Tasks, pk=pk)

        context['task'] = task
        return context


class TaskCreateView(FormView):
    template_name = 'task/task_create.html'
    form_class = TaskForm

    def form_valid(self, form):
        self.task = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.task.pk})


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