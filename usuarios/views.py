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
    codigo_google = request.GET.get('code')
    if not codigo_google:
        return JsonResponse({'success': False, 'error': 'No se recibio el codigo de Google'}, status=400)

    # 👇 Tu ID de Google que ya funciona nítido
    client_id = '1001380630801-h5nsvp8tm1b9dgv05cd49d0gq96u0kkf.apps.googleusercontent.com'
    
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    redirect_uri = request.build_absolute_uri('/google-login/')

    try:
        token_response = requests.post('https://oauth2.googleapis.com/token', data={
            'code': codigo_google,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        })
        
        datos_token = token_response.json()
        access_token = datos_token.get('access_token')
        
        if not access_token:
            return JsonResponse({'success': False, 'error': 'No se pudo obtener el access token', 'detalle': datos_token}, status=400)

        user_data = requests.get('https://www.googleapis.com/oauth2/v2/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}).json()

        correo = user_data.get('email')
        if correo:
            user, created = User.objects.get_or_create(
                email=correo,
                defaults={'username': correo.split('@')[0], 'first_name': user_data.get('given_name', '')}
            )
            login(request, user)
            return redirect('inicio')
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
 
    return redirect('login')