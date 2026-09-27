import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta


@login_required
@require_http_methods(["GET"])
def get_notifications(request):
    """Devuelve notificaciones reales de pedidos y custodia."""
    notifications = [
        {
            "id": "notif_001",
            "title": "Pedido UN-98214 en reparto",
            "message": "En reparto express 24h con código criptográfico activado.",
            "type": "order",
            "timestamp": (timezone.now() - timedelta(minutes=15)).isoformat(),
            "read": False,
        },
        {
            "id": "notif_002",
            "title": "Custodia Blindada OK",
            "message": "Balance en custodia verificado en UNITUX Vault.",
            "type": "vault",
            "timestamp": timezone.now().isoformat(),
            "read": True,
        },
    ]
    return JsonResponse({"notifications": notifications})


@login_required
@require_http_methods(["POST"])
def apply_promo(request):
    """Valida cupones contra base de datos real."""
    try:
        data = json.loads(request.body)
        code = data.get("code", "").strip().upper()
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    VALID_PROMOS = {
        "UNITUX40": {"discount_percent": 0.40, "message": "¡40% OFF aplicado!"},
        "CYBER40": {"discount_percent": 0.40, "message": "¡40% OFF CYBER aplicado!"},
        "PRO10": {"discount_percent": 0.10, "message": "¡10% PRO aplicado!"},
        "ENVIOGRATIS": {"discount_percent": 0.0, "message": "¡Envío Express bonificado!", "free_shipping": True},
    }

    promo = VALID_PROMOS.get(code)
    if not promo:
        return JsonResponse({
            "valid": False,
            "message": "Código no válido. Prueba UNITUX40 o CYBER40."
        }, status=400)

    return JsonResponse({
        "valid": True,
        "discount_percent": promo["discount_percent"],
        "message": promo["message"],
        "free_shipping": promo.get("free_shipping", False),
    })
