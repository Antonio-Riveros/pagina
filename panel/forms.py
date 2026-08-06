from django import forms
from projects.models import Project
from core.models import HomePageConfig

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'titulo', 'slug', 'descripcion_corta', 'descripcion_larga',
            'youtube_url', 'miniatura_youtube', 'imagen_portada', 'estado', 'estado_publicacion',
            'destacado', 'url_demo', 'url_github', 'url_cliente',
            'categorias', 'tecnologias', 'orden', 'meta_title', 'meta_description'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Mi Super Proyecto'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mi-super-proyecto'}),
            'descripcion_corta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'descripcion_larga': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'youtube_url': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Pega aquí el <iframe...> o el enlace https://youtu.be/...'}),
            'miniatura_youtube': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'imagen_portada': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'estado_publicacion': forms.Select(attrs={'class': 'form-control'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'url_demo': forms.URLInput(attrs={'class': 'form-control'}),
            'url_github': forms.URLInput(attrs={'class': 'form-control'}),
            'url_cliente': forms.URLInput(attrs={'class': 'form-control'}),
            'categorias': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox-list'}),
            'tecnologias': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox-list'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control'}),
        }

class HomePageConfigForm(forms.ModelForm):
    class Meta:
        model = HomePageConfig
        fields = ['titulo_principal', 'subtitulo_destacado', 'descripcion', 'imagen_hero']
        widgets = {
            'titulo_principal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Construyendo el futuro'}),
            'subtitulo_destacado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. línea por línea_'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Breve descripción de los servicios...'}),
            'imagen_hero': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
