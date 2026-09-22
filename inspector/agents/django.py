from pathlib import Path

from inspector.core.base import AgentBase


class DjangoAgent(AgentBase):

    name = "django"
    description = "Auditoría de Django"

    def execute(self):

        info = []
        warnings = []
        errors = []

        files = {
            "manage.py": "manage.py",
            "requirements.txt": "requirements.txt",
        }

        for file, label in files.items():

            if (self.root / file).exists():
                info.append(f"{label} encontrado")
            else:
                errors.append(f"{label} no encontrado")

        settings = list(self.root.rglob("settings.py"))

        if settings:
            info.append(f"settings.py encontrado ({len(settings)})")
        else:
            errors.append("No se encontró settings.py")

        urls = list(self.root.rglob("urls.py"))

        if urls:
            info.append(f"urls.py encontrados ({len(urls)})")
        else:
            warnings.append("No se encontraron urls.py")

        apps = []

        for folder in self.root.iterdir():
            if folder.is_dir() and (folder / "apps.py").exists():
                apps.append(folder.name)

        info.append(f"Apps Django: {len(apps)}")

        migrations = list(self.root.rglob("migrations"))

        info.append(f"Carpetas migrations: {len(migrations)}")

        if errors:
            return self.error(
                "Se encontraron errores en la estructura Django.",
                errors,
                info,
            )

        if warnings:
            return self.warning(
                "Se encontraron advertencias.",
                warnings,
                info,
            )

        return self.ok(
            "Proyecto Django validado correctamente.",
            info,
        )