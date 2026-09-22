from django.contrib import admin

from .models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_tienda",
        "usuario",
        "estado",
        "activo",
        "verificado",
    )

    list_filter = (
        "estado",
        "activo",
        "verificado",
    )

    search_fields = (
        "nombre_tienda",
        "usuario__username",
        "usuario__email",
    )

    prepopulated_fields = {
        "slug": ("nombre_tienda",),
    }

    ordering = (
        "nombre_tienda",
    )