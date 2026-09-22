from django.core.exceptions import PermissionDenied


class ProductoPermission:

    @staticmethod
    def puede_crear(usuario):
        if not usuario.is_authenticated:
            raise PermissionDenied(
                "Debe iniciar sesión."
            )

        return True

    @staticmethod
    def puede_editar(usuario, producto):
        if usuario.is_superuser:
            return True

        if (
            hasattr(usuario, "proveedor")
            and producto.proveedor.usuario_id == usuario.id
        ):
            return True

        raise PermissionDenied(
            "No tiene permisos para editar este producto."
        )

    @staticmethod
    def puede_eliminar(usuario, producto):
        return ProductoPermission.puede_editar(
            usuario,
            producto,
        )

    @staticmethod
    def puede_publicar(usuario):
        if usuario.is_superuser:
            return True

        if hasattr(usuario, "proveedor"):
            return True

        raise PermissionDenied(
            "No tiene permisos para publicar productos."
        )

    @staticmethod
    def puede_ver_borradores(usuario):
        if usuario.is_superuser:
            return True

        if hasattr(usuario, "proveedor"):
            return True

        raise PermissionDenied(
            "No tiene permisos para visualizar borradores."
        )