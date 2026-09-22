from inspector.security.core.module import SecurityModule


class PermissionsModule(SecurityModule):

    name = "Permissions"
    description = "Auditoría de permisos"
    risk = "CRITICAL"

    DANGEROUS = [

        (
            "@permission_classes([AllowAny])",
            "AllowAny detectado.",
            "Usar IsAuthenticated cuando sea posible.",
            "HIGH",
        ),

        (
            "permission_classes = [AllowAny]",
            "AllowAny detectado.",
            "Revisar permisos.",
            "HIGH",
        ),

    ]

    def scan(self):

        findings = []

        # Solo revisar archivos que el scanner
        # identifica como vistas del proyecto.
        files = self.views_files()

        for file in files:

            content = self.read(file)

            lines = content.splitlines()

            for number, line in enumerate(
                lines,
                start=1,
            ):

                for (
                    pattern,
                    message,
                    recommendation,
                    severity,
                ) in self.DANGEROUS:

                    if pattern in line:

                        findings.append(
                            self.vulnerability(
                                title="Permisos inseguros",
                                file=file,
                                line=number,
                                severity=severity,
                                message=message,
                                recommendation=recommendation,
                                auto_fix=False,
                            )
                        )

        return self.report(findings)