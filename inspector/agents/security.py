from inspector.core.base import AgentBase
from inspector.security.manager import SecurityManager


class SecurityAgent(AgentBase):

    name = "security"
    description = "Plataforma de Ciberseguridad"

    def execute(self):

        manager = SecurityManager()

        report = manager.run()

        info = []
        warnings = []
        errors = []

        modules = report.get("modules", [])
        findings = report.get("findings", [])
        risk = report.get("risk", {})

        total_modules = len(modules)
        ok_modules = 0

        for result in modules:

            module = result.get(
                "module",
                "Unknown",
            )

            status = result.get(
                "status",
                "error",
            )

            if status == "ok":

                ok_modules += 1

                info.append(
                    f"{module}: OK"
                )

            elif status == "warning":

                module_findings = result.get(
                    "findings",
                    [],
                )

                warnings.append(
                    f"{module}: "
                    f"{len(module_findings)} "
                    f"vulnerabilidad(es)"
                )

                for item in module_findings:

                    severity = item.get(
                        "severity",
                        "INFO",
                    )

                    title = item.get(
                        "title",
                        "Vulnerabilidad",
                    )

                    file = item.get(
                        "file",
                        "Desconocido",
                    )

                    line = item.get(
                        "line",
                        "?",
                    )

                    warnings.append(
                        f"[{severity}] "
                        f"{title} | "
                        f"{file} | "
                        f"Línea {line}"
                    )

            else:

                errors.append(
                    f"{module}: error inesperado"
                )

        info.append(
            f"Módulos ejecutados: {total_modules}"
        )

        info.append(
            f"Módulos correctos: {ok_modules}"
        )

        info.append(
            f"Vulnerabilidades: {len(findings)}"
        )

        info.append(
            f"Security Score: "
            f"{risk.get('score', 0)}/100"
        )

        if errors:

            return self.error(
                "Se encontraron errores críticos.",
                errors,
                info,
            )

        if warnings:

            return self.warning(
                "Se detectaron vulnerabilidades.",
                warnings,
                info,
            )

        return self.ok(
            "Auditoría de seguridad completada.",
            info,
        )