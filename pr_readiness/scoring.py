"""Small scoring helpers for PR readiness checks."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    """A CI signal that affects merge readiness."""

    name: str
    passed: bool
    weight: int
    detail: str


@dataclass(frozen=True)
class ReadinessReport:
    """Final readiness result shown in CI output."""

    risk_score: int
    status: str
    findings: tuple[Finding, ...]
    recommendation: str


def calculate_risk_score(findings: Iterable[Finding]) -> int:
    """Return a 0-100 risk score from failed weighted findings."""
    failed_weight = sum(finding.weight for finding in findings if not finding.passed)
    return min(100, max(0, failed_weight))


def classify_status(risk_score: int) -> str:
    """Classify a score into a merge-readiness status."""
    if risk_score >= 70:
        return "Blocked"
    if risk_score >= 30:
        return "Needs Review"
    return "Ready"


def recommendation_for(status: str) -> str:
    """Return a concise recommendation for the readiness status."""
    recommendations = {
        "Ready": "Merge is reasonable after normal reviewer approval.",
        "Needs Review": (
            "Review the failed signals before merging this AI-generated change."
        ),
        "Blocked": (
            "Do not merge until blocking CI, test, or security issues are fixed."
        ),
    }
    return recommendations[status]


def build_readiness_report(findings: Iterable[Finding]) -> ReadinessReport:
    """Build the final report from raw quality findings."""
    finding_tuple = tuple(findings)
    risk_score = calculate_risk_score(finding_tuple)
    status = classify_status(risk_score)
    return ReadinessReport(
        risk_score=risk_score,
        status=status,
        findings=finding_tuple,
        recommendation=recommendation_for(status),
    )
