from django.contrib.auth.models import User
from django.db import models


class CuponFidelidad(models.Model):
    TIPOS = (
        ("porcentaje", "Porcentaje"),
        ("fijo", "Monto Fijo"),
    )

    codigo = models.CharField(max_length=20, unique=True, db_index=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cupones")
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_descuento = models.CharField(
        max_length=10, choices=TIPOS, default="porcentaje"
    )
    minimo_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()
    usado = models.BooleanField(default=False)
    origen = models.CharField(max_length=50, default="sistema_fidelidad")

    class Meta:
        ordering = "-fecha_creacion"
        indexes = (
            models.Index(fields=["usuario", "usado"], name="idx_cupon_usuario_usado"),
        )

    def __str__(self):
        return f"{self.codigo} - {self.usuario.email}"
