import json
import os
import secrets

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import firebase_admin.auth


def registro(request):
    """Registro seguro con UserCreationForm est�ndar de Django."""
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
    """Login tradicional con protecci�n CSRF impl�cita por Django."""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get("next", "/")
            # Prevenci�n de Open Redirect
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
        "orders": [],  # TODO: Pedido.objects.filter(usuario=request.user)
        "favorites": [],  # TODO: Favorito.objects.filter(usuario=request.user)
    }
    return render(request, "usuarios/perfil.html", context)


def logout_view(request):
    """Cierra sesi�n y redirige al inicio."""
    from django.contrib.auth import logout

    logout(request)
    return redirect("inicio")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def google_login(request):
    """
    Flujo dual seguro de Google Auth optimizado para producci�n.
    - GET: Inicia flujo OAuth 2.0 hacia Google (fallback si JS falla)
    - POST: Valida ID Token usando Firebase Admin SDK (recomendado)
    """

    # --- FLUJO POST: Validaci�n con Firebase Admin SDK (Producci�n) ---
    if request.method == "POST":
        token = None

        # Extraer token de form data o JSON body
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
            # Usar Firebase Admin SDK para verificaci�n segura
            import firebase_admin.auth as fb_auth

            decoded_token = fb_auth.verify_id_token(token, check_revoked=True)

            correo = decoded_token.get("email", "").strip().lower()
            display_name = decoded_token.get("name", "")
            first_name = (
                display_name.split()[0] if display_name else correo.split("@")[0]
            )

            if not correo:
                raise ValueError("Google no devolvi� email en el token")

        except (ValueError, KeyError, firebase_admin.auth.InvalidIdTokenError) as e:
            # Log del error real para debugging en producci�n
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Fallo validaci�n Firebase token: {e!s}")

            return JsonResponse(
                {"success": False, "error": "Token inv�lido o expirado."}, status=401
            )

        # Crear o actualizar usuario Django
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
            # Actualizar nombre si cambi� en Google
            if user.first_name != first_name:
                user.first_name = first_name
                user.save(update_fields=["first_name"])

        # Login seguro
        login(request, user)

        # Redirecci�n segura post-login
        next_url = request.POST.get("next", request.GET.get("next", "/"))
        if next_url.startswith("/") and not next_url.startswith("//"):
            return JsonResponse({"success": True, "redirect": next_url})
        return JsonResponse({"success": True, "redirect": "/"})

    # --- FLUJO GET: OAuth Nativo de Google (Fallback) ---
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    if not client_id:
        return JsonResponse(
            {"success": False, "error": "Configuraci�n de Google incompleta."},
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
    """Procesa el c�digo de autorizaci�n devuelto por Google OAuth."""
    code = request.GET.get("code")
    state = request.GET.get("state")
    stored_state = request.session.pop("oauth_state", None)

    if not code or not state or state != stored_state:
        return JsonResponse(
            {"success": False, "error": "Callback inv�lido."}, status=400
        )

    # Intercambiar c�digo por ID token usando Google Token Endpoint
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

        # Reutilizar la l�gica de validaci�n existente haciendo un POST interno simulado
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
