import re
import urllib.request
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

class Category(models.Model):
    nombre = models.CharField(_("Nombre"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    orden = models.PositiveIntegerField(_("Orden"), default=0)

    class Meta:
        verbose_name = _("Categoría")
        verbose_name_plural = _("Categorías")
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre

class Technology(models.Model):
    nombre = models.CharField(_("Nombre"), max_length=100)
    icono = models.CharField(_("Ícono (SVG o Clase)"), max_length=1000, blank=True, help_text="Código SVG o clase CSS (ej. fa-brands fa-python)")
    color = models.CharField(_("Color"), max_length=50, blank=True, help_text="Color hex, ej. #3776AB")
    orden = models.PositiveIntegerField(_("Orden"), default=0)

    class Meta:
        verbose_name = _("Tecnología")
        verbose_name_plural = _("Tecnologías")
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre

class Project(models.Model):
    ESTADO_CHOICES = (
        ('en_desarrollo', 'En Desarrollo'),
        ('produccion', 'Producción'),
        ('finalizado', 'Finalizado'),
        ('pausado', 'Pausado'),
    )
    
    PUBLICACION_CHOICES = (
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
    )

    titulo = models.CharField(_("Título"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    descripcion_corta = models.TextField(_("Descripción Corta"), max_length=500)
    descripcion_larga = models.TextField(_("Descripción Larga"), blank=True)
    
    # YouTube Integration
    youtube_url = models.TextField(_("Enlace o Iframe de YouTube"), help_text="Requerido. Pega el enlace completo o el código <iframe> de YouTube. El sistema extraerá el video automáticamente.")
    youtube_id = models.CharField(_("ID de YouTube"), max_length=20, blank=True)
    miniatura_youtube = models.ImageField(_("Miniatura Automática de YouTube"), upload_to="projects/youtube_thumbs/", blank=True, null=True)
    
    imagen_portada = models.ImageField(_("Imagen Principal / Portada"), upload_to="projects/", blank=True, null=True)
    
    # Status
    estado = models.CharField(_("Estado"), max_length=50, choices=ESTADO_CHOICES, default='finalizado')
    estado_publicacion = models.CharField(_("Estado de Publicación"), max_length=50, choices=PUBLICACION_CHOICES, default='publicado')
    destacado = models.BooleanField(_("Destacado"), default=False, help_text="Marcar para mostrar en la página principal.")
    
    # URLs
    url_demo = models.URLField(_("URL Demo"), blank=True)
    url_github = models.URLField(_("URL GitHub"), blank=True)
    url_cliente = models.URLField(_("URL Cliente"), blank=True)
    
    # Relations
    categorias = models.ManyToManyField(Category, verbose_name=_("Categorías"), related_name="proyectos", blank=True)
    tecnologias = models.ManyToManyField(Technology, verbose_name=_("Tecnologías"), related_name="proyectos", blank=True)
    
    # Ordering & Timestamps
    orden = models.PositiveIntegerField(_("Orden"), default=0, help_text="Determina el orden visual en la página principal (ej. 1, 2, 3...)")
    fecha_creacion = models.DateField(_("Fecha de Creación"), blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # SEO
    meta_title = models.CharField(_("Meta Title"), max_length=60, blank=True)
    meta_description = models.CharField(_("Meta Description"), max_length=160, blank=True)

    class Meta:
        verbose_name = _("Proyecto")
        verbose_name_plural = _("Proyectos")
        ordering = ['orden', '-fecha_creacion']

    def __str__(self):
        return self.titulo
        
    @property
    def embed_url(self):
        if self.youtube_id:
            return f"https://www.youtube.com/embed/{self.youtube_id}?rel=0&playsinline=1&enablejsapi=1"
        return ""
        
    @property
    def iframe(self):
        if self.embed_url:
            return format_html(
                '<iframe id="yt-player-{}" width="100%" height="100%" src="{}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen webkitallowfullscreen mozallowfullscreen style="position: absolute; top: 0; left: 0;"></iframe>',
                self.id,
                self.embed_url
            )
        return ""
        
    @property
    def descripcion_formateada(self):
        text = self.descripcion_corta
        if not text:
            return ""
            
        # Escape user input first to prevent XSS
        escaped_text = escape(text)
        
        if escaped_text.startswith('- '):
            escaped_text = escaped_text[2:]
            
        # Replace the dash pattern with HTML breaks
        formatted = escaped_text.replace(' - ', '<br>&bull; ')
        
        # Preserve user's manual line breaks from the textarea
        formatted = formatted.replace('\n', '<br>')
        
        # Si quedó algún salto inicial suelto
        if formatted.startswith('&bull; '):
            pass # Keep it if it starts with a bullet
            
        return mark_safe(formatted)
        
    def save(self, *args, **kwargs):
        # SEO defaults
        if not self.meta_title:
            self.meta_title = self.titulo[:60]
        if not self.meta_description:
            self.meta_description = self.descripcion_corta[:160]
            
        # YouTube Extraction
        if self.youtube_url:
            # Regex to match youtube ID from multiple formats (watch?v=, youtu.be/, embeds etc)
            yt_regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:shorts\/|[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
            match = re.search(yt_regex, self.youtube_url)
            
            if match:
                new_youtube_id = match.group(1)
                
                # Limpiar la URL para que siempre quede un enlace bonito en el panel
                self.youtube_url = f"https://youtu.be/{new_youtube_id}"
                
                # Fetch new thumbnail if the ID changed or we don't have a thumbnail
                if new_youtube_id != self.youtube_id or not self.miniatura_youtube:
                    self.youtube_id = new_youtube_id
                    thumbnail_url = f"https://img.youtube.com/vi/{self.youtube_id}/maxresdefault.jpg"
                    try:
                        result = urllib.request.urlretrieve(thumbnail_url)
                        self.miniatura_youtube.save(
                            f"{self.youtube_id}.jpg",
                            ContentFile(open(result[0], 'rb').read()),
                            save=False
                        )
                    except Exception:
                        # Fallback to hqdefault
                        try:
                            thumbnail_url = f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg"
                            result = urllib.request.urlretrieve(thumbnail_url)
                            self.miniatura_youtube.save(
                                f"{self.youtube_id}.jpg",
                                ContentFile(open(result[0], 'rb').read()),
                                save=False
                            )
                        except Exception:
                            pass
            else:
                pass # Si no encuentra ID, mantiene lo que estaba o vacío
        else:
            pass # No limpiamos el ID ni la miniatura por si lo subieron a mano

        super().save(*args, **kwargs)

class Capture(models.Model):
    proyecto = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="capturas")
    titulo = models.CharField(_("Título"), max_length=200, blank=True)
    imagen = models.ImageField(_("Imagen"), upload_to="projects/captures/")
    orden = models.PositiveIntegerField(_("Orden"), default=0)

    class Meta:
        verbose_name = _("Captura")
        verbose_name_plural = _("Capturas")
        ordering = ['orden', 'id']

    def __str__(self):
        return f"Captura {self.id} - {self.proyecto.titulo}"
