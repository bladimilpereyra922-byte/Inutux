import json
import os

import firebase_admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from firebase_admin import credentials

from .models import Carrito, Producto, Proveedor

# ---------------------------------------------------------------------------
# Inicialización segura de Firebase Admin SDK (Render + Local)
# ---------------------------------------------------------------------------
if not firebase_admin._apps:
    firebase_key = os.environ.get("FIREBASE_KEY")

    if firebase_key:
        try:
            cred_dict = json.loads(firebase_key)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"⚠️ Error procesando FIREBASE_KEY: {e}")
    else:
        ruta_local = "unitux-c7b8b-firebase-adminsdk-fbsvc-21553d0c90.json"
        if os.path.exists(ruta_local):
            cred = credentials.Certificate(ruta_local)
            firebase_admin.initialize_app(cred)
        elif os.path.exists("firebase-key.json"):
            cred = credentials.Certificate("firebase-key.json")
            firebase_admin.initialize_app(cred)
        else:
            print("⚠️ Firebase no configurado. El proyecto iniciará sin Firebase.")


# ---------------------------------------------------------------------------
# Vistas Principales
# ---------------------------------------------------------------------------
def inicio(request):
    """Pantalla principal Cyber-Luxe conectada a catalogo.Producto."""
    busqueda = request.GET.get("q", "")

    productos = Producto.objects.filter(activo=True)
    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    productos_destacados = productos.order_by("-creado_en")[:8]

    return render(
        request,
        "tienda/home.html",
        {
            "productos_destacados": productos_destacados,
            "busqueda": busqueda,
        },
    )


@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, "tienda/carrito.html", {"carrito": carrito})


@login_required
def panel_proveedor(request):
    try:
        proveedor = Proveedor.objects.get(usuario=request.user)
        productos = Producto.objects.filter(proveedor=proveedor)
        return render(
            request,
            "tienda/panel_proveedor.html",
            {"proveedor": proveedor, "productos": productos},
        )
    except Proveedor.DoesNotExist:
        return redirect("registro_proveedor")


@login_required
def pago(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    total_calculado = carrito.total()
    total_formateado = f"{total_calculado:.2f}" if total_calculado else "0.00"

    return render(request, "tienda/pago.html", {"total": total_formateado})

def detalle_producto(request, pk):
    """Vista para mostrar el detalle de un producto."""
    from django.shortcuts import get_object_or_404
    
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    
    return render(
        request, 
        "tienda/detalle_producto.html", 
        {"producto": producto}
    )