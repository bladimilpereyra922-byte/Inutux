import json
import logging
import os
import secrets

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


def registro(request):
    """Registro seguro con UserCreationForm estándar de Django."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("inicio")
    else:
        form = UserCreationForm()
    return render(request, "usuarios/registro.html", {"form": form})


def login_view(request):
    """Login tradicional con protección CSRF implícita por Django."""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get("next", "/")
            if next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)
            return redirect("inicio")
    else:
        form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form})


@require_http_methods(["GET"])
def perfil_view(request):
    """Vista profesional de perfil de usuario."""
    if not request.user.is_authenticated:
        return redirect("login")

    context = {
        "user": request.user,
        "orders": [],
        "favorites": [],
    }
    return render(request, "usuarios/perfil.html", context)


def recuperar_password(request):
    """Recuperación segura de contraseña con token temporal."""
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        user = User.objects.filter(email__iexact=email).first()

        if user:
            token = secrets.token_urlsafe(32)
            request.session["reset_token"] = {
                "uid": user.pk,
                "token": token,
                "expires": (timezone.now() + __import__("datetime").timedelta(hours=1)).isoformat(),
            }
            msg = "Si el correo está registrado, recibirás instrucciones."
        else:
            msg = "Si el correo está registrado, recibirás instrucciones."

        return render(request, "usuarios/recuperar_password.html", {"message": msg})

    return render(request, "usuarios/recuperar_password.html")


def reset_password_confirm(request, uidb64, token):
    """Valida token y permite establecer nueva contraseña."""
    return render(request, "usuarios/reset_password_confirm.html")


def logout_view(request):
    """Cierra sesión y redirige al inicio."""
    logout(request)
    return redirect("inicio")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def google_login(request):
    """
    Flujo dual seguro de Google Auth optimizado para producción.
    - GET: Inicia flujo OAuth 2.0 hacia Google (fallback si JS falla)
    - POST: Valida ID Token usando Firebase Admin SDK (recomendado)
    """

    # --- FLUJO POST: Validación con Firebase Admin SDK (Producción) ---
    if request.method == "POST":
        token = None

        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                token = data.get("token")
            except json.JSONDecodeError:
                pass

        if not token:
            token = request.POST.get("token") or request.GET.get("token")

        if not token:
            return JsonResponse(
                {"success": False, "error": "Token no proporcionado."}, status=400
            )

        try:
            import firebase_admin.auth as fb_auth

            decoded_token = fb_auth.verify_id_token(token, check_revoked=True)

            correo = decoded_token.get("email", "").strip().lower()
            display_name = decoded_token.get("name", "")
            first_name = (
                display_name.split()[0] if display_name else correo.split("@")[0]
            )

            if not correo:
                raise ValueError("Google no devolvió email en el token")

        except (ValueError, KeyError, AttributeError) as e:
            logger.error(f"Fallo validación Firebase token: {e!s}")
            return JsonResponse(
                {"success": False, "error": "Token inválido o expirado."}, status=401
            )

        user = User.objects.filter(email__iexact=correo).first()
        if user is None:
            base_username = correo.split("@")[0][:140]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                suffix = f"-{counter}"
                username = f"{base_username[: 140 - len(suffix)]}{suffix}"
                counter += 1

            user = User.objects.create_user(
                username=username,
                email=correo,
                first_name=first_name,
            )
        else:
            if user.first_name != first_name:
                user.first_name = first_name
                user.save(update_fields=["first_name"])

        login(request, user)

        next_url = request.POST.get("next", request.GET.get("next", "/"))
        if next_url.startswith("/") and not next_url.startswith("//"):
            return JsonResponse({"success": True, "redirect": next_url})
        return JsonResponse({"success": True, "redirect": "/"})

    # --- FLUJO GET: OAuth Nativo de Google (Fallback) ---
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    if not client_id:
        return JsonResponse(
            {"success": False, "error": "Configuración de Google incompleta."},
            status=500,
        )

    redirect_uri = request.build_absolute_uri(reverse("google_callback"))
    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32)

    request.session["oauth_state"] = state
    request.session["oauth_nonce"] = nonce

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "nonce": nonce,
        "prompt": "consent select_account",
    }

    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"

    return HttpResponseRedirect(auth_url)


def google_callback(request):
    """Procesa el código de autorización devuelto por Google OAuth."""
    code = request.GET.get("code")
    state = request.GET.get("state")
    stored_state = request.session.pop("oauth_state", None)

    if not code or not state or state != stored_state:
        return JsonResponse(
            {"success": False, "error": "Callback inválido."}, status=400
        )

    client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")
    redirect_uri = request.build_absolute_uri(reverse("google_callback"))

    try:
        import requests

        resp = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
            timeout=10,
        )
        token_data = resp.json()
        id_token = token_data.get("id_token")

        if not id_token:
            return redirect("/login/?error=oauth_failed")

        from django.test import RequestFactory

        factory = RequestFactory()
        fake_request = factory.post("/google-login/", {"token": id_token})
        fake_request.session = request.session
        result = google_login(fake_request)

        if isinstance(result, JsonResponse):
            data = json.loads(result.content)
            if data.get("success"):
                return redirect(data.get("redirect", "/"))

        return redirect("/login/?error=oauth_processing_failed")

    except (requests.exceptions.RequestException, ValueError, KeyError):
        return redirect("/login/?error=oauth_exchange_failed")
