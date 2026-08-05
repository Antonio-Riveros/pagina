import urllib.parse
import urllib.request
from django.db import models
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from projects.models import Project

class Video(models.Model):
    proyecto = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="videos", verbose_name=_("Proyecto"))
    titulo = models.CharField(_("Título"), max_length=200)
    youtube_url = models.URLField(_("URL de YouTube"))
    youtube_id = models.CharField(_("ID de YouTube"), max_length=20, blank=True, help_text="Se extrae automáticamente de la URL.")
    miniatura = models.ImageField(_("Miniatura"), upload_to="videos/thumbnails/", blank=True, null=True, help_text="Se descarga automáticamente de YouTube.")
    descripcion = models.TextField(_("Descripción"), blank=True)
    
    orden = models.PositiveIntegerField(_("Orden"), default=0)
    destacado = models.BooleanField(_("Destacado"), default=False)
    publicado = models.BooleanField(_("Publicado"), default=True)

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")
        ordering = ['orden', '-id']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        # Extract YouTube ID
        if self.youtube_url:
            parsed_url = urllib.parse.urlparse(self.youtube_url)
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
                query = urllib.parse.parse_qs(parsed_url.query)
                self.youtube_id = query.get('v', [''])[0]
            elif parsed_url.hostname == 'youtu.be':
                self.youtube_id = parsed_url.path[1:]

        # Fetch thumbnail if not exists and we have youtube_id
        if self.youtube_id and not self.miniatura:
            thumbnail_url = f"https://img.youtube.com/vi/{self.youtube_id}/maxresdefault.jpg"
            try:
                result = urllib.request.urlretrieve(thumbnail_url)
                self.miniatura.save(
                    f"{self.youtube_id}.jpg",
                    ContentFile(open(result[0], 'rb').read()),
                    save=False
                )
            except Exception as e:
                # Fallback to hqdefault if maxresdefault doesn't exist
                try:
                    thumbnail_url = f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg"
                    result = urllib.request.urlretrieve(thumbnail_url)
                    self.miniatura.save(
                        f"{self.youtube_id}.jpg",
                        ContentFile(open(result[0], 'rb').read()),
                        save=False
                    )
                except Exception:
                    pass

        super().save(*args, **kwargs)
