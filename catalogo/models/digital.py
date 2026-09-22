from django.db import models

from .producto import Producto


class ProductoDigital(models.Model):
    producto = models.OneToOneField(
        Producto,
        on_delete=models.CASCADE,
        related_name="producto_digital",
    )

    archivo = models.FileField(
        upload_to="productos_digitales/",
    )

    version = models.CharField(
        max_length=50,
        blank=True,
    )

    tamano_mb = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    descargas_maximas = models.PositiveIntegerField(
        default=0,
        help_text="0 = ilimitadas",
    )

    dias_disponibles = models.PositiveIntegerField(
        default=0,
        help_text="0 = sin vencimiento",
    )

    requiere_licencia = models.BooleanField(
        default=False,
    )

    activa = models.BooleanField(
        default=True,
    )

    creado = models.DateTimeField(
        auto_now_add=True,
    )

    actualizado = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Producto digital"
        verbose_name_plural = "Productos digitales"

        indexes = [
            models.Index(fields=["activa"]),
            models.Index(fields=["version"]),
        ]

    def __str__(self):
        return f"Digital - {self.producto.nombre}"