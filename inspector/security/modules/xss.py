import re

from inspector.security.core.module import SecurityModule


class XSSModule(SecurityModule):

    name = "XSS"
    description = "Detección de posibles vulnerabilidades Cross-Site Scripting"
    risk = "HIGH"

    PATTERNS = [

        (
            r"\|safe\b",
            "Uso de |safe detectado.",
            "Verificar que el contenido haya sido sanitizado antes de marcarlo como seguro.",
            "HIGH",
        ),

        (
            r"\|escapejs\b",
            None,
            None,
            None,
        ),

        (
            r"mark_safe\s*\(",
            "Uso de mark_safe() detectado.",
            "No marcar contenido controlado por usuarios como HTML seguro.",
            "HIGH",
        ),

        (
            r"HttpResponse\s*\(.*request\.",
            "Posible contenido controlado por el usuario enviado directamente en la respuesta.",
            "Validar y escapar correctamente la entrada del usuario.",
            "HIGH",
        ),

        (
            r"innerHTML\s*=",
            "Asignación directa a innerHTML detectada.",
            "Utilizar textContent o sanitizar correctamente el contenido.",
            "HIGH",
        ),

        (
            r"document\.write\s*\(",
            "Uso de document.write() detectado.",
            "Evitar document.write() con datos controlados por usuarios.",
            "HIGH",
        ),

    ]

    def scan(self):

        findings = []

        files = (
            self.python_files()
            + self.finder.html()
            + self.finder.javascript()
        )

        seen = set()

        for file in files:

            if file in seen:
                continue

            seen.add(file)

            content = self.read(file)

            for number, line in enumerate(
                content.splitlines(),
                start=1,
            ):

                for pattern, message, recommendation, severity in self.PATTERNS:

                    if not message:
                        continue

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
                            title="Cross-Site Scripting (XSS)",
                            file=file,
                            line=number,
                            severity=severity,
                            message=message,
                            recommendation=recommendation,
                            auto_fix=False,
                            owasp="A03:2021",
                            cwe="CWE-79",
                        )
                    )

        return self.report(findings)