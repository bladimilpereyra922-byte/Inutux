from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health, name="api_health"),
    path("productos/", views.productos, name="api_productos"),
]
