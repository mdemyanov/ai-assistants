#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0", "requests>=2.28"]
# ///
"""
AI Skills CLI — управление skills для Claude Desktop.

Использование:
    python ai-skills-cli.py list              # Показать установленные skills
    python ai-skills-cli.py remote            # Показать доступные для загрузки
    python ai-skills-cli.py install <name>    # Установить skill
    python ai-skills-cli.py update            # Обновить все skills
    python ai-skills-cli.py validate <path>   # Валидировать skill
    python ai-skills-cli.py package <path>    # Упаковать skill в ZIP
"""

import argparse
import json
import os
import platform
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Optional

try:
    import requests
    import yaml
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install pyyaml requests")
    sys.exit(1)


# Конфигурация
REPO = "USER/ai-assistants"  # TODO: Заменить на реальный репозиторий
API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"


def get_skills_dir() -> Path:
    """Определяет директорию skills в зависимости от OS."""
    custom_dir = os.environ.get('CLAUDE_SKILLS_DIR')
    if custom_dir:
        return Path(custom_dir)

    system = platform.system()

    if system == 'Darwin':
        return Path.home() / 'Library' / 'Application Support' / 'Claude' / 'skills'
    elif system == 'Linux':
        # Проверяем WSL
        try:
            with open('/proc/version', 'r') as f:
                if 'microsoft' in f.read().lower():
                    # WSL - используем Windows путь через APPDATA
                    appdata = os.environ.get('APPDATA')
                    if appdata:
                        return Path(appdata) / 'Claude' / 'skills'
        except FileNotFoundError:
            pass
        return Path.home() / '.config' / 'claude' / 'skills'
    elif system == 'Windows':
        appdata = os.environ.get('APPDATA')
        if appdata:
            return Path(appdata) / 'Claude' / 'skills'
        return Path.home() / 'AppData' / 'Roaming' / 'Claude' / 'skills'
    else:
        return Path.home() / '.claude' / 'skills'


def extract_skill_info(skill_path: Path) -> Optional[dict]:
    """Извлекает информацию о skill из SKILL.md."""
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return None

    content = skill_md.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None

    try:
        frontmatter = yaml.safe_load(match.group(1))
        if isinstance(frontmatter, dict):
            return {
                'name': frontmatter.get('name', skill_path.name),
                'description': frontmatter.get('description', '')[:80],
                'version': frontmatter.get('version'),
                'path': str(skill_path)
            }
    except yaml.YAMLError:
        pass

    return None


def cmd_list(args):
    """Показать установленные skills."""
    skills_dir = get_skills_dir()

    if not skills_dir.exists():
        print(f"Skills directory not found: {skills_dir}")
        return

    skills = []
    for item in sorted(skills_dir.iterdir()):
        if item.is_dir():
            info = extract_skill_info(item)
            if info:
                skills.append(info)

    if not skills:
        print("No skills installed")
        print(f"\nInstall with: python ai-skills-cli.py install <name>")
        return

    print(f"\n📦 Installed skills ({skills_dir}):\n")
    print(f"{'Name':<25} {'Version':<10} {'Description'}")
    print("-" * 70)

    for skill in skills:
        version = skill.get('version') or 'N/A'
        desc = skill.get('description', '')[:40]
        print(f"{skill['name']:<25} {version:<10} {desc}")

    print(f"\nTotal: {len(skills)} skills")


def cmd_remote(args):
    """Показать доступные skills из последнего релиза."""
    print("🔍 Fetching latest release...\n")

    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        release = response.json()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch release: {e}")
        return

    version = release.get('tag_name', 'unknown')
    print(f"Latest release: {version}\n")
    print(f"{'Skill':<30} {'Size':<10}")
    print("-" * 40)

    for asset in release.get('assets', []):
        name = asset['name']
        size_kb = asset['size'] / 1024
        skill_name = re.sub(r'_v[\d.]+\.zip$', '', name).replace('.zip', '')
        print(f"{skill_name:<30} {size_kb:.1f} KB")


def cmd_install(args):
    """Установить skill из релиза."""
    skill_name = args.name
    skills_dir = get_skills_dir()

    print(f"🔍 Fetching latest release...")

    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        release = response.json()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch release: {e}")
        return

    # Найти asset
    asset = None
    for a in release.get('assets', []):
        if a['name'].startswith(skill_name):
            asset = a
            break

    if not asset:
        print(f"❌ Skill '{skill_name}' not found")
        print("\nAvailable skills:")
        for a in release.get('assets', []):
            name = re.sub(r'_v[\d.]+\.zip$', '', a['name']).replace('.zip', '')
            print(f"  - {name}")
        return

    # Скачать
    print(f"📥 Downloading {asset['name']}...")
    try:
        download_response = requests.get(asset['browser_download_url'], timeout=60)
        download_response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Download failed: {e}")
        return

    # Создать директорию
    skills_dir.mkdir(parents=True, exist_ok=True)

    # Распаковать
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
        tmp.write(download_response.content)
        tmp_path = tmp.name

    try:
        print(f"📦 Installing to {skills_dir}...")
        with zipfile.ZipFile(tmp_path, 'r') as zf:
            zf.extractall(skills_dir)
        print(f"✅ Installed {skill_name}")
    finally:
        os.unlink(tmp_path)


