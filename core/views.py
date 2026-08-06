from django.shortcuts import render
from projects.models import Project, Technology
from videos.models import Video
from core.models import HomePageConfig

def home(request):
    proyectos_destacados = Project.objects.filter(estado_publicacion='publicado', destacado=True).prefetch_related('tecnologias').order_by('orden')[:3]
    ultimos_videos = Video.objects.filter(publicado=True)[:4]
    
    stats = {
        'proyectos': Project.objects.filter(estado_publicacion='publicado').count(),
        'videos': Video.objects.filter(publicado=True).count(),
        'tecnologias': Technology.objects.count(),
    }
    
    tecnologias = Technology.objects.all()
    config = HomePageConfig.get_solo()
    
    return render(request, 'pages/home.html', {
        'proyectos_destacados': proyectos_destacados,
        'ultimos_videos': ultimos_videos,
        'stats': stats,
        'tecnologias': tecnologias,
        'config': config,
    })
