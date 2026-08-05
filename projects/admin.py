from django.contrib import admin
from django.utils.html import mark_safe
from .models import Category, Technology, Project, Capture
from videos.models import Video

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'orden')
    list_editable = ('orden',)
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'icono_preview', 'color', 'orden')
    list_editable = ('color', 'orden')
    search_fields = ('nombre',)
    
    def icono_preview(self, obj):
        if obj.icono:
            if obj.icono.startswith('<svg'):
                return mark_safe(f'<div style="width: 24px; height: 24px;">{obj.icono}</div>')
            return mark_safe(f'<i class="{obj.icono}" style="font-size: 24px; color: {obj.color or "#000"};"></i>')
        return "-"
    icono_preview.short_description = "Ícono"

class CaptureInline(admin.TabularInline):
    model = Capture
    extra = 1
    fields = ('titulo', 'imagen', 'imagen_preview', 'orden')
    readonly_fields = ('imagen_preview',)
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" style="max-height: 100px; border-radius: 4px;" />')
        return "-"
    imagen_preview.short_description = "Preview"

class VideoInline(admin.StackedInline):
    model = Video
    extra = 1
    fields = ('titulo', 'youtube_url', 'miniatura_preview', 'orden', 'destacado', 'publicado')
    readonly_fields = ('miniatura_preview',)
    
    def miniatura_preview(self, obj):
        if obj.miniatura:
            return mark_safe(f'<img src="{obj.miniatura.url}" style="max-height: 100px; border-radius: 4px;" />')
        return "-"
    miniatura_preview.short_description = "Miniatura"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'imagen_preview', 'estado', 'destacado', 'publicado', 'orden')
    list_editable = ('estado', 'destacado', 'publicado', 'orden')
    list_filter = ('estado', 'destacado', 'publicado', 'categorias', 'tecnologias')
    search_fields = ('titulo', 'resumen', 'descripcion_larga')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [CaptureInline, VideoInline]
    filter_horizontal = ('categorias', 'tecnologias')
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('titulo', 'slug', 'resumen', 'descripcion_larga')
        }),
        ('Multimedia', {
            'fields': ('imagen_principal', 'logo')
        }),
        ('Configuración y Estado', {
            'fields': ('estado', 'destacado', 'publicado', 'orden')
        }),
        ('Enlaces', {
            'fields': ('url_demo', 'url_github', 'url_cliente')
        }),
        ('Relaciones', {
            'fields': ('categorias', 'tecnologias')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )

    def imagen_preview(self, obj):
        if obj.imagen_principal:
            return mark_safe(f'<img src="{obj.imagen_principal.url}" style="max-height: 50px; border-radius: 4px;" />')
        return "-"
    imagen_preview.short_description = "Imagen"
