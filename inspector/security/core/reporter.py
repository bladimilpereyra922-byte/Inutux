from datetime import datetime, timezone


class ReportBuilder:
    def __init__(self):

        self.findings = []

    def add(
        self,
        module,
        title,
        severity,
        file,
        line,
        message,
        recommendation,
        auto_fix=False,
        fix=None,
        cwe=None,
        cve=None,
        owasp=None,
        mitre=None,
    ):

        self.findings.append(
            {
                "module": module,
                "title": title,
                "severity": severity,
                "file": str(file),
                "line": line,
                "message": message,
                "recommendation": recommendation,
                "auto_fix": auto_fix,
                "fix": fix,
                "cwe": cwe,
                "cve": cve,
                "owasp": owasp,
                "mitre": mitre,
                "time": datetime.now(tz=timezone.utc).isoformat(),
            }
        )

    def build(self):

        return self.findings
