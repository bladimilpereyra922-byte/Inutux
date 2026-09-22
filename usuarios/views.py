import json
import os

import requests
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from requests.exceptions import RequestException


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
            return redirect("inicio")
    else:
        form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("inicio")


@require_POST
def google_login(request):
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
    return JsonResponse({"success": True, "redirect": "/"})