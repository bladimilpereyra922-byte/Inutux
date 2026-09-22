class RiskEngine:

    WEIGHTS = {
        "CRITICAL": 10,
        "HIGH": 5,
        "MEDIUM": 2,
        "LOW": 1,
        "INFO": 0,
    }

    def normalize_severity(self, value):

        if not isinstance(value, str):
            return "INFO"

        value = value.strip().upper()

        if value not in self.WEIGHTS:
            return "INFO"

        return value

    def score(self, findings):

        if not findings:
            return 100

        total_risk = 0

        for finding in findings:

            severity = self.normalize_severity(
                finding.get("severity")
            )

            total_risk += self.WEIGHTS[severity]

        # El score representa la seguridad relativa
        # del proyecto y queda siempre entre 0 y 100.
        #
        # 100 = sin hallazgos
        # 0   = riesgo extremadamente alto

        score = 100 - min(
            total_risk,
            100,
        )

        return max(
            0,
            min(score, 100),
        )

    def statistics(self, findings):

        stats = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "INFO": 0,
        }

        for finding in findings:

            severity = self.normalize_severity(
                finding.get("severity")
            )

            stats[severity] += 1

        return stats

    def by_module(self, findings):

        modules = {}

        for finding in findings:

            module = finding.get(
                "module",
                "Unknown",
            )

            modules.setdefault(
                module,
                [],
            )

            modules[module].append(
                finding
            )

        return modules

    def by_file(self, findings):

        files = {}

        for finding in findings:

            file = finding.get(
                "file",
                "",
            )

            files.setdefault(
                file,
                [],
            )

            files[file].append(
                finding
            )

        return files

    def summary(self, findings):

        return {
            "score": self.score(findings),
            "statistics": self.statistics(findings),
            "modules": self.by_module(findings),
            "files": self.by_file(findings),
            "total": len(findings),
        }