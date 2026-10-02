import json
import logging
import os
import secrets
from datetime import timedelta

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


def registro(request):
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
    if not request.user.is_authenticated:
        return redirect("login")
    context = {
        "user": request.user,
        "orders": [],
        "favorites": [],
    }
    return render(request, "usuarios/perfil.html", context)


def recuperar_password(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        user = User.objects.filter(email__iexact=email).first()
        if user:
            token = secrets.token_urlsafe(32)
            request.session["reset_token"] = {
                "uid": user.pk,
                "token": token,
                "expires": (timezone.now() + timedelta(hours=1)).isoformat(),
            }
            msg = "Si el correo esta registrado, recibiras instrucciones."
        else:
            msg = "Si el correo esta registrado, recibiras instrucciones."
        return render(request, "usuarios/recuperar_password.html", {"message": msg})
    return render(request, "usuarios/recuperar_password.html")


def reset_password_confirm(request, uidb64, token):
    return render(request, "usuarios/reset_password_confirm.html")


def logout_view(request):
    logout(request)
    return redirect("inicio")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def google_login(request):
    """Procesa token de Firebase Auth y crea sesión Django."""
    if request.method != "POST":
        return JsonResponse({"error": "Metodo no permitido"}, status=405)

    try:
        data = json.loads(request.body)
        id_token = data.get("token")

        if not id_token:
            return JsonResponse({"error": "Token no proporcionado"}, status=400)

        import firebase_admin.auth as fb_auth
        from firebase_admin.exceptions import FirebaseError

        decoded_token = fb_auth.verify_id_token(id_token, check_revoked=True)
        firebase_uid = decoded_token["uid"]
        email = decoded_token.get("email", "")
        name = decoded_token.get("name", email.split("@")[0])

        user, created = User.objects.get_or_create(
            username=firebase_uid,
            defaults={"email": email, "first_name": name},
        )

        if not created and (user.email != email or user.first_name != name):
            user.email = email
            user.first_name = name
            user.save(update_fields=["email", "first_name"])

        login(request, user)

        return JsonResponse(
            {
                "success": True,
                "redirect": "/perfil/",
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                },
            }
        )

    except (ValueError, KeyError, FirebaseError) as e:
        logger.error(f"Error en google_login: {e!s}")
        return JsonResponse({"error": str(e), "success": False}, status=401)


def google_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    stored_state = request.session.pop("oauth_state", None)

    if not code or not state or state != stored_state:
        return JsonResponse(
            {"success": False, "error": "Callback invalido."}, status=400
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
