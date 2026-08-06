from django.views.generic import ListView, DetailView
from .models import Project

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'proyectos'
    
    def get_queryset(self):
        # Usar prefetch_related para evitar el problema N+1 con tecnologías
        return Project.objects.filter(estado_publicacion='publicado').prefetch_related('tecnologias').order_by('orden', '-fecha_creacion')
        
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'proyecto'
    
    def get_queryset(self):
        return Project.objects.filter(estado_publicacion='publicado').prefetch_related('tecnologias', 'capturas')
