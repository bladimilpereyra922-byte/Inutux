from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tienda import views
from usuarios import views as usuarios_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle'),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/agregar/<int:pk>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/eliminar/<int:pk>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('registro/', usuarios_views.registro, name='registro'),
    path('login/', usuarios_views.login_view, name='login'),
    path('logout/', usuarios_views.logout_view, name='logout'),
    path('proveedor/', views.panel_proveedor, name='panel_proveedor'),
    path('proveedor/registro/', views.registro_proveedor, name='registro_proveedor'),
    path('soporte/', views.chat_soporte, name='chat_soporte'),
    path('pago/', views.pago, name='pago'),
    path('google-login/', usuarios_views.google_login, name='google_login'),
]

# 👇 ESTO ES LO QUE FALTA: Le dice a Django que sirva las imágenes en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)