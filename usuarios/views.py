from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt  # <-- IMPORTANTE: Nueva importación

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

# --- NUEVA VISTA PARA GOOGLE EXENTA DE CSRF ---
@csrf_exempt
def google_login(request):
    if request.method == 'POST':
        # Aquí va tu lógica actual para procesar el token de Google
        # Por ahora te redirige a inicio al recibir los datos de forma segura
        return redirect('inicio')
    return redirect('login')