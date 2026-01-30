#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0", "requests>=2.28"]
# ///
"""
Update Skill — обновление skill из указанного source.

Использование:
    python update_skill.py <skill_path>   # Обновить один skill
    python update_skill.py --all          # Обновить все skills с source
    python update_skill.py --list         # Показать skills с source

Примеры:
    python update_skill.py skills/gramax
    python update_skill.py --all
"""

import argparse
import os
import re
import shutil
import sys
import tempfile
import zipfile
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
    import yaml
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Install with: pip install pyyaml requests")
    sys.exit(1)


def extract_meta(skill_path: Path) -> dict | None:
    """Извлекает метаданные из _meta.md."""
    meta_file = skill_path / '_meta.md'
    if not meta_file.exists():
        return None

    content = meta_file.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None

    try:
        meta = yaml.safe_load(match.group(1))
        if isinstance(meta, dict):
            return meta
    except yaml.YAMLError:
        pass

    return None


def parse_github_url(url: str) -> tuple[str, str] | None:
    """Парсит GitHub URL и возвращает (owner, repo)."""
    parsed = urlparse(url)
    if 'github.com' not in parsed.netloc:
        return None

    parts = parsed.path.strip('/').split('/')
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None


def download_github_zipball(owner: str, repo: str, branch: str = 'main') -> bytes | None:
    """Скачивает zipball репозитория с GitHub."""
    url = f"https://api.github.com/repos/{owner}/{repo}/zipball/{branch}"
    headers = {'Accept': 'application/vnd.github+json'}

    # Используем токен если доступен
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'

    try:
        response = requests.get(url, headers=headers, timeout=60, allow_redirects=True)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"❌ Download failed: {e}")
        return None


def update_meta_date(skill_path: Path) -> None:
    """Обновляет поле updated в _meta.md."""
    meta_file = skill_path / '_meta.md'
    if not meta_file.exists():
        return

    content = meta_file.read_text(encoding='utf-8')
    today = date.today().isoformat()

    # Обновляем поле updated
    updated_content = re.sub(
        r'^(updated:\s*)[\d-]+',
        f'\\g<1>{today}',
        content,
        flags=re.MULTILINE
    )

    if updated_content != content:
        meta_file.write_text(updated_content, encoding='utf-8')


def update_skill(skill_path: Path, dry_run: bool = False) -> bool:
    """Обновляет skill из указанного source."""
    skill_path = skill_path.resolve()
    skill_name = skill_path.name

    if not skill_path.exists():
        print(f"❌ Skill not found: {skill_path}")
        return False

    meta = extract_meta(skill_path)
    if not meta:
        print(f"⚠️  {skill_name}: _meta.md not found or invalid")
        return False

    source = meta.get('source')
    if not source:
        print(f"⚠️  {skill_name}: source not specified")
        return False

    source_path = meta.get('source_path', '')

    # Парсим GitHub URL
    github_info = parse_github_url(source)
    if not github_info:
        print(f"❌ {skill_name}: unsupported source URL (only GitHub supported)")
        return False

    owner, repo = github_info
    print(f"📥 {skill_name}: fetching from {owner}/{repo}...")

    if dry_run:
        print(f"   (dry run - skipping actual update)")
        return True

    # Скачиваем репозиторий
    zipball = download_github_zipball(owner, repo)
    if not zipball:
        return False

    # Распаковываем во временную директорию
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        zip_path = tmp_path / 'repo.zip'

        zip_path.write_bytes(zipball)

        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(tmp_path)

        # GitHub zipball распаковывается в директорию owner-repo-hash
        extracted_dirs = [d for d in tmp_path.iterdir() if d.is_dir()]
        if not extracted_dirs:
            print(f"❌ {skill_name}: failed to extract archive")
            return False

        repo_root = extracted_dirs[0]

        # Определяем source directory
        if source_path:
            source_dir = repo_root / source_path
            if not source_dir.exists():
                print(f"❌ {skill_name}: source_path '{source_path}' not found in repo")
                return False
        else:
            source_dir = repo_root

        # Сохраняем локальный _meta.md
        local_meta = skill_path / '_meta.md'
        meta_backup = None
        if local_meta.exists():
            meta_backup = local_meta.read_text(encoding='utf-8')

        # Копируем файлы
        exclude = {'__pycache__', '.DS_Store', '.git', '_meta.md', '.obsidian'}
        files_copied = 0

        for item in source_dir.iterdir():
            if item.name in exclude:
                continue

            dest = skill_path / item.name

            if item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest, ignore=shutil.ignore_patterns(*exclude))
            else:
                shutil.copy2(item, dest)

            files_copied += 1

        # Восстанавливаем _meta.md
        if meta_backup:
            local_meta.write_text(meta_backup, encoding='utf-8')

        # Обновляем дату
        update_meta_date(skill_path)

        print(f"✅ {skill_name}: updated ({files_copied} items)")
        return True


def find_skills_with_source(skills_dir: Path) -> list[Path]:
    """Находит все skills с указанным source."""
    skills = []
    for item in sorted(skills_dir.iterdir()):
        if item.is_dir():
            meta = extract_meta(item)
            if meta and meta.get('source'):
                skills.append(item)
    return skills


def cmd_update(args):
    """Обновить один skill."""
    skill_path = Path(args.path).resolve()
    success = update_skill(skill_path, dry_run=args.dry_run)
    sys.exit(0 if success else 1)


def cmd_all(args):
    """Обновить все skills с source."""
    skills_dir = Path(args.skills_dir).resolve()

    if not skills_dir.exists():
        print(f"❌ Directory not found: {skills_dir}")
        sys.exit(1)

    skills = find_skills_with_source(skills_dir)

    if not skills:
        print(f"No skills with source found in {skills_dir}")
        sys.exit(0)

    print(f"\n🔄 Updating {len(skills)} skills...\n")

    success_count = 0
    for skill_path in skills:
        if update_skill(skill_path, dry_run=args.dry_run):
            success_count += 1

    print(f"\n📊 Updated: {success_count}/{len(skills)}")
    sys.exit(0 if success_count == len(skills) else 1)


def cmd_list(args):
    """Показать skills с source."""
    skills_dir = Path(args.skills_dir).resolve()

    if not skills_dir.exists():
        print(f"❌ Directory not found: {skills_dir}")
        sys.exit(1)

    skills = find_skills_with_source(skills_dir)

    if not skills:
        print(f"No skills with source found in {skills_dir}")
        sys.exit(0)

    print(f"\n📦 Skills with source ({skills_dir}):\n")
    print(f"{'Name':<25} {'Source'}")
    print("-" * 70)

    for skill_path in skills:
        meta = extract_meta(skill_path)
        source = meta.get('source', '') if meta else ''
        source_path = meta.get('source_path', '') if meta else ''
        display = f"{source}"
        if source_path:
            display += f" → {source_path}"
        print(f"{skill_path.name:<25} {display[:45]}")

    print(f"\nTotal: {len(skills)} skills")


def main():
    parser = argparse.ArgumentParser(
        description='Update Skill — обновление skill из указанного source',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python update_skill.py skills/gramax     # Update single skill
  python update_skill.py --all             # Update all skills with source
  python update_skill.py --list            # List skills with source
        """
    )

    parser.add_argument(
        'path',
        nargs='?',
        help='Path to skill directory'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Update all skills with source'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List skills with source'
    )
    parser.add_argument(
        '--skills-dir',
        default='skills',
        help='Skills directory (default: skills)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be updated without making changes'
    )

    args = parser.parse_args()

    if args.list:
        cmd_list(args)
    elif args.all:
        cmd_all(args)
    elif args.path:
        cmd_update(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
