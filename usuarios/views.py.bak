import os
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('inicio')

def google_login(request):
    # Ahora Django recibe el token de autenticación que genera Firebase en el navegador
    id_token = request.GET.get('token')
    if not id_token:
        return JsonResponse({'success': False, 'error': 'No se recibió el token de Firebase'}, status=400)

    # El ID de tu proyecto Firebase
    firebase_project_id = "unitux-c7b8b"
    
    try:
        # Validamos el token directamente con la API oficial de Firebase para total seguridad
        url_verificar = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={os.environ.get('GOOGLE_CLIENT_SECRET')}"
        response = requests.post(url_verificar, json={"idToken": id_token})
        datos_usuario = response.json()
        
        if 'users' not in datos_usuario:
            return JsonResponse({'success': False, 'error': 'Token de Firebase inválido', 'detalle': datos_usuario}, status=400)
        
        info_perfil = datos_usuario['users'][0]
        correo = info_perfil.get('email')
        
        if correo:
            # Buscamos el usuario en tu base de datos o lo creamos si es nuevo
            user, created = User.objects.get_or_create(
                email=correo,
                defaults={
                    'username': correo.split('@')[0], 
                    'first_name': info_perfil.get('displayName', '').split(' ')[0]
                }
            )
            # Iniciamos sesión en Django de forma segura
            login(request, user)
            return redirect('inicio')
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
 
    return redirect('login')