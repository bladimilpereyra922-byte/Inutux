from django.db import models
from django.utils.text import slugify

from proveedores.models import Proveedor
from catalogo.managers.producto_manager import ProductoManager
from catalogo.validators.producto_validator import ProductoValidator

from .categoria import Categoria


class Producto(models.Model):
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name="productos",
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos",
    )

    nombre = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        unique=True,
        max_length=220,
        blank=True,
    )

    sku = models.CharField(
        max_length=80,
        unique=True,
    )

    descripcion = models.TextField()

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

    costo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    stock = models.PositiveIntegerField(
        default=0,
    )

    activo = models.BooleanField(
        default=True,
    )

    destacado = models.BooleanField(
        default=False,
    )

    digital = models.BooleanField(
        default=False,
    )

    peso = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0,
    )

    alto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    ancho = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    largo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    seo_title = models.CharField(
        max_length=255,
        blank=True,
    )

    seo_description = models.TextField(
        blank=True,
    )

    creado = models.DateTimeField(
        auto_now_add=True,
    )

    actualizado = models.DateTimeField(
        auto_now=True,
    )

    objects = ProductoManager()

    class Meta:
        ordering = ["-creado"]

        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["activo"]),
            models.Index(fields=["destacado"]),
            models.Index(fields=["categoria"]),
            models.Index(fields=["proveedor"]),
            models.Index(fields=["precio"]),
            models.Index(fields=["stock"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(precio__gte=0),
                name="producto_precio_positivo",
            ),
            models.CheckConstraint(
                condition=models.Q(stock__gte=0),
                name="producto_stock_positivo",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)

        ProductoValidator.validar_producto(self)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre