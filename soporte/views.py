import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from proveedores.models import Proveedor


@login_required
def chat_soporte(request):
    """Vista principal del chat de soporte."""
    proveedores = Proveedor.objects.filter(estado="aprobado", activo=True)
    return render(
        request,
        "soporte/chat_soporte.html",
        {"proveedores": proveedores},
    )


@login_required
@require_http_methods(["POST"])
def api_chat_ia(request):
    """Endpoint API para el agente de IA UNITUX."""
    try:
        data = json.loads(request.body)
        mensaje_usuario = data.get("mensaje", "").strip()

        if not mensaje_usuario:
            return JsonResponse({"error": "Mensaje vacío"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    #  LÓGICA DEL AGENTE DE IA UNITUX
    # En producción, aquí conectarías con OpenAI, Anthropic o tu modelo local
    respuesta_ia = _generar_respuesta_ia(mensaje_usuario)

    return JsonResponse(
        {
            "respuesta": respuesta_ia,
            "timestamp": __import__("django.utils.timezone").now().isoformat(),
        }
    )


def _generar_respuesta_ia(mensaje: str) -> str:
    """Motor de respuesta inteligente basado en reglas + fallback."""
    mensaje_lower = mensaje.lower()

    # Base de conocimiento UNITUX
    base_conocimiento = {
        "envio": " Todos los envíos son express 24h con custodia blindada. Tu pedido llegará mañana antes de las 6 PM.",
        "pago": "💳 Aceptamos tarjetas, transferencias y cripto. Los fondos quedan en custodia hasta la verificación técnica.",
        "devolucion": "🔄 Tienes 7 días hábiles para devoluciones. El reembolso se procesa en 48h tras la inspección.",
        "garantia": "🛡️ Garantía UNITUX PRO: 90 días de cobertura total contra defectos de fábrica.",
        "vender": "🏪 Para vender en UNITUX necesitas registro de proveedor aprobado. ¿Quieres que te envíe el formulario?",
        "custodia": "🔒 Custodia Blindada: Tus fondos están protegidos por smart contracts hasta que recibas y verifiques el producto.",
        "horario": "⏰ Soporte humano disponible 24/7. Nuestro agente IA responde al instante en cualquier momento.",
        "precio": "💰 Los precios incluyen IVA y envío express. No hay costos ocultos en UNITUX.",
    }

    # Búsqueda inteligente por palabras clave
    for keyword, respuesta in base_conocimiento.items():
        if keyword in mensaje_lower:
            return respuesta

    # Fallback profesional cuando no entiende
    return (
        '🤖 Soy el Agente UNITUX. Entendí tu consulta sobre "' + mensaje[:50] + '...". '
        "Para darte una respuesta precisa, ¿podrías especificar si es sobre: "
        "envíos, pagos, garantías, devoluciones o registro de vendedor? "
        "Si prefieres, puedo conectarte con un especialista humano ahora mismo."
    )
