from django.http import JsonResponse
from catalogo.models import Producto


def health(request):
    return JsonResponse({
        "status": "ok",
        "service": "inutux-api",
    })


def productos(request):
    productos_data = []

    for producto in Producto.objects.filter(activo=True).prefetch_related("multimedia"):
        imagen = producto.multimedia.filter(es_principal=True).first()

        productos_data.append({
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "stock": producto.stock,
            "imagen": imagen.archivo.url if imagen and imagen.archivo else None,
        })

    return JsonResponse({
        "success": True,
        "productos": productos_data,
    })