def cmd_update(args):
    """Обновить все установленные skills."""
    skills_dir = get_skills_dir()

    if not skills_dir.exists():
        print("No skills installed")
        return

    print("🔄 Updating all skills...")

    # Получить список установленных
    installed = []
    for item in skills_dir.iterdir():
        if item.is_dir() and (item / 'SKILL.md').exists():
            installed.append(item.name)

    if not installed:
        print("No skills to update")
        return

    # Получить релиз
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        release = response.json()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch release: {e}")
        return

    # Обновить каждый skill
    for skill_name in installed:
        # Найти asset
        asset = None
        for a in release.get('assets', []):
            if a['name'].startswith(skill_name):
                asset = a
                break

        if not asset:
            print(f"⚠️  {skill_name}: not found in release")
            continue

        print(f"📥 Updating {skill_name}...")

        try:
            download_response = requests.get(asset['browser_download_url'], timeout=60)
            download_response.raise_for_status()

            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
                tmp.write(download_response.content)
                tmp_path = tmp.name

            with zipfile.ZipFile(tmp_path, 'r') as zf:
                zf.extractall(skills_dir)

            os.unlink(tmp_path)
            print(f"✅ {skill_name} updated")

        except Exception as e:
            print(f"❌ {skill_name}: {e}")

    print("\n✅ Update complete")


def cmd_validate(args):
    """Валидировать skill."""
    skill_path = Path(args.path).resolve()

    if not skill_path.exists():
        print(f"❌ Path not found: {skill_path}")
        return

    # Импортируем валидатор
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from validate_all import validate_skill, find_skills
    except ImportError:
        print("❌ validate_all.py not found")
        return

    if skill_path.is_dir() and (skill_path / 'SKILL.md').exists():
        # Валидация одного skill
        result = validate_skill(skill_path)
        if result.is_valid:
            print(f"✅ {result.skill_name} is valid")
        else:
            print(f"❌ {result.skill_name} has errors:")
            for error in result.errors:
                print(f"  - {error}")
    else:
        # Валидация директории со skills
        skills = find_skills(skill_path)
        if not skills:
            print(f"No skills found in {skill_path}")
            return

        all_valid = True
        for sp in skills:
            result = validate_skill(sp)
            if result.is_valid:
                print(f"✅ {result.skill_name}")
            else:
                print(f"❌ {result.skill_name}")
                for error in result.errors:
                    print(f"  - {error}")
                all_valid = False

        if all_valid:
            print(f"\n✅ All {len(skills)} skills are valid")
        else:
            print(f"\n❌ Some skills have errors")


def cmd_package(args):
    """Упаковать skill в ZIP."""
    skill_path = Path(args.path).resolve()
    output_dir = Path(args.output).resolve() if args.output else Path.cwd()

    if not skill_path.exists():
        print(f"❌ Path not found: {skill_path}")
        return

    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        print(f"❌ SKILL.md not found in {skill_path}")
        return

    info = extract_skill_info(skill_path)
    if not info:
        print("❌ Cannot extract skill info")
        return

    name = info['name']
    version = info.get('version')

    if version:
        archive_name = f"{name}_v{version}.zip"
    else:
        archive_name = f"{name}.zip"

    output_path = output_dir / archive_name

    # Создать архив
    output_dir.mkdir(parents=True, exist_ok=True)

    exclude = {'__pycache__', '.DS_Store', '.git', '_meta.md', '.obsidian'}

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_path):
            dirs[:] = [d for d in dirs if d not in exclude]
            for file in files:
                if file in exclude or file.endswith('.pyc'):
                    continue
                file_path = Path(root) / file
                arcname = str(file_path.relative_to(skill_path.parent))
                zf.write(file_path, arcname)

    size_kb = output_path.stat().st_size / 1024
    print(f"✅ Created {output_path} ({size_kb:.1f} KB)")


def main():
    parser = argparse.ArgumentParser(
        description='AI Skills CLI — управление skills для Claude Desktop',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # list
    subparsers.add_parser('list', help='Show installed skills')

    # remote
    subparsers.add_parser('remote', help='Show available skills from release')

    # install
    install_parser = subparsers.add_parser('install', help='Install a skill')
    install_parser.add_argument('name', help='Skill name to install')

    # update
    subparsers.add_parser('update', help='Update all installed skills')

    # validate
    validate_parser = subparsers.add_parser('validate', help='Validate a skill')
    validate_parser.add_argument('path', help='Path to skill or directory')

    # package
    package_parser = subparsers.add_parser('package', help='Package skill to ZIP')
    package_parser.add_argument('path', help='Path to skill directory')
    package_parser.add_argument('-o', '--output', help='Output directory')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        'list': cmd_list,
        'remote': cmd_remote,
        'install': cmd_install,
        'update': cmd_update,
        'validate': cmd_validate,
        'package': cmd_package
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
