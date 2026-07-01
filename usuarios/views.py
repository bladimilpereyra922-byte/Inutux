from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto, Categoria, Carrito, ItemCarrito, Proveedor, Reporte

def inicio(request):
    busqueda = request.GET.get('q', '')
    productos = Producto.objects.filter(activo=True)
    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)
    categorias = Categoria.objects.all()
    return render(request, 'tienda/inicio.html', {
        'productos': productos,
        'categorias': categorias,
        'busqueda': busqueda
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

@login_required
def panel_proveedor(request):
    try:
        proveedor = request.user.proveedor
        if proveedor.estado != 'aprobado':
            return render(request, 'tienda/pendiente.html')
        productos = Producto.objects.filter(proveedor=proveedor)
        return render(request, 'tienda/panel_proveedor.html', {
            'proveedor': proveedor,
            'productos': productos
        })
    except:
        return redirect('registro_proveedor')

@login_required
def registro_proveedor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_tienda')
        descripcion = request.POST.get('descripcion')
        telefono = request.POST.get('telefono')
        Proveedor.objects.create(
            usuario=request.user,
            nombre_tienda=nombre,
            descripcion=descripcion,
            telefono=telefono
        )
        return redirect('panel_proveedor')
    return render(request, 'tienda/registro_proveedor.html')

@login_required
def chat_soporte(request):
    respuesta = None
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor_id')
        mensaje = request.POST.get('mensaje')
        proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
        Reporte.objects.create(
            cliente=request.user,
            proveedor=proveedor,
            mensaje=mensaje
        )
        respuesta = 'Gracias por tu reporte. Hemos recibido tu queja sobre ' + proveedor.nombre_tienda + ' y el equipo de Inutux la revisara pronto.'
    proveedores = Proveedor.objects.filter(estado='aprobado')
    return render(request, 'tienda/chat_soporte.html', {
        'proveedores': proveedores,
        'respuesta': respuesta
    })