from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    nombre = models.CharField(
        max_length=80,
        unique=True,
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
    )

    descripcion = models.TextField(
        blank=True,
    )

    color = models.CharField(
        max_length=7,
        default="#2563EB",
        help_text="Color hexadecimal (#RRGGBB).",
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
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["nombre"]

        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["activa"]),
            models.Index(fields=["nombre"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre