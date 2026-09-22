from inspector.security.core.module import SecurityModule


class DependenciesModule(SecurityModule):

    name = "Dependencies"
    description = "Auditoría de dependencias"
    risk = "HIGH"

    DANGEROUS = {
        "django<5": "Actualizar Django.",
        "requests<2.32": "Actualizar Requests.",
        "pillow<10": "Actualizar Pillow.",
        "cryptography<43": "Actualizar Cryptography.",
        "urllib3<2": "Actualizar urllib3.",
    }

    def scan(self):

        findings = []

        for file in self.requirement_files():

            content = self.read(file)

            lines = content.splitlines()

            for number, line in enumerate(lines, start=1):

                value = line.strip().lower()

                if not value or value.startswith("#"):
                    continue

                for package, recommendation in self.DANGEROUS.items():

                    name = package.split("<")[0]

                    if value.startswith(name):

                        findings.append(

                            self.vulnerability(

                                title=f"Dependencia: {name}",

                                file=file,

                                line=number,

                                severity="MEDIUM",

                                message=f"Revisar versión instalada: {line.strip()}",

                                recommendation=recommendation,

                                auto_fix=False,

                            )

                        )

        return self.report(findings)