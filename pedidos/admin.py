from django.contrib import admin

from .models import DireccionPedido, EventoPedido, ItemPedido, Pago, Pedido, PedidoProveedor


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('creado_en',)


class EventoPedidoInline(admin.TabularInline):
    model = EventoPedido
    extra = 0
    readonly_fields = ('creado_en',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'cliente', 'estado', 'total', 'moneda', 'creado_en')
    list_filter = ('estado', 'moneda')
    search_fields = ('codigo', 'cliente__username', 'cliente__email')
    readonly_fields = ('codigo', 'creado_en', 'actualizado_en', 'pagado_en', 'cancelado_en')
    date_hierarchy = 'creado_en'


@admin.register(PedidoProveedor)
class PedidoProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'pedido',
        'proveedor',
        'estado',
        'estado_logistico',
        'total',
        'creado_en',
    )
    list_filter = ('estado', 'estado_logistico', 'proveedor')
    search_fields = ('codigo', 'pedido__codigo', 'proveedor__nombre_tienda')
    readonly_fields = (
        'creado_en',
        'actualizado_en',
        'preparado_en',
        'enviado_en',
        'entregado_en',
        'cancelado_en',
    )
    inlines = (ItemPedidoInline, EventoPedidoInline)
    date_hierarchy = 'creado_en'


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('producto_nombre', 'pedido_proveedor', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('producto_nombre', 'pedido_proveedor__codigo')
    readonly_fields = ('creado_en',)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'proveedor_pago', 'estado', 'monto', 'moneda', 'confirmado_en')
    list_filter = ('proveedor_pago', 'estado', 'moneda')
    search_fields = ('pedido__codigo', 'referencia_externa')
    readonly_fields = ('creado_en', 'confirmado_en')


@admin.register(DireccionPedido)
class DireccionPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'destinatario', 'ciudad', 'provincia', 'pais', 'telefono')
    search_fields = ('pedido__codigo', 'destinatario', 'ciudad', 'provincia', 'municipio', 'telefono')
    readonly_fields = ('creado_en',)


@admin.register(EventoPedido)
class EventoPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido_proveedor', 'tipo', 'actor', 'estado_anterior', 'estado_nuevo', 'creado_en')
    list_filter = ('tipo',)
    search_fields = ('pedido_proveedor__codigo', 'actor__username', 'comentario')
    readonly_fields = ('creado_en',)
