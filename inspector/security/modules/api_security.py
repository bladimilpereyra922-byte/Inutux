import re

from inspector.security.core.module import SecurityModule


class APISecurityModule(SecurityModule):

    name = "API Security"
    description = "Auditoría de seguridad de APIs"
    risk = "HIGH"

    def scan(self):

        findings = []

        files = (
            self.python_files()
            + self.url_files()
        )

        patterns = [

            (
                r"@api_view\s*\(\s*\[",
                "Endpoint DRF detectado.",
                "Verificar autenticación y permisos explícitos.",
                "MEDIUM",
            ),

            (
                r"permission_classes\s*=\s*\[\s*AllowAny",
                "API configurada con AllowAny.",
                "Usar permisos restrictivos cuando el endpoint maneje información sensible.",
                "HIGH",
            ),

            (
                r"@csrf_exempt",
                "Endpoint excluido de protección CSRF.",
                "Revisar cuidadosamente la necesidad de excluir CSRF.",
                "HIGH",
            ),

        ]

        for file in files:

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
                ) in patterns:

                    try:

                        matched = re.search(
                            pattern,
                            line,
                            re.IGNORECASE,
                        )

                    except re.error:

                        matched = None

                    if not matched:
                        continue

                    findings.append(
                        self.vulnerability(
                            title="API Security",
                            file=file,
                            line=number,
                            severity=severity,
                            message=message,
                            recommendation=recommendation,
                            auto_fix=False,
                            owasp="A01:2021",
                        )
                    )

        return self.report(findings)