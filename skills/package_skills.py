#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0"]
# ///
"""
Skill Packager — создание ZIP-архивов для Claude Desktop skills.

Упаковывает skills из исходной директории в ZIP-архивы с версионированием.
Поддерживает упаковку отдельных skills или всех сразу.

Использование:
    python package_skills.py <source_dir> <output_dir> [--skill NAME] [--all]
    
Примеры:
    # Упаковать все skills
    python package_skills.py . ./dist --all
    
    # Упаковать конкретный skill
    python package_skills.py . ./dist --skill correspondence-2
    
    # Показать список skills без упаковки
    python package_skills.py . ./dist --list

Требования:
    - Python 3.7+
    - PyYAML (pip install pyyaml)
"""

import argparse
import os
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    print("❌ Требуется PyYAML: pip install pyyaml")
    sys.exit(1)


# Файлы/директории, которые НЕ включаем в архив
EXCLUDE_PATTERNS = [
    '__pycache__',
    '.DS_Store',
    '.git',
    '*.pyc',
    '*.pyo',
    '.env',
    '_meta.md',  # Obsidian metadata, не нужна для Claude Desktop
    '.obsidian',
    'package_skills.py',  # Сам скрипт упаковки
]


def should_exclude(path: Path) -> bool:
    """Проверяет, нужно ли исключить файл/директорию."""
    name = path.name
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith('*'):
            if name.endswith(pattern[1:]):
                return True
        elif name == pattern:
            return True
    return False


def extract_version_from_skill(skill_path: Path) -> Optional[str]:
    """Извлекает версию из SKILL.md frontmatter или _meta.md."""
    # Сначала пробуем SKILL.md
    skill_md = skill_path / 'SKILL.md'
    if skill_md.exists():
        content = skill_md.read_text(encoding='utf-8')
        # Ищем version в frontmatter
        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                if isinstance(frontmatter, dict) and 'version' in frontmatter:
                    return str(frontmatter['version'])
            except yaml.YAMLError:
                pass
    
    # Пробуем _meta.md
    meta_md = skill_path / '_meta.md'
    if meta_md.exists():
        content = meta_md.read_text(encoding='utf-8')
        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                if isinstance(frontmatter, dict) and 'version' in frontmatter:
                    return str(frontmatter['version'])
            except yaml.YAMLError:
                pass
    
    return None


def extract_skill_info(skill_path: Path) -> dict:
    """Извлекает информацию о skill из SKILL.md."""
    info = {
        'name': skill_path.name,
        'version': None,
        'description': None,
    }
    
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return info
    
    content = skill_md.read_text(encoding='utf-8')
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1))
            if isinstance(frontmatter, dict):
                info['name'] = frontmatter.get('name', skill_path.name)
                info['version'] = frontmatter.get('version')
                desc = frontmatter.get('description', '')
                # Обрезаем description для отображения
                info['description'] = desc[:80] + '...' if len(desc) > 80 else desc
        except yaml.YAMLError:
            pass
    
    # Пробуем _meta.md для версии если не нашли
    if not info['version']:
        info['version'] = extract_version_from_skill(skill_path)
    
    return info


def is_valid_skill(path: Path) -> bool:
    """Проверяет, является ли директория валидным skill."""
    return path.is_dir() and (path / 'SKILL.md').exists()


def list_skills(source_dir: Path) -> list[dict]:
    """Возвращает список всех skills в директории."""
    skills = []
    for item in sorted(source_dir.iterdir()):
        if is_valid_skill(item):
            info = extract_skill_info(item)
            info['path'] = item
            skills.append(info)
    return skills


def package_skill(skill_path: Path, output_dir: Path, include_version: bool = True) -> Optional[Path]:
    """
    Упаковывает skill в ZIP-архив.
    
    Args:
        skill_path: Путь к директории skill
        output_dir: Директория для сохранения архива
        include_version: Добавлять версию в имя файла
    
    Returns:
        Путь к созданному архиву или None при ошибке
    """
    if not is_valid_skill(skill_path):
        print(f"❌ Не найден SKILL.md в {skill_path}")
        return None
    
    info = extract_skill_info(skill_path)
    skill_name = info['name']
    version = info['version']
    
    # Формируем имя архива
    if include_version and version:
        archive_name = f"{skill_name}_v{version}.zip"
    else:
        archive_name = f"{skill_name}.zip"
    
    output_path = output_dir / archive_name
    
    # Создаём архив
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(skill_path):
                # Фильтруем директории
                dirs[:] = [d for d in dirs if not should_exclude(Path(d))]
                
                for file in files:
                    file_path = Path(root) / file
                    if should_exclude(file_path):
                        continue
                    
                    # Относительный путь внутри архива
                    arcname = str(file_path.relative_to(skill_path.parent))
                    zf.write(file_path, arcname)
        
        return output_path
    
    except Exception as e:
        print(f"❌ Ошибка при создании архива: {e}")
        return None


