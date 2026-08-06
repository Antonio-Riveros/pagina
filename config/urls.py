from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('proyectos/', include('projects.urls')),
    path('videos/', include('videos.urls')),
    path('contacto/', include('contact.urls')),
    path('panel/', include('panel.urls')),
    path('ccd2/', RedirectView.as_view(url='/panel/login/')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
