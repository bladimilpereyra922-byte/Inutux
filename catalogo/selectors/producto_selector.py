from django.db.models import Prefetch

from catalogo.models import Producto


class ProductoSelector:

    @staticmethod
    def obtener(pk):
        return (
            Producto.objects
            .select_related(
                "categoria",
                "proveedor",
            )
            .prefetch_related(
                "variantes",
                "multimedia",
            )
            .get(pk=pk)
        )

    @staticmethod
    def listar_activos():
        return (
            Producto.objects
            .activos()
            .select_related(
                "categoria",
                "proveedor",
            )
        )

    @staticmethod
    def listar_destacados():
        return (
            Producto.objects
            .destacados()
            .select_related(
                "categoria",
                "proveedor",
            )
        )

    @staticmethod
    def buscar(texto):
        return (
            Producto.objects
            .buscar(texto)
            .select_related(
                "categoria",
                "proveedor",
            )
        )

    @staticmethod
    def por_categoria(categoria):
        return (
            Producto.objects
            .categoria(categoria)
            .select_related(
                "categoria",
                "proveedor",
            )
        )

    @staticmethod
    def por_proveedor(proveedor):
        return (
            Producto.objects
            .proveedor(proveedor)
            .select_related(
                "categoria",
                "proveedor",
            )
        )