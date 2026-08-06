from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Category, Technology, Project, Capture

@admin.action(description="Publicar proyectos seleccionados")
def make_published(modeladmin, request, queryset):
    queryset.update(estado_publicacion='publicado')

@admin.action(description="Pasar a borrador seleccionados")
def make_draft(modeladmin, request, queryset):
    queryset.update(estado_publicacion='borrador')

@admin.action(description="Destacar seleccionados")
def make_featured(modeladmin, request, queryset):
    queryset.update(destacado=True)

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

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('orden', 'titulo', 'estado', 'estado_publicacion', 'destacado', 'portada_preview', 'ver_en_sitio')
    list_editable = ('estado', 'estado_publicacion', 'destacado', 'orden')
    list_display_links = ('titulo', 'portada_preview')
    list_filter = ('estado_publicacion', 'estado', 'destacado', 'categorias')
    search_fields = ('titulo', 'descripcion_corta', 'youtube_id')
    prepopulated_fields = {'slug': ('titulo',)}
    readonly_fields = ('portada_preview', 'youtube_id', 'youtube_preview', 'fecha_actualizacion')
    inlines = [CaptureInline]
    filter_horizontal = ('categorias', 'tecnologias')
    ordering = ('orden', '-fecha_creacion')
    actions = [make_published, make_draft, make_featured]
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('titulo', 'slug', 'descripcion_corta', 'descripcion_larga')
        }),
        ('Multimedia', {
            'fields': ('imagen_portada', 'portada_preview')
        }),
        ('Integración YouTube', {
            'description': 'Solo pega el enlace. El ID, la miniatura y el reproductor se generan automáticamente al guardar.',
            'fields': ('youtube_url', 'youtube_id', 'youtube_preview', 'miniatura_youtube')
        }),
        ('Estado y Configuración', {
            'fields': ('estado', 'estado_publicacion', 'destacado', 'orden', 'fecha_creacion')
        }),
        ('Enlaces Externos', {
            'fields': ('url_demo', 'url_github', 'url_cliente')
        }),
        ('Clasificación', {
            'fields': ('categorias', 'tecnologias')
        }),
        ('SEO (Opcional)', {
            'classes': ('collapse',),
            'description': 'Si lo dejas en blanco, se generarán automáticamente a partir del título y la descripción.',
            'fields': ('meta_title', 'meta_description')
        }),
    )

    def portada_preview(self, obj):
        if obj.imagen_portada:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 4px;" />', obj.imagen_portada.url)
        return "-"
    portada_preview.short_description = "Portada"
    
    def youtube_preview(self, obj):
        if obj.miniatura_youtube:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height: 100px; border-radius: 8px; border: 2px solid #e5e7eb;" /></a>',
                obj.youtube_url, obj.miniatura_youtube.url
            )
        return "No hay video asociado."
    youtube_preview.short_description = "Miniatura YouTube"
    
    def ver_en_sitio(self, obj):
        if obj.pk:
            return format_html(
                '<a class="button" href="/proyectos/{}" target="_blank">Ver <i class="fa-solid fa-arrow-up-right-from-square"></i></a>',
                obj.slug
            )
        return "-"
    ver_en_sitio.short_description = "Acción"
