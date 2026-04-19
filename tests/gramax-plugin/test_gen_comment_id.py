"""Tests for gen_comment_id.py"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent.parent.parent / "plugins" / "gramax" / "scripts" / "gen_comment_id.py"
ID_RE = re.compile(r"^[a-zA-Z0-9]{5}$")


def run(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def test_generates_5_alphanumeric():
    out, _, rc = run()
    assert rc == 0
    assert ID_RE.match(out), f"ID {out!r} does not match /^[a-zA-Z0-9]{{5}}$/"


def test_generates_different_ids():
    ids = {run()[0] for _ in range(10)}
    assert len(ids) > 1, "Expected different IDs across runs"


def test_check_mode_with_existing_yaml(tmp_path):
    yaml_file = tmp_path / "doc.comments.yaml"
    yaml_file.write_text("abc12:\n  comment: {}\nXyZ99:\n  comment: {}\n")
    out, _, rc = run("--check", str(yaml_file))
    assert rc == 0
    assert ID_RE.match(out)
    assert out not in ("abc12", "XyZ99")


def test_check_mode_with_missing_file_ok(tmp_path):
    yaml_file = tmp_path / "nonexistent.comments.yaml"
    out, _, rc = run("--check", str(yaml_file))
    assert rc == 0
    assert ID_RE.match(out)


def test_check_mode_with_invalid_yaml(tmp_path):
    yaml_file = tmp_path / "bad.comments.yaml"
    yaml_file.write_text("this is: not: valid: yaml: at all\n  - broken")
    out, err, rc = run("--check", str(yaml_file))
    assert rc != 0
    assert "yaml" in (out + err).lower()
