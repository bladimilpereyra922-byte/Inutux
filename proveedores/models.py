from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Proveedor(models.Model):
    ESTADOS = (
        ("pendiente", "Pendiente"),
        ("aprobado", "Aprobado"),
        ("bloqueado", "Bloqueado"),
        ("rechazado", "Rechazado"),
    )

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="proveedor",
    )

    nombre_tienda = models.CharField(
        max_length=200,
        unique=True,
    )

    slug = models.SlugField(
        unique=True,
        max_length=220,
    )

    descripcion = models.TextField(
        blank=True,
    )

    logo = models.ImageField(
        upload_to="proveedores/logos/",
        blank=True,
        null=True,
    )

    banner = models.ImageField(
        upload_to="proveedores/banners/",
        blank=True,
        null=True,
    )

    telefono = models.CharField(
        max_length=30,
        blank=True,
    )

    direccion = models.TextField(
        blank=True,
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente",
        db_index=True,
    )

    comision = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10,
    )

    verificado = models.BooleanField(
        default=False,
    )

    activo = models.BooleanField(
        default=True,
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
    )

    actualizado = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["nombre_tienda"]

        indexes = [
            models.Index(fields=["estado"]),
            models.Index(fields=["activo"]),
            models.Index(fields=["verificado"]),
        ]

    def __str__(self):
        return self.nombre_tienda
