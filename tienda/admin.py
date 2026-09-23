from django.contrib import admin

from .models import ConfiguracionTienda


@admin.register(ConfiguracionTienda)
class ConfiguracionTiendaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo", "creado_en")
    search_fields = ("nombre",)
