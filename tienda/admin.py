from django.contrib import admin
from .models import Proveedor, Categoria, Producto

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre_tienda', 'usuario', 'estado', 'comision', 'fecha_registro']
    list_filter = ['estado']
    actions = ['aprobar', 'bloquear']

    def aprobar(self, request, queryset):
        queryset.update(estado='aprobado')
    aprobar.short_description = 'Aprobar proveedores seleccionados'

    def bloquear(self, request, queryset):
        queryset.update(estado='bloqueado')
    bloquear.short_description = 'Bloquear proveedores seleccionados'

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'proveedor', 'precio', 'stock', 'activo']
    list_filter = ['activo', 'categoria']

# Register your models here.``
