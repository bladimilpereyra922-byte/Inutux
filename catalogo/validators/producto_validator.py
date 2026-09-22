from decimal import Decimal

from django.core.exceptions import ValidationError


class ProductoValidator:

    @staticmethod
    def validar_precio(precio):
        if precio is None:
            raise ValidationError("El precio es obligatorio.")

        if Decimal(precio) < 0:
            raise ValidationError("El precio no puede ser negativo.")

    @staticmethod
    def validar_precio_oferta(precio, oferta):
        if oferta is None:
            return

        if Decimal(oferta) < 0:
            raise ValidationError("El precio de oferta no puede ser negativo.")

        if Decimal(oferta) >= Decimal(precio):
            raise ValidationError(
                "El precio de oferta debe ser menor que el precio normal."
            )

    @staticmethod
    def validar_stock(stock):
        if stock < 0:
            raise ValidationError(
                "El stock no puede ser negativo."
            )

    @staticmethod
    def validar_sku(sku):
        if not sku:
            raise ValidationError(
                "El SKU es obligatorio."
            )

        if len(sku) < 4:
            raise ValidationError(
                "El SKU es demasiado corto."
            )

    @classmethod
    def validar_producto(cls, producto):
        cls.validar_precio(producto.precio)
        cls.validar_precio_oferta(
            producto.precio,
            producto.precio_oferta,
        )
        cls.validar_stock(producto.stock)
        cls.validar_sku(producto.sku)