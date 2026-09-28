from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.text import slugify

from catalogo.models import Producto
from proveedores.models import Proveedor


@login_required
def panel_proveedor(request):
    """Panel profesional de vendedor con verificación de estado."""
    try:
        proveedor = request.user.proveedor

        # Validación estricta de estado
        if proveedor.estado != "aprobado":
            return render(
                request,
                "tienda/pendiente.html",
                {"proveedor": proveedor},
            )

        productos = Producto.objects.filter(proveedor=proveedor)

        return render(
            request,
            "tienda/panel_proveedor.html",
            {
                "proveedor": proveedor,
                "productos": productos,
                "total_productos": productos.count(),
            },
        )

    except Proveedor.DoesNotExist:
        return redirect("registro_proveedor")


@login_required
def registro_proveedor(request):
    """Registro seguro de proveedor con validaciones completas."""

    # Si ya es proveedor aprobado, redirigir al panel
    if (
        hasattr(request.user, "proveedor")
        and request.user.proveedor.estado == "aprobado"
    ):
        return redirect("panel_proveedor")

    if request.method == "POST":
        nombre_tienda = request.POST.get("nombre_tienda", "").strip()
        descripcion = request.POST.get("descripcion", "").strip()
        telefono = request.POST.get("telefono", "").strip()

        # Validaciones profesionales
        errores = []
        if not nombre_tienda:
            errores.append("El nombre de la tienda es obligatorio.")

        if len(nombre_tienda) < 3:
            errores.append("El nombre debe tener al menos 3 caracteres.")

        if not telefono:
            errores.append("El teléfono de contacto es obligatorio.")

        # Verificar slug único
        slug_propuesto = slugify(nombre_tienda)
        if (
            Proveedor.objects.filter(slug=slug_propuesto)
            .exclude(usuario=request.user)
            .exists()
        ):
            errores.append("Ya existe una tienda con ese nombre. Por favor elige otro.")

        if errores:
            for error in errores:
                messages.error(request, error)
            return render(
                request,
                "tienda/registro_proveedor.html",
                {
                    "nombre_tienda": nombre_tienda,
                    "descripcion": descripcion,
                    "telefono": telefono,
                },
            )

        # Creación segura del proveedor
        Proveedor.objects.create(
            usuario=request.user,
            nombre_tienda=nombre_tienda,
            descripcion=descripcion,
            telefono=telefono,
            slug=slug_propuesto,
        )

        messages.success(
            request, f"✅ ¡Tienda '{nombre_tienda}' registrada exitosamente!"
        )
        return redirect("panel_proveedor")

    return render(request, "tienda/registro_proveedor.html")
