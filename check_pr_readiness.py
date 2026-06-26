"""Print a lightweight readiness report for an AI-generated pull request."""

from __future__ import annotations

from pr_readiness import build_readiness_report
from pr_readiness.quality import repository_findings


def main() -> None:
    """Run local repository checks and print a CI-friendly summary."""
    report = build_readiness_report(repository_findings())

    print("AI PR Readiness Report")
    print("======================")
    print(f"Risk score: {report.risk_score}/100")
    print(f"Status: {report.status}")
    print()
    print("Findings:")
    for finding in report.findings:
        marker = "PASS" if finding.passed else "FAIL"
        print(f"- [{marker}] {finding.name} ({finding.weight} risk): {finding.detail}")
    print()
    print(f"Recommendation: {report.recommendation}")


if __name__ == "__main__":
    main()
