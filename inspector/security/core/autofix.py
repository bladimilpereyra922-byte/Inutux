from pathlib import Path
import shutil


class AutoFixEngine:

    def __init__(self, root=None):

        self.root = Path(root) if root else Path.cwd()

        self.backup_dir = (
            self.root
            / "inspector"
            / "security"
            / "history"
            / "backups"
        )

    def backup(self, file):

        file = Path(file)

        if not file.exists():
            return None

        self.backup_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        backup = (
            self.backup_dir
            / f"{file.name}.backup"
        )

        shutil.copy2(
            file,
            backup,
        )

        return backup

    def can_fix(self, finding):

        return finding.get(
            "auto_fix",
            False,
        )

    def fix(self, finding):

        if not self.can_fix(finding):

            return {
                "status": "skipped",
                "message": "Corrección automática no autorizada.",
            }

        return {
            "status": "manual",
            "message": "La corrección requiere implementación segura.",
        }

    def rollback(self, file):

        file = Path(file)

        backup = (
            self.backup_dir
            / f"{file.name}.backup"
        )

        if not backup.exists():

            return {
                "status": "error",
                "message": "No existe respaldo.",
            }

        shutil.copy2(
            backup,
            file,
        )

        return {
            "status": "ok",
            "message": "Archivo restaurado correctamente.",
        }