def create_installation_guide(skills: list[dict], output_dir: Path) -> Path:
    """Создаёт инструкцию по установке."""
    guide_path = output_dir / "INSTALLATION_GUIDE.md"
    
    content = f"""# Инструкция по установке Skills для Claude Desktop

Дата создания: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Быстрая установка

### macOS / Linux

```bash
# 1. Найдите директорию skills Claude Desktop
# Обычно: ~/Library/Application Support/Claude/skills/

# 2. Распакуйте нужный архив
unzip <skill-name>.zip -d ~/Library/Application\\ Support/Claude/skills/

# 3. Перезапустите Claude Desktop
```

### Windows

1. Откройте `%APPDATA%\\Claude\\skills\\` в проводнике
2. Распакуйте архив в эту директорию
3. Перезапустите Claude Desktop

---

## Доступные Skills

| Skill | Версия | Описание |
|-------|--------|----------|
"""
    
    for skill in skills:
        version = skill.get('version', 'N/A')
        desc = skill.get('description', '')
        content += f"| {skill['name']} | {version} | {desc} |\n"
    
    content += """
---

## Структура Skill

Каждый skill содержит:

```
skill-name/
├── SKILL.md          # Основные инструкции (обязательно)
├── scripts/          # Исполняемые скрипты (опционально)
├── references/       # Документация для контекста (опционально)
└── assets/           # Шаблоны и ресурсы (опционально)
```

## Проверка установки

После установки skill должен автоматически активироваться при соответствующих запросах.
Триггеры для каждого skill описаны в поле `description` файла SKILL.md.

## Обновление Skills

1. Удалите старую версию из директории skills
2. Распакуйте новый архив
3. Перезапустите Claude Desktop
"""
    
    guide_path.write_text(content, encoding='utf-8')
    return guide_path


def main():
    parser = argparse.ArgumentParser(
        description='Упаковка Claude Desktop skills в ZIP-архивы',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s . ./dist --all              # Упаковать все skills
  %(prog)s . ./dist --skill my-skill   # Упаковать один skill
  %(prog)s . ./dist --list             # Показать список skills
        """
    )
    
    parser.add_argument('source_dir', help='Директория с skills')
    parser.add_argument('output_dir', help='Директория для архивов')
    parser.add_argument('--skill', '-s', help='Имя конкретного skill для упаковки')
    parser.add_argument('--all', '-a', action='store_true', help='Упаковать все skills')
    parser.add_argument('--list', '-l', action='store_true', help='Показать список skills')
    parser.add_argument('--no-version', action='store_true', help='Не добавлять версию в имя файла')
    parser.add_argument('--no-guide', action='store_true', help='Не создавать инструкцию')
    
    args = parser.parse_args()
    
    source_dir = Path(args.source_dir).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    
    if not source_dir.exists():
        print(f"❌ Директория не найдена: {source_dir}")
        sys.exit(1)
    
    # Получаем список skills
    skills = list_skills(source_dir)
    
    if not skills:
        print(f"❌ Skills не найдены в {source_dir}")
        sys.exit(1)
    
    # Режим списка
    if args.list:
        print(f"\n📦 Skills в {source_dir}:\n")
        print(f"{'Имя':<25} {'Версия':<10} {'Описание'}")
        print("-" * 80)
        for skill in skills:
            version = skill.get('version') or 'N/A'
            desc = (skill.get('description') or '')[:40]
            print(f"{skill['name']:<25} {version:<10} {desc}")
        print(f"\nВсего: {len(skills)} skills")
        return
    
    # Нужно указать --all или --skill
    if not args.all and not args.skill:
        parser.print_help()
        print("\n❌ Укажите --all для упаковки всех skills или --skill NAME для конкретного")
        sys.exit(1)
    
    # Создаём output директорию
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Определяем какие skills упаковывать
    if args.skill:
        skills_to_pack = [s for s in skills if s['name'] == args.skill]
        if not skills_to_pack:
            print(f"❌ Skill '{args.skill}' не найден")
            print(f"Доступные: {', '.join(s['name'] for s in skills)}")
            sys.exit(1)
    else:
        skills_to_pack = skills
    
    # Упаковываем
    print(f"\n🚀 Упаковка skills в {output_dir}\n")
    
    packed = []
    for skill in skills_to_pack:
        print(f"📦 {skill['name']}...", end=' ')
        result = package_skill(
            skill['path'], 
            output_dir, 
            include_version=not args.no_version
        )
        if result:
            size_kb = result.stat().st_size / 1024
            print(f"✅ {result.name} ({size_kb:.1f} KB)")
            packed.append(skill)
        else:
            print("❌ Ошибка")
    
    # Создаём инструкцию
    if packed and not args.no_guide:
        guide = create_installation_guide(packed, output_dir)
        print(f"\n📄 Создана инструкция: {guide.name}")
    
    print(f"\n✅ Упаковано: {len(packed)}/{len(skills_to_pack)} skills")
    print(f"📁 Результат: {output_dir}")


if __name__ == "__main__":
    main()
