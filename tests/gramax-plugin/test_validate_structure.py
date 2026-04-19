"""Tests for validate_structure.py"""
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent.parent / "plugins" / "gramax" / "scripts" / "validate_structure.py"
FIXTURES = Path(__file__).parent / "fixtures"


def run(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True
    )
    return result.stdout, result.stderr, result.returncode


def test_sample_catalog_valid():
    out, err, rc = run(str(FIXTURES / "sample-catalog"))
    assert rc == 0, f"stdout: {out}\nstderr: {err}"


def test_bad_catalog_reports_index_in_root(tmp_path):
    dest = tmp_path / "bad"
    shutil.copytree(FIXTURES / "bad-catalog", dest)
    out, _, rc = run(str(dest))
    assert rc == 1
    assert "_index.md" in out
    assert "root" in out.lower() or "корн" in out.lower()


def test_bad_catalog_reports_unpaired_note(tmp_path):
    dest = tmp_path / "bad"
    shutil.copytree(FIXTURES / "bad-catalog", dest)
    out, _, rc = run(str(dest))
    assert "note" in out.lower() or "парн" in out.lower() or "paired" in out.lower()


def test_bad_catalog_reports_ds_store(tmp_path):
    dest = tmp_path / "bad"
    shutil.copytree(FIXTURES / "bad-catalog", dest)
    (dest / ".DS_Store").touch()  # .DS_Store gitignored — создаём динамически
    out, _, rc = run(str(dest))
    assert ".DS_Store" in out


def test_fix_yes_removes_ds_store(tmp_path):
    dest = tmp_path / "bad"
    shutil.copytree(FIXTURES / "bad-catalog", dest)
    (dest / ".DS_Store").touch()
    assert (dest / ".DS_Store").exists()
    run(str(dest), "--fix", "--yes")
    assert not (dest / ".DS_Store").exists()


def test_fix_without_yes_refuses(tmp_path):
    dest = tmp_path / "bad"
    shutil.copytree(FIXTURES / "bad-catalog", dest)
    (dest / ".DS_Store").touch()
    out, err, rc = run(str(dest), "--fix")
    assert rc == 2
    assert "--yes" in (out + err)
    assert (dest / ".DS_Store").exists()


def test_strict_promotes_warnings(tmp_path):
    """.DS_Store — warning по default, error в --strict."""
    dest = tmp_path / "bad"
    shutil.copytree(FIXTURES / "bad-catalog", dest)
    (dest / ".DS_Store").touch()
    # remove _index.md и незакрытый note чтобы остался только .DS_Store (warning)
    (dest / "_index.md").unlink()
    out1, _, rc1 = run(str(dest))
    out2, _, rc2 = run(str(dest), "--strict")
    # без --strict: только warnings → rc=0; со --strict → rc=1
    assert rc1 == 0
    assert rc2 == 1


def test_missing_frontmatter_reports_error(tmp_path):
    (tmp_path / ".doc-root.yaml").write_text("code: X\ntitle: X\nsyntax: XML\nlanguage: ru\n")
    (tmp_path / "page.md").write_text("Без frontmatter вообще\n")
    out, _, rc = run(str(tmp_path))
    assert rc == 1
    assert "frontmatter" in out.lower()
