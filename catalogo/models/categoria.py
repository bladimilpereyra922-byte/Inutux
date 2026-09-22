from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    nombre = models.CharField(
        max_length=150,
        unique=True,
    )

    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True,
    )

    descripcion = models.TextField(
        blank=True,
    )

    imagen = models.ImageField(
        upload_to="categorias/",
        blank=True,
        null=True,
    )

    categoria_padre = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="subcategorias",
    )

    orden = models.PositiveIntegerField(
        default=0,
    )

    activa = models.BooleanField(
        default=True,
    )

    seo_title = models.CharField(
        max_length=255,
        blank=True,
    )

    seo_description = models.TextField(
        blank=True,
    )

    creada = models.DateTimeField(
        auto_now_add=True,
    )

    actualizada = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["orden", "nombre"]

        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["activa"]),
            models.Index(fields=["categoria_padre"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre