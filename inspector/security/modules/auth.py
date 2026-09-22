from inspector.security.core.module import SecurityModule


class AuthModule(SecurityModule):

    name = "Auth"
    description = "Auditoría de autenticación"
    risk = "CRITICAL"

    def scan(self):

        findings = []

        for file in self.settings_files():

            content = self.read(file)

            checks = [

                (
                    "AUTH_PASSWORD_VALIDATORS",
                    "No se configuraron validadores de contraseña.",
                    "Configurar AUTH_PASSWORD_VALIDATORS.",
                    "HIGH",
                ),

                (
                    "LOGIN_URL",
                    "LOGIN_URL no configurado.",
                    "Configurar LOGIN_URL.",
                    "LOW",
                ),

                (
                    "LOGIN_REDIRECT_URL",
                    "LOGIN_REDIRECT_URL no configurado.",
                    "Configurar LOGIN_REDIRECT_URL.",
                    "LOW",
                ),

                (
                    "SESSION_EXPIRE_AT_BROWSER_CLOSE",
                    "La sesión no expira al cerrar el navegador.",
                    "Activar SESSION_EXPIRE_AT_BROWSER_CLOSE.",
                    "MEDIUM",
                ),

            ]

            for setting, message, recommendation, severity in checks:

                if setting not in content:

                    findings.append(

                        self.vulnerability(

                            title=setting,

                            file=file,

                            severity=severity,

                            message=message,

                            recommendation=recommendation,

                            auto_fix=False,

                        )

                    )

        return self.report(findings)