from django.db import models
from django.utils.translation import gettext_lazy as _

class Message(models.Model):
    nombre = models.CharField(_("Nombre"), max_length=150)
    email = models.EmailField(_("Email"))
    mensaje = models.TextField(_("Mensaje"))
    fecha = models.DateTimeField(_("Fecha de Recepción"), auto_now_add=True)
    leido = models.BooleanField(_("Leído"), default=False)

    class Meta:
        verbose_name = _("Mensaje de Contacto")
        verbose_name_plural = _("Mensajes de Contacto")
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.nombre} - {self.email}"
