import re

from inspector.security.core.module import SecurityModule


class SQLInjectionModule(SecurityModule):

    name = "SQL Injection"
    description = "Detección de posibles inyecciones SQL"
    risk = "CRITICAL"

    PATTERNS = [

        (
            r"\.raw\s*\(",
            "Uso de SQL raw detectado.",
            "Usar consultas parametrizadas y evitar concatenar entrada del usuario.",
            "HIGH",
        ),

        (
            r"\.extra\s*\(",
            "Uso de QuerySet.extra() detectado.",
            "Revisar y reemplazar por APIs ORM seguras.",
            "HIGH",
        ),

        (
            r"execute\s*\(\s*[\"'].*(%s|%s).*",
            "Consulta SQL potencialmente insegura.",
            "Utilizar parámetros separados en lugar de concatenar valores.",
            "CRITICAL",
        ),

        (
            r"execute\s*\(\s*f[\"']",
            "SQL construido mediante f-string.",
            "Usar consultas parametrizadas.",
            "CRITICAL",
        ),

        (
            r"execute\s*\(\s*[\"'].*\+",
            "SQL construido mediante concatenación.",
            "Utilizar consultas parametrizadas.",
            "CRITICAL",
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

                for pattern, message, recommendation, severity in self.PATTERNS:

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
                            title="SQL Injection",
                            file=file,
                            line=number,
                            severity=severity,
                            message=message,
                            recommendation=recommendation,
                            auto_fix=False,
                            owasp="A03:2021",
                            cwe="CWE-89",
                        )
                    )

        return self.report(findings)