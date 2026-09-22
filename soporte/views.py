from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from proveedores.models import Proveedor


@login_required
def chat_soporte(request):
    proveedores = Proveedor.objects.filter(
        estado="aprobado",
        activo=True,
    )

    return render(
        request,
        "soporte/chat_soporte.html",
        {
            "proveedores": proveedores,
        },
    )