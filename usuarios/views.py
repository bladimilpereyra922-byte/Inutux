import os
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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

# --- VISTA PROCESADORA DE GOOGLE (BLINDADA Y SEGURA) ---
def google_login(request):
    # 1. Capturamos el código que Google nos manda por la URL
    codigo_google = request.GET.get('code')
    
    if not codigo_google:
        redirect_uri = 'https://inutux.onrender.com/google-login/'
    
    # 2. Configura los datos. Nota cómo el Secreto ahora se lee de forma segura desde el sistema operativo
    client_id = '551444650101-5opam7p1psqlu7ucc3k2d9ipvtak5ii3.apps.googleusercontent.com'
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')  # <--- PROTEGIDO CON VARIABLE DE ENTORNO
    
    redirect_uri = 'https://inutux.onrender.com/google-login/'
    token_url = 'https://oauth2.googleapis.com/token'
    
    payload = {
        'code': codigo_google,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    
    try:
        # 3. Intercambio interno y seguro con los servidores de Google
        token_response = requests.post(token_url, data=payload)
        token_data = token_response.json()
        access_token = token_data.get('access_token')
        
        if not access_token:
            return HttpResponse(f"Error al obtener token de Google. Respuesta: {token_data}", status=400)
        
        # 4. Solicitamos la información del perfil del usuario a Google
        user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        user_info_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})
        user_data = user_info_response.json()
        
        correo = user_data.get('email')
        nombre = user_data.get('given_name', 'UsuarioGoogle')
        
        if correo:
            # 5. Buscamos al usuario en la base de datos por su correo o lo registramos de forma automática
            user, created = User.objects.get_or_create(email=correo, defaults={
                'username': correo.split('@')[0],  
                'first_name': nombre
            })
            
            # 6. Iniciamos la sesión en el servidor para dar paso a la tienda
            login(request, user)
            return redirect('inicio')  
            
    except Exception as e:
        return HttpResponse(f"Fallo crítico en el servidor de autenticación: {str(e)}", status=500)
        
    return redirect('login')