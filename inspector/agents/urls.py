from pathlib import Path

from inspector.core.base import AgentBase


class UrlsAgent(AgentBase):

    name = "urls"
    description = "Auditoría de URLs Django"

    EXCLUDED = {
        "venv",
        ".venv",
        ".git",
        "__pycache__",
        "site-packages",
        "node_modules",
        "dist",
        "build",
        ".pytest_cache",
        "tools",
        "scripts",
        "docs",
        "logs",
        "reports",
        "config",
        "inspector",
    }

    def execute(self):

        info = []
        warnings = []
        errors = []

        url_files = []

        for file in self.root.rglob("urls.py"):

            if any(part in self.EXCLUDED for part in file.parts):
                continue

            # Solo revisar apps Django reales
            app_folder = file.parent

            if (
                file.name != "urls.py"
                or (
                    not (app_folder / "apps.py").exists()
                    and file.parent.name != "inutux"
                )
            ):
                continue

            url_files.append(file)

        if not url_files:
            return self.error(
                "No se encontraron archivos urls.py",
                ["No existe ningún urls.py válido"],
            )

        info.append(f"Archivos urls.py: {len(url_files)}")

        total_paths = 0
        total_includes = 0

        for file in sorted(url_files):

            try:

                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                paths = (
                    content.count("path(")
                    + content.count("re_path(")
                )

                includes = content.count("include(")

                total_paths += paths
                total_includes += includes

                info.append(
                    f"{file.parent.name}: {paths} rutas"
                )

                if (
                    paths > 0
                    and "urlpatterns" not in content
                ):
                    warnings.append(
                        f"{file.parent.name}: urlpatterns no encontrado"
                    )

            except Exception as e:
                errors.append(str(e))

        info.append(f"Total rutas: {total_paths}")
        info.append(f"Includes: {total_includes}")

        if errors:
            return self.error(
                "Errores encontrados en URLs.",
                errors,
                info,
            )

        if warnings:
            return self.warning(
                "Advertencias encontradas.",
                warnings,
                info,
            )

        return self.ok(
            "URLs validadas correctamente.",
            info,
        )