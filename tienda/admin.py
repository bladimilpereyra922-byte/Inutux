from django.contrib import admin
from .models import Proveedor, Categoria, Producto, Reporte

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

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'proveedor', 'estado', 'fecha']
    list_filter = ['estado']
    actions = ['marcar_revisado', 'marcar_resuelto']

    def marcar_revisado(self, request, queryset):
        queryset.update(estado='revisado')
    marcar_revisado.short_description = 'Marcar como revisado'

    def marcar_resuelto(self, request, queryset):
        queryset.update(estado='resuelto')
    marcar_resuelto.short_description = 'Marcar como resuelto'