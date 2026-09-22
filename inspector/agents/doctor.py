from inspector.core.base import AgentBase


class DoctorAgent(AgentBase):

    name = "doctor"
    description = "Diagnóstico general del proyecto"

    def execute(self):

        info = []
        warnings = []
        errors = []

        if (self.root / "manage.py").exists():
            info.append("manage.py encontrado")
        else:
            errors.append("No existe manage.py")

        if (self.root / "requirements.txt").exists():
            info.append("requirements.txt encontrado")
        else:
            warnings.append("No existe requirements.txt")

        if (self.root / ".git").exists():
            info.append("Repositorio Git encontrado")
        else:
            warnings.append("No es un repositorio Git")

        if (self.root / "venv").exists():
            info.append("Entorno virtual encontrado")
        else:
            warnings.append("No existe entorno virtual")

        apps = []

        for item in self.root.iterdir():
            if item.is_dir() and (item / "apps.py").exists():
                apps.append(item.name)

        info.append(f"Apps Django encontradas: {len(apps)}")

        status = "ok"

        if errors:
            status = "error"
        elif warnings:
            status = "warning"

        return {
            "status": status,
            "message": "Diagnóstico completado",
            "errors": errors,
            "warnings": warnings,
            "info": info,
        }