"""Tests for validate_comments.py"""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent.parent / "plugins" / "gramax" / "scripts" / "validate_comments.py"
FIXTURES = Path(__file__).parent / "fixtures"


def run(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True
    )
    return result.stdout, result.stderr, result.returncode


def test_valid_doc_passes():
    out, err, rc = run(str(FIXTURES / "comments" / "doc.md"))
    assert rc == 0, f"stdout: {out}\nstderr: {err}"


def test_missing_yaml_key_detected(tmp_path):
    md = tmp_path / "page.md"
    md.write_text(
        "---\norder: 1\ntitle: T\n---\n\n"
        "Text with <comment id=\"abc12\">fragment</comment>.\n"
    )
    (tmp_path / "page.comments.yaml").write_text("XyZ99:\n  comment:\n    dateTime: '2026-01-01T00:00:00.000Z'\n    user:\n      mail: a@b.c\n      name: A\n    content: x\n  answers: []\n")
    out, _, rc = run(str(md))
    assert rc == 1
    assert "abc12" in out
    assert "yaml" in out.lower() or "missing" in out.lower()


def test_orphaned_yaml_key_detected(tmp_path):
    md = tmp_path / "page.md"
    md.write_text("---\norder: 1\ntitle: T\n---\n\nNo comment tags here.\n")
    (tmp_path / "page.comments.yaml").write_text(
        "abc12:\n  comment:\n    dateTime: '2026-01-01T00:00:00.000Z'\n    user:\n      mail: a@b.c\n      name: A\n    content: x\n  answers: []\n"
    )
    out, _, rc = run(str(md))
    assert rc == 1
    assert "abc12" in out


def test_invalid_id_format(tmp_path):
    md = tmp_path / "page.md"
    md.write_text("---\norder: 1\ntitle: T\n---\n\n<comment id=\"XX\">x</comment>\n")
    out, _, rc = run(str(md))
    assert rc == 1
    assert "format" in out.lower() or "invalid" in out.lower() or "id" in out.lower()


def test_missing_required_fields(tmp_path):
    md = tmp_path / "page.md"
    md.write_text("---\norder: 1\ntitle: T\n---\n\n<comment id=\"abc12\">x</comment>\n")
    (tmp_path / "page.comments.yaml").write_text("abc12:\n  comment:\n    content: x\n  answers: []\n")
    out, _, rc = run(str(md))
    assert rc == 1
    assert "datetime" in out.lower() or "user" in out.lower()


def test_duplicate_ids_in_md(tmp_path):
    md = tmp_path / "page.md"
    md.write_text(
        "---\norder: 1\ntitle: T\n---\n\n"
        "<comment id=\"abc12\">one</comment> and <comment id=\"abc12\">two</comment>\n"
    )
    (tmp_path / "page.comments.yaml").write_text(
        "abc12:\n  comment:\n    dateTime: '2026-01-01T00:00:00.000Z'\n    user:\n      mail: a@b.c\n      name: A\n    content: x\n  answers: []\n"
    )
    out, _, rc = run(str(md))
    assert rc == 1
    assert "unique" in out.lower() or "duplicate" in out.lower() or "abc12" in out


def test_strict_flags_duplicate_answers(tmp_path):
    """Comments fixture содержит дубликат ответов — warning по default, error в --strict."""
    # Копируем фикстуру
    md = tmp_path / "doc.md"
    yaml_file = tmp_path / "doc.comments.yaml"
    md.write_text((FIXTURES / "comments" / "doc.md").read_text(encoding="utf-8"))
    yaml_file.write_text((FIXTURES / "comments" / "doc.comments.yaml").read_text(encoding="utf-8"))

    _, _, rc_default = run(str(md))
    _, _, rc_strict = run(str(md), "--strict")
    assert rc_default == 0
    assert rc_strict == 1
