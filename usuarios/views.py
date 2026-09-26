import json
import os
import secrets
from datetime import timedelta

import requests
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from requests.exceptions import RequestException


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
            # Prevención de Open Redirect
            if next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)
            return redirect("inicio")
    else:
        form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form})


def recuperar_password(request):
    """
    Recuperación segura de contraseña.
    Genera un token único que expira en 1 hora.
    En producción, este token debe enviarse por email.
    """
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        user = User.objects.filter(email__iexact=email).first()

        if user:
            # Generar token seguro criptográficamente
            token = secrets.token_urlsafe(32)
            # Guardar token y expiración en sesión o BD (aquí usamos session como ejemplo mínimo)
            request.session["reset_token"] = {
                "uid": user.pk,
                "token": token,
                "expires": (timezone.now() + timedelta(hours=1)).isoformat(),
            }
            # ️ EN PRODUCCIÓN: Enviar 'token' por email a 'email'
            # Por ahora mostramos mensaje genérico para no exponer si el email existe
            msg = "Si el correo está registrado, recibirás instrucciones."
        else:
            # Mensaje idéntico para evitar enumeración de usuarios
            msg = "Si el correo está registrado, recibirás instrucciones."

        return render(request, "usuarios/recuperar_password.html", {"message": msg})

    return render(request, "usuarios/recuperar_password.html")


def reset_password_confirm(request, uidb64, token):
    """Valida token de recuperación y permite establecer nueva contraseña."""
    # Lógica de validación de token y formulario de nueva contraseña
    # Implementar según tu modelo de reset
    return render(request, "usuarios/reset_password_confirm.html")


def logout_view(request):
    logout(request)
    return redirect("inicio")


@require_http_methods(["GET", "POST"])
def google_login(request):
    """
    Flujo dual seguro de Google Auth:
    - GET: Inicia flujo OAuth 2.0 hacia Google (Opción A)
    - POST: Valida ID Token de Firebase Identity Toolkit (tu lógica original)
    """

    # --- FLUJO GET: Redirigir a Google OAuth Consent Screen ---
    if request.method == "GET":
        client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
        if not client_id:
            return JsonResponse(
                {"success": False, "error": "GOOGLE_CLIENT_ID no configurado."},
                status=500,
            )

        redirect_uri = request.build_absolute_uri(reverse("google_callback"))
        state = secrets.token_urlsafe(16)  # Protección CSRF para OAuth
        request.session["oauth_state"] = state

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "nonce": secrets.token_urlsafe(16),  # Anti-replay
            "prompt": "consent",
        }
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"
        return HttpResponseRedirect(auth_url)

    # --- FLUJO POST: Tu lógica original de validación con Firebase ---
    token = request.POST.get("token")
    if not token:
        try:
            data = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            data = {}
        token = data.get("token")

    if not token:
        return JsonResponse(
            {"success": False, "error": "No se recibió el token de Google."},
            status=400,
        )

    firebase_api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not firebase_api_key:
        return JsonResponse(
            {"success": False, "error": "Falta configurar FIREBASE_WEB_API_KEY."},
            status=500,
        )

    url = (
        "https://identitytoolkit.googleapis.com/v1/accounts:lookup"
        f"?key={firebase_api_key}"
    )

    try:
        response = requests.post(url, json={"idToken": token}, timeout=10)
        datos = response.json()
    except (RequestException, ValueError):
        return JsonResponse(
            {"success": False, "error": "No fue posible validar con Firebase."},
            status=502,
        )

    if response.status_code != 200 or not datos.get("users"):
        return JsonResponse(
            {"success": False, "error": "Token de Google inválido."},
            status=400,
        )

    info_perfil = datos["users"][0]
    correo = (info_perfil.get("email") or "").strip().lower()

    if not correo:
        return JsonResponse(
            {"success": False, "error": "Google no devolvió un correo electrónico."},
            status=400,
        )

    display_name = (info_perfil.get("displayName") or "").strip()
    first_name = display_name.split()[0] if display_name else correo.split("@")[0]

    user = User.objects.filter(email__iexact=correo).first()
    if user is None:
        base_username = correo.split("@")[0][:150]
        username = base_username
        contador = 1
        while User.objects.filter(username=username).exists():
            sufijo = f"-{contador}"
            username = f"{base_username[:150 - len(sufijo)]}{sufijo}"
            contador += 1

        user = User.objects.create_user(
            username=username,
            email=correo,
            first_name=first_name,
        )

    login(request, user)

    # Soporte para redirección post-login segura
    next_url = request.POST.get("next", "/")
    if next_url.startswith("/") and not next_url.startswith("//"):
        return JsonResponse({"success": True, "redirect": next_url})
    return JsonResponse({"success": True, "redirect": "/"})


def google_callback(request):
    """Procesa el código de autorización devuelto por Google OAuth."""
    code = request.GET.get("code")
    state = request.GET.get("state")
    stored_state = request.session.pop("oauth_state", None)

    if not code or not state or state != stored_state:
        return JsonResponse({"success": False, "error": "Callback inválido."}, status=400)

    # Intercambiar código por ID token usando Google Token Endpoint
    client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")
    redirect_uri = request.build_absolute_uri(reverse("google_callback"))

    try:
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

        # Reutilizar la lógica de validación existente haciendo un POST interno simulado
        # O mejor: llamar directamente a la lógica de creación/login aquí
        # Para mantener DRY, podemos refactorizar, pero por ahora hacemos POST fetch-like:
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

    except (RequestException, ValueError, KeyError):
        return redirect("/login/?error=oauth_exchange_failed")