from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto, Categoria, Carrito, ItemCarrito

def inicio(request):
    productos = Producto.objects.filter(activo=True)
    categorias = Categoria.objects.all()
    return render(request, 'tienda/inicio.html', {
        'productos': productos,
        'categorias': categorias
    })

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    return render(request, 'tienda/detalle.html', {
        'producto': producto
    })

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