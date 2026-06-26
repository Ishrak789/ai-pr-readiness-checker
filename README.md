# AI PR Readiness Checker

A lightweight CI/CD validation tool that checks whether an AI-generated code
change looks safe to merge. The project is intentionally small: it combines
linting, tests, security scanning, and a readable readiness score that can run
locally or inside CircleCI.

## Why This Matters for AI-Generated Code

AI coding tools can produce useful changes quickly, but they can also introduce
subtle regressions, missing tests, insecure patterns, or code that only appears
complete. A CI/CD readiness gate gives reviewers a fast signal before merging:

- Did the generated code pass basic quality checks?
- Are tests present and passing?
- Did a security scan find obvious risks?
- Is the change documented well enough for a human reviewer?

This project shows how an engineering team could add a simple validation layer
around AI-assisted development without building a heavy platform.

## Architecture

- `pr_readiness/scoring.py` contains the risk score and status classification
  logic.
- `pr_readiness/quality.py` contains small repository hygiene checks.
- `check_pr_readiness.py` prints the CI-friendly readiness report.
- `tests/` contains pytest unit tests for the helper functions.
- `.circleci/config.yml` runs install, lint, tests, security scanning, and the
  readiness report.

## Setup

Create a virtual environment and install the development dependencies:

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
```

Run the local validation commands:

```bash
ruff check .
pytest
bandit -r pr_readiness check_pr_readiness.py
python check_pr_readiness.py
```

## Sample Output

```text
AI PR Readiness Report
======================
Risk score: 0/100
Status: Ready

Findings:
- [PASS] Source package present (25 risk): Expected a small Python package with readiness helpers.
- [PASS] Unit tests present (25 risk): Expected pytest tests for scoring and quality helpers.
- [PASS] CircleCI pipeline configured (20 risk): Expected CI jobs for linting, tests, security scan, and readiness check.
- [PASS] README explains AI-code validation (15 risk): Expected documentation that connects the project to AI-written changes.
- [PASS] Tooling configured (15 risk): Expected ruff, pytest, and bandit setup files.

Recommendation: Merge is reasonable after normal reviewer approval.
```

## Resume Bullet Points

- Built a Python CI/CD readiness checker for AI-generated pull requests with
  risk scoring, merge status classification, and reviewer recommendations.
- Integrated CircleCI workflow steps for dependency installation, Ruff linting,
  pytest unit tests, Bandit security scanning, and a custom readiness report.
- Created a small, testable Python package that models quality signals as
  weighted findings and converts them into actionable CI output.
