"""Simple quality-signal helpers used by the readiness checker."""

from __future__ import annotations

from pathlib import Path

from pr_readiness.scoring import Finding


def path_exists(path: str | Path) -> bool:
    """Return whether a required project file or directory exists."""
    return Path(path).exists()


def count_python_files(root: str | Path) -> int:
    """Count Python source files under a directory."""
    root_path = Path(root)
    if not root_path.exists():
        return 0
    return sum(1 for path in root_path.rglob("*.py") if path.is_file())


def has_readme_section(readme_path: str | Path, heading: str) -> bool:
    """Return whether README.md contains a specific Markdown heading."""
    path = Path(readme_path)
    if not path.exists():
        return False
    normalized_heading = heading.strip().casefold()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().lstrip("#").strip().casefold() == normalized_heading:
            return True
    return False


def repository_findings(project_root: str | Path = ".") -> list[Finding]:
    """Collect lightweight repository hygiene findings."""
    root = Path(project_root)
    package_dir = root / "pr_readiness"
    tests_dir = root / "tests"
    return [
        Finding(
            name="Source package present",
            passed=path_exists(package_dir) and count_python_files(package_dir) >= 2,
            weight=25,
            detail="Expected a small Python package with readiness helpers.",
        ),
        Finding(
            name="Unit tests present",
            passed=path_exists(tests_dir) and count_python_files(tests_dir) >= 1,
            weight=25,
            detail="Expected pytest tests for scoring and quality helpers.",
        ),
        Finding(
            name="CircleCI pipeline configured",
            passed=path_exists(root / ".circleci" / "config.yml"),
            weight=20,
            detail=(
                "Expected CI jobs for linting, tests, security scan, "
                "and readiness check."
            ),
        ),
        Finding(
            name="README explains AI-code validation",
            passed=has_readme_section(
                root / "README.md",
                "Why This Matters for AI-Generated Code",
            ),
            weight=15,
            detail=(
                "Expected documentation that connects the project "
                "to AI-written changes."
            ),
        ),
        Finding(
            name="Tooling configured",
            passed=path_exists(root / "pyproject.toml")
            and path_exists(root / "requirements-dev.txt"),
            weight=15,
            detail="Expected ruff, pytest, and bandit setup files.",
        ),
    ]
