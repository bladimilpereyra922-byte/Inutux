from inspector.security.core.module import SecurityModule


class JWTModule(SecurityModule):

    name = "JWT"
    description = "Auditoría de JSON Web Tokens"
    risk = "CRITICAL"

    def scan(self):

        findings = []

        files = list(
            dict.fromkeys(
                self.python_files()
                + self.settings_files()
            )
        )

        checks = [

            (
                "verify=False",
                "La verificación del JWT está deshabilitada.",
                "Nunca deshabilitar la verificación de firmas JWT.",
                "CRITICAL",
            ),

            (
                "algorithms=['none']",
                "JWT acepta el algoritmo NONE.",
                "Permitir únicamente algoritmos seguros (HS256, RS256, ES256...).",
                "CRITICAL",
            ),

            (
                "algorithms=[\"none\"]",
                "JWT acepta el algoritmo NONE.",
                "Permitir únicamente algoritmos seguros (HS256, RS256, ES256...).",
                "CRITICAL",
            ),

        ]

        for file in files:

            content = self.read(file)

            for number, line in enumerate(
                content.splitlines(),
                start=1,
            ):

                for pattern, message, recommendation, severity in checks:

                    if pattern.lower() in line.lower():

                        findings.append(
                            self.vulnerability(
                                title="JWT Security",
                                file=file,
                                line=number,
                                severity=severity,
                                message=message,
                                recommendation=recommendation,
                                auto_fix=False,
                            )
                        )

        return self.report(findings)