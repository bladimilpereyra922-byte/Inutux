from pathlib import Path

from inspector.core.base import AgentBase


class ModelsAgent(AgentBase):

    name = "models"
    description = "Auditoría de Modelos Django"

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

        model_files = []

        for file in self.root.rglob("models.py"):

            if any(part in self.EXCLUDED for part in file.parts):
                continue

            model_files.append(file)

        if not model_files:
            return self.error(
                "No se encontraron modelos.",
                ["No existe ningún models.py"],
            )

        info.append(f"Archivos models.py: {len(model_files)}")

        total_models = 0
        foreign_keys = 0
        one_to_one = 0
        many_to_many = 0

        for model in model_files:

            try:

                content = model.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                classes = content.count("class ")

                total_models += classes

                foreign_keys += content.count("ForeignKey(")
                one_to_one += content.count("OneToOneField(")
                many_to_many += content.count("ManyToManyField(")

                info.append(
                    f"{model.parent.name}: {classes} modelos"
                )

                if (
                    classes > 0
                    and "from django.db import models" not in content
                ):
                    warnings.append(
                        f"{model.parent.name}: falta importar django.db.models"
                    )

            except Exception as e:
                warnings.append(str(e))

        info.append(f"Total modelos: {total_models}")
        info.append(f"ForeignKey: {foreign_keys}")
        info.append(f"OneToOne: {one_to_one}")
        info.append(f"ManyToMany: {many_to_many}")

        if errors:
            return self.error(
                "Errores encontrados en los modelos.",
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
            "Modelos validados correctamente.",
            info,
        )