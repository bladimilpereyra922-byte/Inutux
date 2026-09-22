from datetime import datetime


class SecurityReport:

    def __init__(self):

        self.created = datetime.now()

        self.modules = []

        self.findings = []

    def add(self, result):

        self.modules.append(result["module"])

        for finding in result.get("findings", []):

            finding["module"] = result["module"]

            self.findings.append(finding)

    def statistics(self):

        stats = {

            "critical": 0,

            "high": 0,

            "medium": 0,

            "low": 0,

            "info": 0,

        }

        for item in self.findings:

            severity = item["severity"].lower()

            if severity in stats:

                stats[severity] += 1

        return stats

    def score(self):

        score = 100

        for item in self.findings:

            severity = item["severity"].upper()

            if severity == "CRITICAL":

                score -= 15

            elif severity == "HIGH":

                score -= 8

            elif severity == "MEDIUM":

                score -= 4

            elif severity == "LOW":

                score -= 2

        return max(score, 0)

    def summary(self):

        return {

            "modules": len(self.modules),

            "findings": len(self.findings),

            "score": self.score(),

            "statistics": self.statistics(),

            "generated": self.created.isoformat(),

        }