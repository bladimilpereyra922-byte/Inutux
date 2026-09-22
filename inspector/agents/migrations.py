from pathlib import Path

from inspector.core.base import AgentBase


class MigrationsAgent(AgentBase):

    name = "migrations"
    description = "Auditoría de Migraciones Django"

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
    }

    def execute(self):

        info = []
        warnings = []
        errors = []

        migration_dirs = []

        for folder in self.root.rglob("migrations"):

            if not folder.is_dir():
                continue

            if any(part in self.EXCLUDED for part in folder.parts):
                continue

            migration_dirs.append(folder)

        if not migration_dirs:
            return self.error(
                "No se encontraron migraciones.",
                ["No existe ninguna carpeta migrations"],
            )

        info.append(f"Carpetas migrations: {len(migration_dirs)}")

        total_files = 0

        for folder in migration_dirs:

            files = [
                f for f in folder.glob("*.py")
                if f.name != "__init__.py"
            ]

            total_files += len(files)

            info.append(
                f"{folder.parent.name}: {len(files)} migraciones"
            )

            numbers = []

            for file in files:

                prefix = file.stem.split("_")[0]

                if prefix.isdigit():
                    numbers.append(int(prefix))

            numbers.sort()

            if numbers:

                expected = list(
                    range(numbers[0], numbers[-1] + 1)
                )

                missing = sorted(
                    set(expected) - set(numbers)
                )

                if missing:
                    warnings.append(
                        f"{folder.parent.name}: faltan migraciones {missing}"
                    )

        info.append(f"Total migraciones: {total_files}")

        if errors:
            return self.error(
                "Errores encontrados en las migraciones.",
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
            "Migraciones validadas correctamente.",
            info,
        )