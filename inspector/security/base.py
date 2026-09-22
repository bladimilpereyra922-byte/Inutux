from pathlib import Path


class SecurityModule:

    name = "base"
    description = "Base Security Module"
    risk = "INFO"

    def __init__(self):

        self.root = Path.cwd()

        self.project = {}

    def python_files(self):

        return self.project.get("python", [])

    def settings_files(self):

        return self.project.get("settings", [])

    def url_files(self):

        return self.project.get("urls", [])

    def env_files(self):

        return self.project.get("env", [])

    def docker_files(self):

        return self.project.get("docker", [])

    def requirement_files(self):

        return self.project.get("requirements", [])

    def manage_files(self):

        return self.project.get("manage", [])

    def read(self, file):

        try:

            return file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        except Exception:

            return ""

    def vulnerability(

        self,

        title,

        file,

        message,

        recommendation,

        severity="MEDIUM",

        line=None,

        auto_fix=False,

        fix=None,

    ):

        return {

            "title": title,

            "file": str(file),

            "line": line,

            "severity": severity,

            "message": message,

            "recommendation": recommendation,

            "auto_fix": auto_fix,

            "fix": fix,

        }

    def report(self, findings):

        return {

            "module": self.name,

            "description": self.description,

            "risk": self.risk,

            "status": "warning" if findings else "ok",

            "findings": findings,

        }