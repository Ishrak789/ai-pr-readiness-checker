from pathlib import Path

from pr_readiness.quality import (
    count_python_files,
    has_readme_section,
    path_exists,
    repository_findings,
)


def test_path_exists_detects_existing_file(tmp_path: Path) -> None:
    target = tmp_path / "example.py"
    target.write_text("print('hello')\n", encoding="utf-8")

    assert path_exists(target)


def test_count_python_files_counts_nested_python_files(tmp_path: Path) -> None:
    package = tmp_path / "package"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "module.py").write_text("", encoding="utf-8")
    (package / "notes.md").write_text("", encoding="utf-8")

    assert count_python_files(package) == 2


def test_has_readme_section_matches_markdown_heading(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("# Demo\n\n## Architecture\n", encoding="utf-8")

    assert has_readme_section(readme, "architecture")


def test_repository_findings_returns_weighted_findings(tmp_path: Path) -> None:
    findings = repository_findings(tmp_path)

    assert findings
    assert all(finding.weight > 0 for finding in findings)
