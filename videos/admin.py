from django.contrib import admin
from django.utils.html import mark_safe
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'proyecto', 'miniatura_preview', 'destacado', 'publicado', 'orden')
    list_editable = ('destacado', 'publicado', 'orden')
    list_filter = ('destacado', 'publicado', 'proyecto')
    search_fields = ('titulo', 'descripcion', 'youtube_id')
    readonly_fields = ('youtube_id', 'miniatura_preview')

    def miniatura_preview(self, obj):
        if obj.miniatura:
            return mark_safe(f'<img src="{obj.miniatura.url}" style="max-height: 50px; border-radius: 4px;" />')
        return "-"
    miniatura_preview.short_description = "Miniatura"
