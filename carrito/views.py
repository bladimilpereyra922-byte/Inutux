from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from carrito.models import Carrito, ItemCarrito
from catalogo.models import Producto


@login_required
def ver_carrito(request):
    """Vista principal del carrito con contexto completo."""
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    return render(
        request,
        "tienda/carrito.html",
        {
            "carrito": carrito,
            "total_items": carrito.items.count(),
            "subtotal": carrito.total(),
        },
    )


@login_required
def agregar_carrito(request, pk):
    """Agrega producto al carrito con feedback visual."""
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    item, creado = ItemCarrito.objects.update_or_create(
        carrito=carrito, producto=producto, defaults={"cantidad": 1}
    )

    if not creado:
        item.cantidad += 1
        item.save()

    messages.success(request, f"✅ {producto.nombre} agregado al carrito.")
    return redirect("carrito")


@login_required
def eliminar_carrito(request, pk):
    """Elimina item del carrito con validación de seguridad."""
    item = get_object_or_404(
        ItemCarrito,
        pk=pk,
        carrito__usuario=request.user,
    )

    nombre_producto = item.producto.nombre
    item.delete()

    messages.info(request, f"🗑️ {nombre_producto} eliminado del carrito.")
    return redirect("carrito")
