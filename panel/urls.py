from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    PanelDashboardView,
    PanelProjectListView,
    PanelProjectCreateView,
    PanelProjectCreateView,
    PanelProjectUpdateView,
    PanelProjectDeleteView,
    PanelLoginView,
    PanelHomeConfigView
)

app_name = 'panel'

urlpatterns = [
    path('login/', PanelLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/panel/login/'), name='logout'),
    path('', PanelDashboardView.as_view(), name='dashboard'),
    path('configuracion-inicio/', PanelHomeConfigView.as_view(), name='home_config'),
    path('proyectos/', PanelProjectListView.as_view(), name='project_list'),
    path('proyectos/nuevo/', PanelProjectCreateView.as_view(), name='project_create'),
    path('proyectos/<int:pk>/editar/', PanelProjectUpdateView.as_view(), name='project_update'),
    path('proyectos/<int:pk>/eliminar/', PanelProjectDeleteView.as_view(), name='project_delete'),
]
