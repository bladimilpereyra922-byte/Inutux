from django.apps import AppConfig


class ProveedoresConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "proveedores"
    verbose_name = "Proveedores"

    def ready(self):
        try:
            import proveedores.signals  # noqa: F401
        except ImportError:
            pass