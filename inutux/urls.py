from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from carrito import views as carrito_views
from pagos import views as pagos_views
from proveedores import views as proveedores_views
from soporte import views as soporte_views
from tienda import views as catalogo_views
from usuarios import views as usuarios_views

urlpatterns = [
    path("api/", include("api.urls")),
    path("admin/", admin.site.urls),

    # Inicio
    path("", catalogo_views.inicio, name="inicio"),

    # Productos
    path(
        "producto/<int:pk>/",
        catalogo_views.detalle_producto,
        name="detalle",
    ),

    # Carrito
    path(
        "carrito/",
        carrito_views.ver_carrito,
        name="carrito",
    ),
    path(
        "carrito/agregar/<int:pk>/",
        carrito_views.agregar_carrito,
        name="agregar_carrito",
    ),
    path(
        "carrito/eliminar/<int:pk>/",
        carrito_views.eliminar_carrito,
        name="eliminar_carrito",
    ),

    # Usuarios
    path("registro/", usuarios_views.registro, name="registro"),
    path("login/", usuarios_views.login_view, name="login"),
    path("logout/", usuarios_views.logout_view, name="logout"),
    path("google-login/", usuarios_views.google_login, name="google_login"),

    # Proveedores
    path(
        "proveedor/",
        proveedores_views.panel_proveedor,
        name="panel_proveedor",
    ),
    path(
        "proveedor/registro/",
        proveedores_views.registro_proveedor,
        name="registro_proveedor",
    ),

    # Soporte
    path(
    "soporte/",
    soporte_views.chat_soporte,
    name="chat_soporte",
),

    # Pago
    path(
        "pago/",
        pagos_views.pago,
        name="pago",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
