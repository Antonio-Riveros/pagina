from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from projects.models import Project
from videos.models import Video
from core.models import HomePageConfig
from .forms import ProjectForm, HomePageConfigForm

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class PanelLoginView(LoginView):
    template_name = 'panel/login.html'
    redirect_authenticated_user = True
    
class PanelDashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'panel/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_proyectos'] = Project.objects.count()
        context['proyectos_publicados'] = Project.objects.filter(estado_publicacion='publicado').count()
        context['proyectos_borrador'] = Project.objects.filter(estado_publicacion='borrador').count()
        return context

class PanelProjectListView(StaffRequiredMixin, ListView):
    model = Project
    template_name = 'panel/projects/list.html'
    context_object_name = 'proyectos'
    ordering = ['orden', '-fecha_creacion']

class PanelProjectCreateView(StaffRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'panel/projects/form.html'
    success_url = reverse_lazy('panel:project_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Proyecto'
        return context

class PanelProjectUpdateView(StaffRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'panel/projects/form.html'
    success_url = reverse_lazy('panel:project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Proyecto'
        return context

class PanelProjectDeleteView(StaffRequiredMixin, DeleteView):
    model = Project
    template_name = 'panel/projects/delete.html'
    success_url = reverse_lazy('panel:project_list')

class PanelHomeConfigView(StaffRequiredMixin, UpdateView):
    model = HomePageConfig
    form_class = HomePageConfigForm
    template_name = 'panel/home_config.html'
    success_url = reverse_lazy('panel:dashboard')

    def get_object(self, queryset=None):
        return HomePageConfig.get_solo()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Configuración de Inicio'
        return context
