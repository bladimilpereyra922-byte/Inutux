from django.db import models

from .producto import Producto


class MultimediaProducto(models.Model):
    TIPOS = [
        ("imagen", "Imagen"),
        ("video", "Video"),
        ("modelo3d", "Modelo 3D"),
        ("documento", "Documento"),
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="multimedia",
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS,
        default="imagen",
    )

    archivo = models.FileField(
        upload_to="catalogo/",
    )

    titulo = models.CharField(
        max_length=200,
        blank=True,
    )

    texto_alternativo = models.CharField(
        max_length=255,
        blank=True,
    )

    principal = models.BooleanField(
        default=False,
    )

    orden = models.PositiveIntegerField(
        default=0,
    )

    activo = models.BooleanField(
        default=True,
    )

    creado = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Multimedia del producto"
        verbose_name_plural = "Multimedia de productos"
        ordering = ["orden", "id"]

        indexes = [
            models.Index(fields=["producto"]),
            models.Index(fields=["tipo"]),
            models.Index(fields=["principal"]),
            models.Index(fields=["activo"]),
        ]

    def __str__(self):
        return f"{self.producto.nombre} - {self.tipo}"