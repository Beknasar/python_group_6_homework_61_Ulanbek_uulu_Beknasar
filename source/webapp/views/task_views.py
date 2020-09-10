from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

from webapp.models import Tasks, Project
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from webapp.forms import TaskForm, SearchForm
from django.db.models import Q


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


class TaskCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'task/task_create.html'
    form_class = TaskForm
    model = Tasks
    permission_required = 'webapp.add_tasks'

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m()
        return redirect('project_view', pk=project.pk)

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().has_permission() and self.request.user in project.author.all()


class TaskUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'task/task_update.html'
    form_class = TaskForm
    model = Tasks
    context_object_name = 'task'
    permission_required = 'webapp.change_tasks'

    def has_permission(self):
        task = self.get_object()
        return super().has_permission() and self.request.user in task.project.author.all()

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.object.pk})


class TaskDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'task/task_delete.html'
    permission_required = 'webapp.delete_tasks'
    model = Tasks
    success_url = reverse_lazy('index')

    def has_permission(self):
        task = self.get_object()
        return super().has_permission() and self.request.user in task.project.author.all()
