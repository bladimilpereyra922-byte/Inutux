from django.db import models

from .variante import VarianteProducto


class MovimientoInventario(models.Model):
    TIPOS = [
        ("entrada", "Entrada"),
        ("salida", "Salida"),
        ("ajuste", "Ajuste"),
        ("reserva", "Reserva"),
        ("liberacion", "Liberación"),
        ("devolucion", "Devolución"),
    ]

    variante = models.ForeignKey(
        VarianteProducto,
        on_delete=models.CASCADE,
        related_name="movimientos_inventario",
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS,
    )

    cantidad = models.PositiveIntegerField()

    stock_anterior = models.PositiveIntegerField()

    stock_nuevo = models.PositiveIntegerField()

    referencia = models.CharField(
        max_length=120,
        blank=True,
    )

    observaciones = models.TextField(
        blank=True,
    )

    creado = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
        ordering = ["-creado"]

        indexes = [
            models.Index(fields=["variante"]),
            models.Index(fields=["tipo"]),
            models.Index(fields=["creado"]),
        ]

    def __str__(self):
        return f"{self.variante} - {self.tipo} ({self.cantidad})"