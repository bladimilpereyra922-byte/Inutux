from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from catalogo.models import Producto


@receiver(pre_save, sender=Producto)
def generar_slug_producto(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.nombre)


@receiver(post_save, sender=Producto)
def producto_guardado(sender, instance, created, **kwargs):
    if created:
        print(f"[CATALOGO] Producto creado: {instance.nombre}")
    else:
        print(f"[CATALOGO] Producto actualizado: {instance.nombre}")