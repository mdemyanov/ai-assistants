"""Tests for slugify.py"""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent.parent / "plugins" / "gramax" / "scripts" / "slugify.py"


def run_slugify(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def test_cyrillic_to_latin():
    out, _, rc = run_slugify("Быстрый старт")
    assert rc == 0
    assert out == "bystryy-start"


def test_lowercase_applied():
    out, _, rc = run_slugify("Установка И Настройка")
    assert rc == 0
    assert out == "ustanovka-i-nastroyka"


def test_special_chars_collapsed():
    out, _, rc = run_slugify("Что нового?!")
    assert rc == 0
    assert out == "chto-novogo"


def test_cyrillic_composite_letters():
    out, _, rc = run_slugify("ёжик щука")
    assert rc == 0
    assert out == "yozhik-shchuka"


def test_soft_hard_signs_dropped():
    out, _, rc = run_slugify("объект съел")
    assert rc == 0
    assert out == "obekt-sel"


def test_filename_flag_adds_md():
    out, _, rc = run_slugify("--filename", "Быстрый старт")
    assert rc == 0
    assert out == "bystryy-start.md"


def test_folder_flag_no_extension():
    out, _, rc = run_slugify("--folder", "Раздел Документы")
    assert rc == 0
    assert out == "razdel-dokumenty"


def test_multiple_dashes_collapsed():
    out, _, rc = run_slugify("API -- интеграция")
    assert rc == 0
    assert out == "api-integratsiya"


def test_empty_input_error():
    out, err, rc = run_slugify("")
    assert rc != 0
    assert "empty" in err.lower() or "required" in err.lower()
