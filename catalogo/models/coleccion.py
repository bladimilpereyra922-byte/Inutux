from django.db import models
from django.utils.text import slugify


class Coleccion(models.Model):
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
        upload_to="colecciones/",
        blank=True,
        null=True,
    )

    activa = models.BooleanField(
        default=True,
    )

    destacada = models.BooleanField(
        default=False,
    )

    orden = models.PositiveIntegerField(
        default=0,
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
        verbose_name = "Colección"
        verbose_name_plural = "Colecciones"
        ordering = ["orden", "nombre"]

        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["activa"]),
            models.Index(fields=["destacada"]),
            models.Index(fields=["orden"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre