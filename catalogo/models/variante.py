from django.db import models

from .producto import Producto


class VarianteProducto(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="variantes",
    )

    nombre = models.CharField(
        max_length=120,
    )

    sku = models.CharField(
        max_length=80,
        unique=True,
    )

    codigo_barras = models.CharField(
        max_length=100,
        blank=True,
    )

    precio = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    precio_oferta = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    stock = models.PositiveIntegerField(
        default=0,
    )

    peso = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0,
    )

    activa = models.BooleanField(
        default=True,
    )

    creada = models.DateTimeField(
        auto_now_add=True,
    )

    actualizada = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Variante"
        verbose_name_plural = "Variantes"
        ordering = ["producto", "nombre"]

        indexes = [
            models.Index(fields=["producto"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["activa"]),
            models.Index(fields=["stock"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(precio__gte=0),
                name="variante_precio_positivo",
            ),
            models.CheckConstraint(
                condition=models.Q(stock__gte=0),
                name="variante_stock_positivo",
            ),
        ]

    def __str__(self):
        return f"{self.producto.nombre} - {self.nombre}"