#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0"]
# ///
"""
Skill Validator - Проверяет корректность структуры skill

Использование:
    python quick_validate.py <skill-directory>

Примеры:
    python quick_validate.py ./my-skill
    python quick_validate.py /path/to/skills/data-analyzer
"""

import sys
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ Требуется PyYAML: pip install pyyaml")
    sys.exit(1)


ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}


def validate_skill(skill_path: str) -> tuple[bool, str]:
    """
    Валидирует структуру skill.
    
    Returns:
        (is_valid, message)
    """
    skill_path = Path(skill_path)
    
    # Проверяем SKILL.md
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md не найден"
    
    content = skill_md.read_text(encoding='utf-8')
    
    # Проверяем frontmatter
    if not content.startswith('---'):
        return False, "Нет YAML frontmatter (должен начинаться с ---)"
    
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Некорректный формат frontmatter"
    
    frontmatter_text = match.group(1)
    
    # Парсим YAML
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter должен быть YAML словарём"
    except yaml.YAMLError as e:
        return False, f"Ошибка YAML: {e}"
    
    # Проверяем неожиданные поля
    unexpected = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        return False, (
            f"Неожиданные поля: {', '.join(sorted(unexpected))}. "
            f"Допустимые: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )
    
    # Проверяем обязательные поля
    if 'name' not in frontmatter:
        return False, "Отсутствует обязательное поле 'name'"
    if 'description' not in frontmatter:
        return False, "Отсутствует обязательное поле 'description'"
    
    # Валидируем name
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"'name' должен быть строкой, получен {type(name).__name__}"
    
    name = name.strip()
    if name:
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Имя '{name}' должно быть в hyphen-case (только lowercase, цифры, дефисы)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Имя '{name}' не может начинаться/заканчиваться дефисом или содержать --"
        if len(name) > 64:
            return False, f"Имя слишком длинное ({len(name)} символов). Максимум 64."
    
    # Валидируем description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"'description' должен быть строкой, получен {type(description).__name__}"
    
    description = description.strip()
    if description:
        if '<' in description or '>' in description:
            return False, "Description не может содержать угловые скобки (< или >)"
        if len(description) > 1024:
            return False, f"Description слишком длинный ({len(description)} символов). Максимум 1024."
    
    # Проверяем наличие TODO
    if '[TODO' in content:
        return False, "SKILL.md содержит незаполненные [TODO] плейсхолдеры"
    
    return True, "✅ Skill валиден!"


def main():
    if len(sys.argv) != 2:
        print("Использование: python quick_validate.py <skill-directory>")
        print("\nПримеры:")
        print("  python quick_validate.py ./my-skill")
        print("  python quick_validate.py /path/to/skill")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    print(f"🔍 Валидация: {skill_path}\n")
    
    valid, message = validate_skill(skill_path)
    print(message)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
