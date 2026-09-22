from inspector.core.base import AgentBase
from inspector.security.scanner import ProjectScanner


class ScannerAgent(AgentBase):

    name = "scanner"
    description = "Escáner general del proyecto"

    def execute(self):

        scanner = ProjectScanner()

        project = scanner.scan()

        info = [
            f"Archivos Python: {len(project['python'])}",
            f"settings.py: {len(project['settings'])}",
            f"urls.py: {len(project['urls'])}",
            f".env: {len(project['env'])}",
            f"requirements.txt: {len(project['requirements'])}",
            f"Docker: {len(project['docker'])}",
            f"manage.py: {len(project['manage'])}",
        ]

        return self.ok(
            "Escaneo completado correctamente.",
            info,
        )