from inspector.security.core.module import SecurityModule


class OAuthModule(SecurityModule):

    name = "OAuth"
    description = "Auditoría de OAuth"
    risk = "HIGH"

    def scan(self):

        findings = []

        files = list(
            dict.fromkeys(
                self.settings_files()
                + self.url_files()
            )
        )

        checks = [
            (
                "verify=False",
                "La verificación TLS está deshabilitada.",
                "No deshabilitar la verificación TLS en OAuth.",
                "CRITICAL",
            ),
        ]

        seen = set()

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
                ) in checks:

                    if pattern.lower() not in line.lower():
                        continue

                    key = (
                        str(file),
                        number,
                        pattern,
                    )

                    if key in seen:
                        continue

                    seen.add(key)

                    findings.append(
                        self.vulnerability(
                            title="OAuth Security",
                            file=file,
                            line=number,
                            severity=severity,
                            message=message,
                            recommendation=recommendation,
                            auto_fix=False,
                            owasp="A07:2021",
                        )
                    )

        return self.report(findings)