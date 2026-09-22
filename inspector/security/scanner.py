from pathlib import Path


class ProjectScanner:
    """
    Escáner central del proyecto.

    Recorre el proyecto una sola vez y entrega
    toda la información a los módulos de seguridad.
    """

    EXCLUDED = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "site-packages",
        ".pytest_cache",
        "dist",
        "build",
        ".idea",
        ".vscode",
        "logs",
        "reports",
        "inspector",
    }

    def __init__(self, root=None):

        self.root = Path(root) if root else Path.cwd()

        self.data = {
            "python": [],
            "settings": [],
            "urls": [],
            "requirements": [],
            "env": [],
            "docker": [],
            "manage": [],
            "all_files": [],
        }

    def scan(self):

        for file in self.root.rglob("*"):

            if any(
                part in self.EXCLUDED
                for part in file.parts
            ):
                continue

            if not file.is_file():
                continue

            self.data["all_files"].append(file)

            name = file.name.lower()

            if file.suffix == ".py":
                self.data["python"].append(file)

            if name == "settings.py":
                self.data["settings"].append(file)

            elif name == "urls.py":
                self.data["urls"].append(file)

            elif name == "requirements.txt":
                self.data["requirements"].append(file)

            elif name == ".env":
                self.data["env"].append(file)

            elif name == "manage.py":
                self.data["manage"].append(file)

            elif name in (
                "dockerfile",
                "docker-compose.yml",
                "docker-compose.yaml",
            ):
                self.data["docker"].append(file)

        return self.data

    def python_files(self):
        return self.data["python"]

    def settings_files(self):
        return self.data["settings"]

    def url_files(self):
        return self.data["urls"]

    def env_files(self):
        return self.data["env"]

    def docker_files(self):
        return self.data["docker"]

    def requirement_files(self):
        return self.data["requirements"]

    def manage_files(self):
        return self.data["manage"]

    def all_files(self):
        return self.data["all_files"]