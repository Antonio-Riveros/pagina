from django.shortcuts import render
from projects.models import Project, Technology
from videos.models import Video

def home(request):
    proyectos_destacados = Project.objects.filter(publicado=True, destacado=True)[:3]
    ultimos_videos = Video.objects.filter(publicado=True)[:4]
    
    stats = {
        'proyectos': Project.objects.filter(publicado=True).count(),
        'videos': Video.objects.filter(publicado=True).count(),
        'tecnologias': Technology.objects.count(),
    }
    
    tecnologias = Technology.objects.all()
    
    return render(request, 'pages/home.html', {
        'proyectos_destacados': proyectos_destacados,
        'ultimos_videos': ultimos_videos,
        'stats': stats,
        'tecnologias': tecnologias,
    })
