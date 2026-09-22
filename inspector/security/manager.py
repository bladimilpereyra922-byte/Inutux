import importlib
import inspect
import pkgutil

import inspector.security.modules as modules

from inspector.security.scanner import ProjectScanner
from inspector.security.core.risk import RiskEngine
from inspector.security.core.autofix import AutoFixEngine
from inspector.security.core.finder import Finder


class SecurityManager:

    def __init__(self, root=None):

        self.scanner = ProjectScanner(root)

        self.project = self.scanner.scan()

        self.modules = []

        self.risk = RiskEngine()

        self.autofix = AutoFixEngine(
            self.scanner.root
        )

        self.finder = Finder(
            self.project
        )

        self.load()

    def load(self):

        self.modules.clear()

        for _, module_name, _ in pkgutil.iter_modules(
            modules.__path__
        ):

            module = importlib.import_module(
                f"inspector.security.modules.{module_name}"
            )

            for _, cls in inspect.getmembers(
                module,
                inspect.isclass,
            ):

                if (
                    hasattr(cls, "scan")
                    and hasattr(cls, "name")
                    and cls.__module__ == module.__name__
                ):

                    instance = cls()

                    instance.project = self.project
                    instance.finder = self.finder
                    instance.risk = self.risk
                    instance.autofix = self.autofix

                    self.modules.append(
                        instance
                    )

    def run(self):

        findings = []

        module_results = []

        for module in self.modules:

            print(
                f"[SECURITY] {module.name}"
            )

            try:

                result = module.scan()

                if not isinstance(result, dict):

                    result = {
                        "module": module.name,
                        "status": "error",
                        "findings": [
                            {
                                "title": "Invalid module result",
                                "severity": "CRITICAL",
                                "message": (
                                    "El módulo devolvió "
                                    "un resultado inválido."
                                ),
                            }
                        ],
                    }

                result.setdefault(
                    "module",
                    module.name,
                )

                result.setdefault(
                    "status",
                    "ok",
                )

                result.setdefault(
                    "findings",
                    [],
                )

                module_results.append(
                    result
                )

                module_findings = result.get(
                    "findings",
                    [],
                )

                if isinstance(
                    module_findings,
                    list,
                ):

                    for finding in module_findings:

                        if isinstance(
                            finding,
                            dict,
                        ):

                            finding.setdefault(
                                "module",
                                module.name,
                            )

                            findings.append(
                                finding
                            )

            except Exception as e:

                module_results.append(
                    {
                        "module": module.name,
                        "status": "error",
                        "findings": [
                            {
                                "title": "Internal Error",
                                "severity": "CRITICAL",
                                "message": str(e),
                                "module": module.name,
                            }
                        ],
                    }
                )

        return {
            "status": "ok",
            "modules": module_results,
            "findings": findings,
            "risk": self.risk.summary(
                findings
            ),
            "total_findings": len(
                findings
            ),
        }