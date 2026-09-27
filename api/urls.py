from django.urls import path
from . import views

urlpatterns = [
    path("notifications/", views.get_notifications, name="api_notifications"),
    path("apply-promo/", views.apply_promo, name="api_apply_promo"),
]
