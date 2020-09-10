from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy

from webapp.models import Project
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from webapp.forms import SearchForm, ProjectForm, ProjectUpdateForm
from django.db.models import Q


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

        form = SearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(name__icontains=search) | Q(description__icontains=search))

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


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'project/project_create.html'
    form_class = ProjectForm
    model = Project
    permission_required = 'webapp.add_project'

    def form_valid(self, form):
        form.save()
        form.instance.author.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'project/project_update.html'
    form_class = ProjectForm
    model = Project
    context_object_name = 'project'
    permission_required = 'webapp.change_project'

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'project/project_delete.html'
    model = Project
    success_url = reverse_lazy('index')
    permission_required = 'webapp.delete_project'


class ProjectPermissonUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'project/user_edit.html'
    form_class = ProjectUpdateForm
    model = Project
    context_object_name = 'project'
    permission_required = 'webapp.change_project'

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})