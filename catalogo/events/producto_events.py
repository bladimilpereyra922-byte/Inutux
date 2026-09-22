from django.dispatch import Signal


producto_creado = Signal()

producto_actualizado = Signal()

producto_eliminado = Signal()

stock_agotado = Signal()

precio_actualizado = Signal()

producto_publicado = Signal()

producto_despublicado = Signal()