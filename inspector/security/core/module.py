from pathlib import Path


class SecurityModule:

    name = "module"
    description = ""
    risk = "INFO"

    def __init__(self):

        self.root = Path.cwd()

        self.project = {}

        self.intelligence = {}

    def python_files(self):
        return self.project.get("python", [])

    def settings_files(self):
        return self.project.get("settings", [])

    def url_files(self):
        return self.project.get("urls", [])

    def models_files(self):
        return self.project.get("models", [])

    def views_files(self):
        return self.project.get("views", [])

    def forms_files(self):
        return self.project.get("forms", [])

    def admin_files(self):
        return self.project.get("admin", [])

    def serializer_files(self):
        return self.project.get("serializers", [])

    def env_files(self):
        return self.project.get("env", [])

    def docker_files(self):
        return self.project.get("docker", [])

    def requirement_files(self):
        return self.project.get("requirements", [])

    def manage_files(self):
        return self.project.get("manage", [])

    def all_files(self):
        return self.project.get("all_files", [])

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
        cwe=None,
        cve=None,
        owasp=None,
        mitre=None,
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

            "cwe": cwe,

            "cve": cve,

            "owasp": owasp,

            "mitre": mitre,

        }

    def report(self, findings):

        return {

            "module": self.name,

            "description": self.description,

            "risk": self.risk,

            "status": "warning" if findings else "ok",

            "findings": findings,

        }