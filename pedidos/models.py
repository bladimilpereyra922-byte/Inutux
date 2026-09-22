from django.conf import settings
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone


class Moneda(models.TextChoices):
    USD = 'USD', 'Dólar estadounidense'
    DOP = 'DOP', 'Peso dominicano'
    EUR = 'EUR', 'Euro'
    MXN = 'MXN', 'Peso mexicano'
    COP = 'COP', 'Peso colombiano'


class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE_PAGO = 'pendiente_pago', 'Pendiente de pago'
        PAGADO = 'pagado', 'Pagado'
        EN_PROCESO = 'en_proceso', 'En proceso'
        PARCIALMENTE_ENTREGADO = 'parcialmente_entregado', 'Parcialmente entregado'
        ENTREGADO = 'entregado', 'Entregado'
        CANCELADO = 'cancelado', 'Cancelado'
        REEMBOLSADO = 'reembolsado', 'Reembolsado'
        CERRADO = 'cerrado', 'Cerrado'

    codigo = models.CharField(max_length=32, unique=True)
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='pedidos',
    )
    estado = models.CharField(
        max_length=30,
        choices=Estado.choices,
        default=Estado.PENDIENTE_PAGO,
    )
    moneda = models.CharField(max_length=3, choices=Moneda.choices, default=Moneda.USD)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    envio_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuesto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    pagado_en = models.DateTimeField(null=True, blank=True)
    cancelado_en = models.DateTimeField(null=True, blank=True)
    motivo_cancelacion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        indexes = [
            models.Index(fields=['cliente', '-creado_en'], name='pedido_cliente_creado_idx'),
            models.Index(fields=['estado', '-creado_en'], name='pedido_estado_creado_idx'),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(subtotal__gte=0)
                & Q(descuento_total__gte=0)
                & Q(envio_total__gte=0)
                & Q(impuesto_total__gte=0)
                & Q(total__gte=0),
                name='pedido_importes_no_negativos',
            ),
        ]

    def __str__(self):
        return f'Pedido {self.codigo}'

    @classmethod
    def generar_codigo(cls):
        """Genera el siguiente código correlativo anual de un pedido."""
        anio = timezone.localdate().year
        prefijo = f'UTX-{anio}-'
        ultimo_codigo = (
            cls.objects.select_for_update()
            .filter(codigo__startswith=prefijo)
            .order_by('-codigo')
            .values_list('codigo', flat=True)
            .first()
        )
        consecutivo = int(ultimo_codigo.rsplit('-', 1)[-1]) + 1 if ultimo_codigo else 1
        return f'{prefijo}{consecutivo:06d}'

    def save(self, *args, **kwargs):
        if self._state.adding and not self.codigo:
            with transaction.atomic():
                self.codigo = self.generar_codigo()
                return super().save(*args, **kwargs)
        return super().save(*args, **kwargs)


class PedidoProveedor(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE_PAGO = 'pendiente_pago', 'Pendiente de pago'
        PAGADO = 'pagado', 'Pagado'
        CONFIRMADO = 'confirmado', 'Confirmado'
        EN_PREPARACION = 'en_preparacion', 'En preparación'
        ENVIADO = 'enviado', 'Enviado'
        ENTREGADO = 'entregado', 'Entregado'
        CANCELADO = 'cancelado', 'Cancelado'
        REEMBOLSADO = 'reembolsado', 'Reembolsado'
        INCIDENCIA = 'incidencia', 'Incidencia'

    class EstadoLogistico(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        EN_PREPARACION = 'en_preparacion', 'En preparación'
        LISTO_DESPACHO = 'listo_despacho', 'Listo para despacho'
        EN_TRANSITO = 'en_transito', 'En tránsito'
        ENTREGADO = 'entregado', 'Entregado'
        DEVUELTO = 'devuelto', 'Devuelto'

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.PROTECT,
        related_name='pedidos_proveedor',
    )
    proveedor = models.ForeignKey(
        'proveedores.Proveedor',
        on_delete=models.PROTECT,
        related_name='pedidos_proveedor',
    )
    codigo = models.CharField(max_length=40, unique=True)
    estado = models.CharField(
        max_length=30,
        choices=Estado.choices,
        default=Estado.PENDIENTE_PAGO,
    )
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    envio = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    porcentaje_comision = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    monto_comision = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monto_proveedor = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    costo_envio = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    costo_logistico = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ganancia_unitux = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado_logistico = models.CharField(
        max_length=30,
        choices=EstadoLogistico.choices,
        default=EstadoLogistico.PENDIENTE,
    )
    transportista = models.CharField(max_length=120, blank=True)
    numero_seguimiento = models.CharField(max_length=120, blank=True)
    fecha_estimada_entrega = models.DateTimeField(null=True, blank=True)
    nota_cliente = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    preparado_en = models.DateTimeField(null=True, blank=True)
    enviado_en = models.DateTimeField(null=True, blank=True)
    entregado_en = models.DateTimeField(null=True, blank=True)
    cancelado_en = models.DateTimeField(null=True, blank=True)
    motivo_cancelacion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'pedido de proveedor'
        verbose_name_plural = 'pedidos de proveedores'
        indexes = [
            models.Index(
                fields=['proveedor', 'estado', '-creado_en'],
                name='pedprov_operacion_idx',
            ),
            models.Index(fields=['estado', '-creado_en'], name='pedprov_estado_creado_idx'),
            models.Index(
                fields=['estado_logistico', '-creado_en'],
                name='pedprov_logistica_idx',
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['pedido', 'proveedor'],
                name='pedido_proveedor_unico',
            ),
            models.CheckConstraint(
                condition=Q(subtotal__gte=0)
                & Q(descuento_total__gte=0)
                & Q(envio__gte=0)
                & Q(impuesto__gte=0)
                & Q(total__gte=0)
                & Q(porcentaje_comision__gte=0)
                & Q(monto_comision__gte=0)
                & Q(monto_proveedor__gte=0)
                & Q(costo_envio__gte=0)
                & Q(costo_logistico__gte=0),
                name='pedprov_importes_no_negativos',
            ),
        ]

    def __str__(self):
        return f'{self.codigo} · {self.proveedor.nombre_tienda}'


class ItemPedido(models.Model):
    pedido_proveedor = models.ForeignKey(
        PedidoProveedor,
        on_delete=models.PROTECT,
        related_name='items',
    )
    producto = models.ForeignKey(
        'catalogo.Producto',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items_pedido',
    )
    producto_nombre = models.CharField(max_length=200)
    producto_descripcion = models.TextField(blank=True)
    proveedor_nombre = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, blank=True)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ítem de pedido'
        verbose_name_plural = 'ítems de pedido'
        indexes = [
            models.Index(fields=['pedido_proveedor'], name='itemped_proveedor_idx'),
            models.Index(fields=['producto', '-creado_en'], name='itemped_producto_creado_idx'),
        ]
        constraints = [
            models.CheckConstraint(condition=Q(cantidad__gt=0), name='itemped_cantidad_positiva'),
            models.CheckConstraint(
                condition=Q(precio_unitario__gte=0) & Q(subtotal__gte=0),
                name='itemped_importes_no_negativos',
            ),
        ]

    def __str__(self):
        return f'{self.cantidad} × {self.producto_nombre}'


