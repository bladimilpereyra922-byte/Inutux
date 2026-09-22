from pathlib import Path

from inspector.core.base import AgentBase


class DatabaseAgent(AgentBase):

    name = "database"
    description = "Auditoría de Base de Datos"

    def execute(self):

        info = []
        warnings = []
        errors = []

        settings_files = list(self.root.rglob("settings.py"))

        if not settings_files:
            return self.error(
                "No se encontró ningún settings.py",
                ["No existe configuración de Django"],
            )

        db_found = False

        for settings in settings_files:

            try:
                content = settings.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                if "DATABASES" in content:
                    db_found = True
                    info.append(f"DATABASES encontrado en {settings.name}")

                    if "sqlite3" in content.lower():
                        info.append("Motor SQLite detectado")

                    if "postgresql" in content.lower() or "psycopg" in content.lower():
                        info.append("Motor PostgreSQL detectado")

                    if "mysql" in content.lower():
                        info.append("Motor MySQL detectado")

            except Exception as e:
                warnings.append(str(e))

        if not db_found:
            errors.append("No existe configuración DATABASES")

        migrations = list(self.root.rglob("migrations"))

        info.append(f"Migraciones encontradas: {len(migrations)}")

        if errors:
            return self.error(
                "Problemas encontrados en la base de datos.",
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
            "Base de datos validada correctamente.",
            info,
        )