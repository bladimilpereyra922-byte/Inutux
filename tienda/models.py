from django.db import models


class ConfiguracionTienda(models.Model):
    """Modelo exclusivo de la app tienda para configuración global."""

    nombre = models.CharField(max_length=200, default="UNITUX")
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "configuración de tienda"
        verbose_name_plural = "configuraciones de tienda"
        ordering = ("-creado_en",)

    def __str__(self):
        return self.nombre