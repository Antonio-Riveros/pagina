from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Project, Category, Technology

def project_list(request):
    proyectos = Project.objects.filter(publicado=True)
    query = request.GET.get('q', '')
    
    if query:
        proyectos = proyectos.filter(
            Q(titulo__icontains=query) | 
            Q(resumen__icontains=query) |
            Q(tecnologias__nombre__icontains=query) |
            Q(categorias__nombre__icontains=query)
        ).distinct()
        
    if request.htmx:
        return render(request, 'projects/partials/_project_list.html', {'proyectos': proyectos})
        
    return render(request, 'projects/list.html', {
        'proyectos': proyectos,
        'query': query,
    })

def project_detail(request, slug):
    proyecto = get_object_or_404(Project, slug=slug, publicado=True)
    return render(request, 'projects/detail.html', {'proyecto': proyecto})
