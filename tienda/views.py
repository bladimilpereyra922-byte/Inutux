from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse
from .models import Producto, Categoria, Carrito, ItemCarrito, Proveedor, Reporte
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import os
import json

# Inicialización segura de Firebase Admin SDK para Render y Local
if not firebase_admin._apps:
    firebase_key = os.environ.get('FIREBASE_KEY')
    
    if firebase_key:
        try:
            # Render: Cargamos el JSON desde la variable de entorno
            cred_dict = json.loads(firebase_key)
            cred = credentials.Certificate(cred_dict)
        except Exception as e:
            raise ValueError(f"Error al procesar la variable FIREBASE_KEY: {e}")
    else:
        # Local: Si no existe la variable, busca el archivo físico
        ruta_local = 'unitux-c7b8b-firebase-adminsdk-fbsvc-21553d0c90.json'
        if os.path.exists(ruta_local):
            cred = credentials.Certificate(ruta_local)
        elif os.path.exists('firebase-key.json'):
            cred = credentials.Certificate('firebase-key.json')
        else:
            raise FileNotFoundError("No se encontró la variable FIREBASE_KEY ni el archivo JSON local de Firebase.")

    firebase_admin.initialize_app(cred)

def inicio(request):
    busqueda = request.GET.get('q', '')
    productos = Producto.objects.filter(activo=True)
    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)
    categorias = Categoria.objects.all()
    return render(request, 'tienda/inicio.html', {'productos': productos, 'categorias': categorias, 'busqueda': busqueda})

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    return render(request, 'tienda/detalle.html', {'producto': producto})

@login_required
def agregar_carrito(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not creado:
        item.cantidad += 1
        item.save()
    return redirect('carrito')

@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, 'tienda/carrito.html', {'carrito': carrito})

@login_required
def eliminar_carrito(request, pk):
    item = get_object_or_404(ItemCarrito, pk=pk, carrito__usuario=request.user)
    item.delete()
    return redirect('carrito')

@login_required
def panel_proveedor(request):
    try:
        proveedor = request.user.proveedor
        if proveedor.estado != 'aprobado':
            return render(request, 'tienda/pendiente.html')
        productos = Producto.objects.filter(proveedor=proveedor)
        return render(request, 'tienda/panel_proveedor.html', {'proveedor': proveedor, 'productos': productos})
    except:
        return redirect('registro_proveedor')

@login_required
def registro_proveedor(request):
    if request.method == 'POST':
        Proveedor.objects.create(
            usuario=request.user,
            nombre_tienda=request.POST.get('nombre_tienda'),
            descripcion=request.POST.get('descripcion'),
            telefono=request.POST.get('telefono')
        )
        return redirect('panel_proveedor')
    return render(request, 'tienda/registro_proveedor.html')

@login_required
def chat_soporte(request):
    respuesta = None
    if request.method == 'POST':
        proveedor = get_object_or_404(Proveedor, pk=request.POST.get('proveedor_id'))
        Reporte.objects.create(cliente=request.user, proveedor=proveedor, mensaje=request.POST.get('mensaje'))
        respuesta = 'Gracias por tu reporte. Hemos recibido tu queja sobre ' + proveedor.nombre_tienda + ' y el equipo de Unitux la revisara pronto.'
    proveedores = Proveedor.objects.filter(estado='aprobado')
    return render(request, 'tienda/chat_soporte.html', {'proveedores': proveedores, 'respuesta': respuesta})

@login_required
def pago(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    
    # 👇 Reemplaza esta parte: Calculamos el total y lo formateamos estrictamente con punto decimal
    total_calculado = carrito.total()
    total_formateado = "{:.2f}".format(total_calculado) if total_calculado else "0.00"
    
    return render(request, 'tienda/pago.html', {'total': total_formateado})