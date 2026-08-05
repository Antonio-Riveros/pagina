from django.db import models
from django.utils.translation import gettext_lazy as _

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
    STATUS_CHOICES = (
        ('en_desarrollo', 'En Desarrollo'),
        ('completado', 'Completado'),
        ('mantenimiento', 'En Mantenimiento'),
    )

    titulo = models.CharField(_("Título"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    resumen = models.TextField(_("Resumen"), max_length=500)
    descripcion_larga = models.TextField(_("Descripción Larga"), blank=True)
    
    imagen_principal = models.ImageField(_("Imagen Principal"), upload_to="projects/")
    logo = models.ImageField(_("Logo del Proyecto"), upload_to="projects/logos/", blank=True, null=True)
    
    estado = models.CharField(_("Estado"), max_length=50, choices=STATUS_CHOICES, default='completado')
    destacado = models.BooleanField(_("Destacado"), default=False)
    publicado = models.BooleanField(_("Publicado"), default=True)
    
    fecha_creacion = models.DateField(_("Fecha de Creación"), blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    url_demo = models.URLField(_("URL Demo"), blank=True)
    url_github = models.URLField(_("URL GitHub"), blank=True)
    url_cliente = models.URLField(_("URL Cliente"), blank=True)
    
    orden = models.PositiveIntegerField(_("Orden"), default=0)
    
    # Relations
    categorias = models.ManyToManyField(Category, verbose_name=_("Categorías"), related_name="proyectos", blank=True)
    tecnologias = models.ManyToManyField(Technology, verbose_name=_("Tecnologías"), related_name="proyectos", blank=True)
    
    # SEO
    meta_title = models.CharField(_("Meta Title"), max_length=60, blank=True)
    meta_description = models.CharField(_("Meta Description"), max_length=160, blank=True)

    class Meta:
        verbose_name = _("Proyecto")
        verbose_name_plural = _("Proyectos")
        ordering = ['orden', '-fecha_creacion']

    def __str__(self):
        return self.titulo

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
