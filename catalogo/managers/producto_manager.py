from django.db import models


class ProductoQuerySet(models.QuerySet):

    def activos(self):
        return self.filter(activo=True)

    def inactivos(self):
        return self.filter(activo=False)

    def destacados(self):
        return self.filter(destacado=True)

    def disponibles(self):
        return self.filter(
            activo=True,
            stock__gt=0,
        )

    def digitales(self):
        return self.filter(digital=True)

    def fisicos(self):
        return self.filter(digital=False)

    def categoria(self, categoria):
        return self.filter(categoria=categoria)

    def proveedor(self, proveedor):
        return self.filter(proveedor=proveedor)

    def buscar(self, texto):
        return self.filter(
            models.Q(nombre__icontains=texto)
            | models.Q(descripcion__icontains=texto)
            | models.Q(sku__icontains=texto)
        )

    def con_stock(self):
        return self.filter(stock__gt=0)

    def sin_stock(self):
        return self.filter(stock=0)

    def baratos(self):
        return self.order_by("precio")

    def caros(self):
        return self.order_by("-precio")

    def recientes(self):
        return self.order_by("-creado")


class ProductoManager(models.Manager):

    def get_queryset(self):
        return ProductoQuerySet(
            self.model,
            using=self._db,
        )

    def activos(self):
        return self.get_queryset().activos()

    def inactivos(self):
        return self.get_queryset().inactivos()

    def disponibles(self):
        return self.get_queryset().disponibles()

    def destacados(self):
        return self.get_queryset().destacados()

    def digitales(self):
        return self.get_queryset().digitales()

    def fisicos(self):
        return self.get_queryset().fisicos()

    def categoria(self, categoria):
        return self.get_queryset().categoria(categoria)

    def proveedor(self, proveedor):
        return self.get_queryset().proveedor(proveedor)

    def buscar(self, texto):
        return self.get_queryset().buscar(texto)

    def con_stock(self):
        return self.get_queryset().con_stock()

    def sin_stock(self):
        return self.get_queryset().sin_stock()

    def baratos(self):
        return self.get_queryset().baratos()

    def caros(self):
        return self.get_queryset().caros()

    def recientes(self):
        return self.get_queryset().recientes()