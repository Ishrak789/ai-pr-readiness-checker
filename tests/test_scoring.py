from pr_readiness.scoring import (
    Finding,
    build_readiness_report,
    calculate_risk_score,
    classify_status,
)


def test_calculate_risk_score_adds_failed_weights_only() -> None:
    findings = [
        Finding("Lint", True, 20, "Ruff passed."),
        Finding("Tests", False, 35, "Pytest failed."),
        Finding("Security", False, 50, "Bandit found high severity issues."),
    ]

    assert calculate_risk_score(findings) == 85


def test_calculate_risk_score_caps_at_100() -> None:
    findings = [
        Finding("Tests", False, 75, "Pytest failed."),
        Finding("Security", False, 50, "Bandit failed."),
    ]

    assert calculate_risk_score(findings) == 100


def test_classify_status_thresholds() -> None:
    assert classify_status(0) == "Ready"
    assert classify_status(29) == "Ready"
    assert classify_status(30) == "Needs Review"
    assert classify_status(69) == "Needs Review"
    assert classify_status(70) == "Blocked"


def test_build_readiness_report_includes_recommendation() -> None:
    report = build_readiness_report([Finding("Lint", False, 30, "Ruff failed.")])

    assert report.risk_score == 30
    assert report.status == "Needs Review"
    assert "Review" in report.recommendation
