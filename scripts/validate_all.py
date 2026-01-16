#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0"]
# ///
"""
Validate All Skills — проверка всех skills в директории.

Использование:
    python validate_all.py <skills_directory>

Примеры:
    python validate_all.py .
    python validate_all.py /path/to/skills
"""

import re
import sys
from pathlib import Path
from typing import NamedTuple

try:
    import yaml
except ImportError:
    print("❌ Требуется PyYAML: pip install pyyaml")
    sys.exit(1)


class ValidationResult(NamedTuple):
    """Результат валидации skill."""
    skill_name: str
    is_valid: bool
    errors: list[str]
    warnings: list[str]


def validate_name(name: str) -> list[str]:
    """Валидация поля name."""
    errors = []

    if not name:
        errors.append("name is required")
        return errors

    if len(name) > 64:
        errors.append(f"name too long ({len(name)} > 64 chars)")

    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        errors.append("name must be hyphen-case (lowercase, digits, hyphens)")

    if name.startswith('-') or name.endswith('-'):
        errors.append("name cannot start or end with hyphen")

    if '--' in name:
        errors.append("name cannot contain double hyphens")

    return errors


def validate_description(description: str) -> list[str]:
    """Валидация поля description."""
    errors = []

    if not description:
        errors.append("description is required")
        return errors

    if len(description) > 1024:
        errors.append(f"description too long ({len(description)} > 1024 chars)")

    if '<' in description or '>' in description:
        errors.append("description cannot contain angle brackets < >")

    return errors


def validate_skill(skill_path: Path) -> ValidationResult:
    """Валидация одного skill."""
    skill_name = skill_path.name
    errors = []
    warnings = []

    # Проверка наличия SKILL.md
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return ValidationResult(
            skill_name=skill_name,
            is_valid=False,
            errors=["SKILL.md not found"],
            warnings=[]
        )

    # Чтение и парсинг SKILL.md
    content = skill_md.read_text(encoding='utf-8')

    # Извлечение frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return ValidationResult(
            skill_name=skill_name,
            is_valid=False,
            errors=["Invalid YAML frontmatter"],
            warnings=[]
        )

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return ValidationResult(
            skill_name=skill_name,
            is_valid=False,
            errors=[f"YAML parse error: {e}"],
            warnings=[]
        )

    if not isinstance(frontmatter, dict):
        return ValidationResult(
            skill_name=skill_name,
            is_valid=False,
            errors=["Frontmatter must be a dictionary"],
            warnings=[]
        )

    # Валидация name
    name = frontmatter.get('name', '')
    errors.extend(validate_name(name))

    # Валидация description
    description = frontmatter.get('description', '')
    errors.extend(validate_description(description))

    # Проверка body
    body = content[match.end():].strip()
    lines = body.split('\n')

    if len(lines) > 500:
        warnings.append(f"SKILL.md body is long ({len(lines)} lines > 500)")

    # Проверка наличия README.md (антипаттерн)
    if (skill_path / 'README.md').exists():
        warnings.append("README.md found (antipattern - use SKILL.md)")

    # Проверка наличия CHANGELOG.md (антипаттерн)
    if (skill_path / 'CHANGELOG.md').exists():
        warnings.append("CHANGELOG.md found (antipattern)")

    return ValidationResult(
        skill_name=skill_name,
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


def find_skills(directory: Path) -> list[Path]:
    """Находит все skill директории."""
    skills = []
    for item in sorted(directory.iterdir()):
        if item.is_dir() and (item / 'SKILL.md').exists():
            skills.append(item)
    return skills


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_all.py <skills_directory>")
        sys.exit(1)

    directory = Path(sys.argv[1]).resolve()

    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        sys.exit(1)

    skills = find_skills(directory)

    if not skills:
        print(f"❌ No skills found in {directory}")
        sys.exit(1)

    print(f"\n🔍 Validating {len(skills)} skills in {directory}\n")
    print("-" * 60)

    total_errors = 0
    total_warnings = 0

    for skill_path in skills:
        result = validate_skill(skill_path)

        if result.is_valid and not result.warnings:
            print(f"✅ {result.skill_name}")
        elif result.is_valid:
            print(f"⚠️  {result.skill_name}")
            for warning in result.warnings:
                print(f"    ⚠ {warning}")
                total_warnings += 1
        else:
            print(f"❌ {result.skill_name}")
            for error in result.errors:
                print(f"    ✗ {error}")
                total_errors += 1
            for warning in result.warnings:
                print(f"    ⚠ {warning}")
                total_warnings += 1

    print("-" * 60)
    print(f"\n📊 Summary: {len(skills)} skills, {total_errors} errors, {total_warnings} warnings")

    if total_errors > 0:
        print("\n❌ Validation failed")
        sys.exit(1)
    else:
        print("\n✅ All skills are valid")
        sys.exit(0)


if __name__ == "__main__":
    main()