class Pago(models.Model):
    class ProveedorPago(models.TextChoices):
        PAYPAL = 'paypal', 'PayPal'
        STRIPE = 'stripe', 'Stripe'
        TRANSFERENCIA = 'transferencia', 'Transferencia'
        WALLET = 'wallet', 'Wallet'
        EFECTIVO = 'efectivo', 'Efectivo'

    class Estado(models.TextChoices):
        CREADO = 'creado', 'Creado'
        PENDIENTE = 'pendiente', 'Pendiente'
        AUTORIZADO = 'autorizado', 'Autorizado'
        CAPTURADO = 'capturado', 'Capturado'
        FALLIDO = 'fallido', 'Fallido'
        CANCELADO = 'cancelado', 'Cancelado'
        REEMBOLSADO = 'reembolsado', 'Reembolsado'
        PARCIALMENTE_REEMBOLSADO = 'parcialmente_reembolsado', 'Parcialmente reembolsado'

    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, related_name='pagos')
    proveedor_pago = models.CharField(
        max_length=30,
        choices=ProveedorPago.choices,
        default=ProveedorPago.PAYPAL,
    )
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.CREADO)
    referencia_externa = models.CharField(max_length=255, unique=True, null=True, blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    moneda = models.CharField(max_length=3, choices=Moneda.choices, default=Moneda.USD)
    respuesta_proveedor = models.JSONField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    confirmado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'pago'
        verbose_name_plural = 'pagos'
        indexes = [
            models.Index(fields=['pedido', 'estado'], name='pago_pedido_estado_idx'),
            models.Index(
                fields=['proveedor_pago', 'estado', '-creado_en'],
                name='pago_conciliacion_idx',
            ),
        ]
        constraints = [
            models.CheckConstraint(condition=Q(monto__gte=0), name='pago_monto_no_negativo'),
        ]

    def __str__(self):
        return f'Pago {self.get_proveedor_pago_display()} · {self.pedido.codigo}'


class DireccionPedido(models.Model):
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.PROTECT,
        related_name='direccion_envio',
    )
    destinatario = models.CharField(max_length=200)
    telefono = models.CharField(max_length=30)
    linea_1 = models.CharField(max_length=255)
    linea_2 = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=120)
    departamento_estado = models.CharField(max_length=120, blank=True)
    provincia = models.CharField(max_length=120, blank=True)
    municipio = models.CharField(max_length=120, blank=True)
    sector = models.CharField(max_length=120, blank=True)
    codigo_postal = models.CharField(max_length=30, blank=True)
    pais = models.CharField(max_length=2)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    referencia = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'dirección de pedido'
        verbose_name_plural = 'direcciones de pedido'

    def __str__(self):
        return f'{self.pedido.codigo} · {self.destinatario}'


class EventoPedido(models.Model):
    class Tipo(models.TextChoices):
        CAMBIO_ESTADO = 'cambio_estado', 'Cambio de estado'
        PAGO = 'pago', 'Pago'
        SISTEMA = 'sistema', 'Sistema'
        NOTA = 'nota', 'Nota'

    pedido_proveedor = models.ForeignKey(
        PedidoProveedor,
        on_delete=models.PROTECT,
        related_name='eventos',
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos_pedido',
    )
    tipo = models.CharField(max_length=30, choices=Tipo.choices, default=Tipo.SISTEMA)
    estado_anterior = models.CharField(max_length=30, blank=True)
    estado_nuevo = models.CharField(max_length=30, blank=True)
    comentario = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'evento de pedido'
        verbose_name_plural = 'eventos de pedido'
        indexes = [
            models.Index(
                fields=['pedido_proveedor', '-creado_en'],
                name='evento_pedprov_creado_idx',
            ),
        ]

    def __str__(self):
        return f'{self.get_tipo_display()} · {self.pedido_proveedor.codigo}'