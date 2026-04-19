"""Tests for parse_comments.py"""
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent.parent / "plugins" / "gramax" / "scripts" / "parse_comments.py"
FIXTURE = Path(__file__).parent / "fixtures" / "comments" / "doc.md"


def run(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True
    )
    return result.stdout, result.stderr, result.returncode


def test_json_format_has_all_comments():
    out, _, rc = run(str(FIXTURE), "--format", "json")
    assert rc == 0
    data = json.loads(out)
    ids = {c["id"] for c in data}
    assert ids == {"abc12", "XyZ99", "Blk01"}


def test_json_includes_anchor_text():
    out, _, rc = run(str(FIXTURE), "--format", "json")
    data = json.loads(out)
    by_id = {c["id"]: c for c in data}
    assert "привязанным фрагментом" in by_id["abc12"]["anchor"]
    assert "другим фрагментом" in by_id["XyZ99"]["anchor"]


def test_answers_deduplicated():
    """abc12 has duplicate answers in fixture — output should have only 1."""
    out, _, rc = run(str(FIXTURE), "--format", "json")
    data = json.loads(out)
    by_id = {c["id"]: c for c in data}
    assert len(by_id["abc12"]["answers"]) == 1


def test_author_filter():
    out, _, rc = run(str(FIXTURE), "--format", "json", "--author", "Charlie")
    data = json.loads(out)
    assert len(data) == 1
    assert data[0]["id"] == "XyZ99"


def test_unanswered_filter():
    out, _, rc = run(str(FIXTURE), "--format", "json", "--unanswered")
    data = json.loads(out)
    ids = {c["id"] for c in data}
    assert ids == {"XyZ99", "Blk01"}


def test_answered_filter():
    out, _, rc = run(str(FIXTURE), "--format", "json", "--answered")
    data = json.loads(out)
    ids = {c["id"] for c in data}
    assert ids == {"abc12"}


def test_summary_output():
    out, _, rc = run(str(FIXTURE), "--summary")
    assert rc == 0
    assert "3" in out  # total comments
    assert "Alice" in out or "alice" in out.lower()


def test_report_format_readable():
    out, _, rc = run(str(FIXTURE), "--format", "report")
    assert rc == 0
    assert "abc12" in out
    assert "Alice" in out
    assert "привязанным" in out


def test_missing_yaml_status(tmp_path):
    md = tmp_path / "page.md"
    md.write_text("---\norder: 1\ntitle: T\n---\n\n<comment id=\"abc12\">x</comment>\n")
    out, _, rc = run(str(md), "--format", "json")
    data = json.loads(out)
    assert len(data) == 1
    assert data[0]["status"] == "yaml_missing"
