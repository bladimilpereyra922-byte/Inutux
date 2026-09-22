from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from proveedores.models import Proveedor
from catalogo.models import Producto


@login_required
def panel_proveedor(request):
    try:
        proveedor = request.user.proveedor

        if proveedor.estado != "aprobado":
            return render(
                request,
                "tienda/pendiente.html",
            )

        productos = Producto.objects.filter(
            proveedor=proveedor,
        )

        return render(
            request,
            "tienda/panel_proveedor.html",
            {
                "proveedor": proveedor,
                "productos": productos,
            },
        )

    except Proveedor.DoesNotExist:
        return redirect("registro_proveedor")


@login_required
def registro_proveedor(request):

    if request.method == "POST":

        Proveedor.objects.create(
            usuario=request.user,
            nombre_tienda=request.POST.get("nombre_tienda"),
            descripcion=request.POST.get("descripcion"),
            telefono=request.POST.get("telefono"),
            slug=slugify(request.POST.get("nombre_tienda")),
        )

        return redirect("panel_proveedor")

    return render(
        request,
        "tienda/registro_proveedor.html",
    )