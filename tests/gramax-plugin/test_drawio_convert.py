"""Tests for drawio_convert.py"""
import re
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent.parent / "plugins" / "gramax" / "scripts" / "drawio_convert.py"
FIXTURE_DRAWIO = Path(__file__).parent / "fixtures" / "drawio" / "cyrillic.drawio"


def run(*args, cwd=None):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, cwd=cwd
    )
    return result.stdout, result.stderr, result.returncode


def test_convert_creates_svg(tmp_path):
    output = tmp_path / "out.svg"
    _, err, rc = run(str(FIXTURE_DRAWIO), str(output))
    assert rc == 0, f"stderr: {err}"
    assert output.exists()
    content = output.read_text(encoding="utf-8")
    assert content.startswith("<svg")
    assert 'content="' in content


def test_svg_has_width_height(tmp_path):
    output = tmp_path / "out.svg"
    run(str(FIXTURE_DRAWIO), str(output), "--width", "800", "--height", "600")
    content = output.read_text(encoding="utf-8")
    assert 'width="800px"' in content
    assert 'height="600px"' in content
    assert 'viewBox="-0.5 -0.5 800 600"' in content


def test_content_is_ascii_only(tmp_path):
    """Content-атрибут не должен содержать сырую кириллицу (должен быть сжат)."""
    output = tmp_path / "out.svg"
    run(str(FIXTURE_DRAWIO), str(output))
    content = output.read_text(encoding="utf-8")
    m = re.search(r'content="([^"]+)"', content)
    assert m
    content_attr = m.group(1)
    assert all(ord(c) < 128 for c in content_attr), "content attribute contains non-ASCII chars"


def test_roundtrip_preserves_cyrillic(tmp_path):
    """convert → decompress → исходный mxGraphModel должен содержать кириллицу."""
    output = tmp_path / "out.svg"
    run(str(FIXTURE_DRAWIO), str(output))
    out_str, _, rc = run("--decompress", str(output))
    assert rc == 0
    assert "Привет, Мир" in out_str


def test_extracts_default_size_from_mxfile(tmp_path):
    """Если --width/--height не заданы, брать из pageWidth/pageHeight."""
    output = tmp_path / "out.svg"
    run(str(FIXTURE_DRAWIO), str(output))
    content = output.read_text(encoding="utf-8")
    # fixture has pageWidth="850" pageHeight="600"
    assert 'width="850px"' in content
    assert 'height="600px"' in content


def test_invalid_input_exit_1(tmp_path):
    bad = tmp_path / "bad.drawio"
    bad.write_text("not xml")
    out = tmp_path / "out.svg"
    _, err, rc = run(str(bad), str(out))
    assert rc == 1
    assert err
