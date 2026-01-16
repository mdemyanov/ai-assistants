#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Skill Initializer - Создаёт новый skill из шаблона

Использование:
    python init_skill.py <skill-name> --path <path>

Примеры:
    python init_skill.py my-new-skill --path /Users/user/skills
    python init_skill.py data-analyzer --path ../skills
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Подробное описание — ЧТО делает skill + КОГДА использовать + конкретные триггеры. Это главный механизм активации!]
---

# {skill_title}

[TODO: 1-2 предложения о назначении skill]

## Структурирование Skill

[TODO: Выбери структуру, подходящую для задачи:

**1. Workflow-Based** (для последовательных процессов)
- Когда есть чёткие пошаговые процедуры
- Структура: Overview → Workflow → Step Details

**2. Task-Based** (для коллекций инструментов)
- Когда skill предлагает разные операции
- Структура: Overview → Quick Start → Tasks

**3. Reference-Based** (для стандартов/спецификаций)
- Для гайдлайнов, политик, требований
- Структура: Overview → Guidelines → Specifications

**4. Capabilities-Based** (для интегрированных систем)
- Когда skill предоставляет связанные фичи
- Структура: Overview → Core Capabilities

Паттерны можно комбинировать. Удали эту секцию после выбора структуры.]

## [TODO: Первая секция по выбранной структуре]

[TODO: Добавь контент:
- Примеры кода для технических skills
- Decision trees для сложных workflows
- Конкретные примеры с реалистичными запросами
- Ссылки на scripts/references/assets]

## Resources

Skill включает примеры ресурсов (удали ненужные):

### scripts/
Исполняемый код для повторяющихся операций.
- `example.py` — пример скрипта

### references/
Документация для загрузки в контекст.
- `api_reference.md` — пример референса

### assets/
Файлы для использования в выводе.
- `example_asset.txt` — пример ассета
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Пример скрипта для {skill_name}

Замени реальной реализацией или удали если не нужен.
"""

def main():
    print("Пример скрипта для {skill_name}")
    # TODO: Добавь логику

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# API Reference для {skill_title}

Пример документации для референса.
Замени реальным контентом или удали если не нужен.

## Когда использовать references/

- Подробная API документация
- Детальные гайды по workflow
- Схемы баз данных
- Информация слишком длинная для SKILL.md
- Контент нужен только в определённых сценариях

## Структура

### API Reference
- Overview
- Authentication  
- Endpoints
- Error codes

### Workflow Guide
- Prerequisites
- Step-by-step
- Troubleshooting
"""

EXAMPLE_ASSET = """# Пример Asset

Этот файл демонстрирует назначение assets/.

Assets — файлы НЕ для загрузки в контекст, а для использования в выводе:
- Шаблоны (.pptx, .docx)
- Изображения (.png, .svg)
- Шрифты (.ttf, .woff2)
- Boilerplate код

Замени реальными ассетами или удали директорию.
"""


def title_case_skill_name(skill_name: str) -> str:
    """Конвертирует hyphen-case в Title Case."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name: str, path: str) -> Path | None:
    """
    Инициализирует новую директорию skill с шаблоном.
    
    Returns:
        Path к созданной директории или None при ошибке
    """
    skill_dir = Path(path).resolve() / skill_name
    
    if skill_dir.exists():
        print(f"❌ Ошибка: Директория уже существует: {skill_dir}")
        return None
    
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Создана директория: {skill_dir}")
    except Exception as e:
        print(f"❌ Ошибка создания директории: {e}")
        return None
    
    # Создаём SKILL.md
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )
    
    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content, encoding='utf-8')
        print("✅ Создан SKILL.md")
    except Exception as e:
        print(f"❌ Ошибка создания SKILL.md: {e}")
        return None
    
    # Создаём директории с примерами
    try:
        # scripts/
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(
            EXAMPLE_SCRIPT.format(skill_name=skill_name),
            encoding='utf-8'
        )
        example_script.chmod(0o755)
        print("✅ Создан scripts/example.py")
        
        # references/
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_ref = references_dir / 'api_reference.md'
        example_ref.write_text(
            EXAMPLE_REFERENCE.format(skill_title=skill_title),
            encoding='utf-8'
        )
        print("✅ Создан references/api_reference.md")
        
        # assets/
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET, encoding='utf-8')
        print("✅ Создан assets/example_asset.txt")
        
    except Exception as e:
        print(f"❌ Ошибка создания ресурсов: {e}")
        return None
    
    print(f"\n✅ Skill '{skill_name}' инициализирован: {skill_dir}")
    print("\nСледующие шаги:")
    print("1. Заполни TODO в SKILL.md и обнови description")
    print("2. Кастомизируй или удали примеры в scripts/, references/, assets/")
    print("3. Запусти quick_validate.py для проверки")
    
    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Использование: python init_skill.py <skill-name> --path <path>")
        print("\nТребования к имени:")
        print("  - Hyphen-case (например, 'data-analyzer')")
        print("  - Только lowercase, цифры, дефисы")
        print("  - Максимум 64 символа")
        print("\nПримеры:")
        print("  python init_skill.py my-skill --path ./skills")
        print("  python init_skill.py api-helper --path /Users/user/skills")
        sys.exit(1)
    
    skill_name = sys.argv[1]
    path = sys.argv[3]
    
    print(f"🚀 Инициализация skill: {skill_name}")
    print(f"   Путь: {path}\n")
    
    result = init_skill(skill_name, path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
