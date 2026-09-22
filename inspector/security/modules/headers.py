from inspector.security.core.module import SecurityModule


class HeadersModule(SecurityModule):

    name = "Headers"
    description = "HTTP Security Headers"
    risk = "HIGH"

    REQUIRED = {
        "SECURE_HSTS_SECONDS":
            "Configurar HSTS.",

        "SECURE_SSL_REDIRECT":
            "Forzar HTTPS.",

        "SESSION_COOKIE_SECURE":
            "Cookies solo por HTTPS.",

        "CSRF_COOKIE_SECURE":
            "Cookies CSRF por HTTPS.",

        "SECURE_BROWSER_XSS_FILTER":
            "Activar protección XSS.",

        "SECURE_CONTENT_TYPE_NOSNIFF":
            "Evitar MIME Sniffing.",

        "X_FRAME_OPTIONS":
            "Evitar Clickjacking.",
    }

    def scan(self):

        findings = []

        for file in self.settings_files():

            content = self.read(file)

            for setting, recommendation in self.REQUIRED.items():

                if setting not in content:

                    findings.append(

                        self.vulnerability(

                            title=setting,

                            file=file,

                            severity="HIGH",

                            message=f"{setting} no configurado.",

                            recommendation=recommendation,

                            auto_fix=True,

                        )

                    )

        return self.report(findings)