import re

from inspector.security.core.module import SecurityModule


class CSRFModule(SecurityModule):

    name = "CSRF"
    description = "Auditoría de protección Cross-Site Request Forgery"
    risk = "HIGH"

    def scan(self):

        findings = []

        for file in self.settings_files():

            content = self.read(file)

            checks = [

                (
                    "CsrfViewMiddleware",
                    "Middleware CSRF no encontrado.",
                    "Agregar django.middleware.csrf.CsrfViewMiddleware.",
                    "CRITICAL",
                ),

                (
                    "CSRF_COOKIE_SECURE",
                    "CSRF_COOKIE_SECURE no configurado.",
                    "Configurar CSRF_COOKIE_SECURE = True cuando se utilice HTTPS.",
                    "HIGH",
                ),

                (
                    "CSRF_COOKIE_HTTPONLY",
                    None,
                    None,
                    None,
                ),

            ]

            for setting, message, recommendation, severity in checks:

                if not message:
                    continue

                if setting not in content:

                    findings.append(
                        self.vulnerability(
                            title="CSRF Security",
                            file=file,
                            severity=severity,
                            message=message,
                            recommendation=recommendation,
                            auto_fix=False,
                            owasp="A05:2021",
                            cwe="CWE-352",
                        )
                    )

        for file in self.python_files():

            content = self.read(file)

            if "@csrf_exempt" in content:

                for number, line in enumerate(
                    content.splitlines(),
                    start=1,
                ):

                    if "@csrf_exempt" in line:

                        findings.append(
                            self.vulnerability(
                                title="CSRF Protection Disabled",
                                file=file,
                                line=number,
                                severity="HIGH",
                                message="@csrf_exempt encontrado.",
                                recommendation=(
                                    "Eliminar la excepción CSRF "
                                    "cuando no sea estrictamente necesaria."
                                ),
                                auto_fix=False,
                                owasp="A05:2021",
                                cwe="CWE-352",
                            )
                        )

        return self.report(findings)