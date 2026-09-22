from django.db import transaction

from catalogo.models import Producto
from catalogo.events.producto_events import (
    producto_creado,
    producto_actualizado,
    producto_publicado,
    producto_despublicado,
)


class ProductoService:

    @staticmethod
    @transaction.atomic
    def crear(**datos):
        producto = Producto.objects.create(**datos)

        producto_creado.send(
            sender=Producto,
            producto=producto,
        )

        return producto

    @staticmethod
    @transaction.atomic
    def actualizar(producto: Producto, **datos):
        for campo, valor in datos.items():
            setattr(producto, campo, valor)

        producto.save()

        producto_actualizado.send(
            sender=Producto,
            producto=producto,
        )

        return producto

    @staticmethod
    @transaction.atomic
    def activar(producto: Producto):
        producto.activo = True
        producto.save(update_fields=["activo"])

        producto_publicado.send(
            sender=Producto,
            producto=producto,
        )

        return producto

    @staticmethod
    @transaction.atomic
    def desactivar(producto: Producto):
        producto.activo = False
        producto.save(update_fields=["activo"])

        producto_despublicado.send(
            sender=Producto,
            producto=producto,
        )

        return producto

    @staticmethod
    @transaction.atomic
    def marcar_destacado(producto: Producto):
        producto.destacado = True
        producto.save(update_fields=["destacado"])

        return producto

    @staticmethod
    @transaction.atomic
    def quitar_destacado(producto: Producto):
        producto.destacado = False
        producto.save(update_fields=["destacado"])

        return producto

    @staticmethod
    @transaction.atomic
    def actualizar_stock(producto: Producto, stock: int):
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        producto.stock = stock
        producto.save(update_fields=["stock"])

        return producto

    @staticmethod
    @transaction.atomic
    def actualizar_precio(producto: Producto, precio):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")

        producto.precio = precio
        producto.save(update_fields=["precio"])

        return producto

    @staticmethod
    @transaction.atomic
    def eliminar(producto: Producto):
        producto.delete()