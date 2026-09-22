import json
import re

from inspector.security.base import SecurityModule


class SecretsModule(SecurityModule):

    name = "Secrets"
    description = "Detección de secretos, credenciales y tokens"
    risk = "CRITICAL"

    def __init__(self):

        super().__init__()

        self.rules = []

        self.load_rules()

    def load_rules(self):

        file = (
            self.root /
            "inspector" /
            "security" /
            "intelligence" /
            "leaked_tokens.json"
        )

        if file.exists():

            self.rules = json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

    def scan(self):

        findings = []

        for py in self.python_files():

            content = self.read(py)

            if not content:
                continue

            lines = content.splitlines()

            for line_number, line in enumerate(
                lines,
                start=1,
            ):

                for rule in self.rules:

                    try:

                        if re.search(
                            rule["pattern"],
                            line,
                        ):

                            findings.append(

                                self.vulnerability(

                                    title=rule["name"],

                                    file=py,

                                    line=line_number,

                                    severity=rule["severity"],

                                    message=rule["message"],

                                    recommendation=rule["recommendation"],

                                    auto_fix=False,

                                    fix=None,

                                )

                            )

                    except re.error:

                        continue

        return self.report(findings)