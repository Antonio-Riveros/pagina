from django.db import models

class HomePageConfig(models.Model):
    titulo_principal = models.CharField(max_length=200, default='Construyendo el futuro')
    subtitulo_destacado = models.CharField(max_length=200, default='línea por línea_')
    descripcion = models.TextField(default='Creamos soluciones digitales robustas.')
    imagen_hero = models.ImageField(upload_to='core/', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name = 'Configuración de Inicio'
        verbose_name_plural = 'Configuración de Inicio'

    def __str__(self):
        return "Configuración del Inicio"
