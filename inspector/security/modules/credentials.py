import re

from inspector.security.core.module import SecurityModule


class CredentialsModule(SecurityModule):

    name = "Credentials"
    description = "Auditoría de contraseñas, credenciales y secretos"
    risk = "CRITICAL"

    PATTERNS = [
        (
            r"password\s*=\s*[\"'][^\"']+[\"']",
            "Contraseña escrita directamente en el código.",
            "No almacenar contraseñas en texto plano.",
            "CRITICAL",
            "CWE-256",
        ),
        (
            r"passwd\s*=\s*[\"'][^\"']+[\"']",
            "Credencial escrita directamente en el código.",
            "Utilizar el sistema seguro de autenticación.",
            "CRITICAL",
            "CWE-256",
        ),
        (
            r"SECRET_KEY\s*=\s*[\"'][^\"']+[\"']",
            "SECRET_KEY escrita directamente en el código.",
            "Mover SECRET_KEY a una variable de entorno o gestor de secretos.",
            "CRITICAL",
            "CWE-798",
        ),
        (
            r"api[_-]?key\s*=\s*[\"'][^\"']+[\"']",
            "API key escrita directamente en el código.",
            "Mover la API key a un gestor de secretos.",
            "CRITICAL",
            "CWE-798",
        ),
    ]

    def scan(self):

        findings = []

        for file in self.python_files():

            content = self.read(file)

            for number, line in enumerate(
                content.splitlines(),
                start=1,
            ):

                for (
                    pattern,
                    message,
                    recommendation,
                    severity,
                    cwe,
                ) in self.PATTERNS:

                    if not re.search(
                        pattern,
                        line,
                        re.IGNORECASE,
                    ):
                        continue

                    findings.append(
                        self.vulnerability(
                            title="Credencial expuesta",
                            file=file,
                            line=number,
                            severity=severity,
                            message=message,
                            recommendation=recommendation,
                            auto_fix=False,
                            cwe=cwe,
                        )
                    )

        return self.report(findings)