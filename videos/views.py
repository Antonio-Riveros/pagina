from django.shortcuts import render
from django.db.models import Q
from .models import Video
from projects.models import Category

def video_library(request):
    videos = Video.objects.filter(publicado=True)
    query = request.GET.get('q', '')
    category_slug = request.GET.get('categoria', '')
    
    if query:
        videos = videos.filter(
            Q(titulo__icontains=query) | 
            Q(descripcion__icontains=query) |
            Q(proyecto__titulo__icontains=query)
        ).distinct()
        
    if category_slug:
        videos = videos.filter(proyecto__categorias__slug=category_slug).distinct()
        
    if request.htmx:
        return render(request, 'videos/partials/_video_list.html', {'videos': videos})
        
    categorias = Category.objects.all()
    
    return render(request, 'videos/library.html', {
        'videos': videos,
        'categorias': categorias,
        'current_category': category_slug,
        'query': query,
    })
