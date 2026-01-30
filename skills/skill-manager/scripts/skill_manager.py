#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0", "requests>=2.28"]
# ///
"""
Skill Manager — управление внешними skills.

Команды:
    install <url>    Установить skill из GitHub URL
    update [name]    Обновить skill(s) из source
    list             Показать установленные skills
    check            Проверить доступные обновления

Примеры:
    python skill_manager.py install anthropics/skills/skills/docx --local
    python skill_manager.py install https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md --global
    python skill_manager.py update docx --local
    python skill_manager.py update --all --local
    python skill_manager.py list --local
    python skill_manager.py check --local
"""

import argparse
import os
import re
import shutil
import sys
import tempfile
import zipfile
from dataclasses import dataclass
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


# === Constants ===

GLOBAL_SKILLS_DIR = Path.home() / '.claude' / 'skills'
LOCAL_SKILLS_DIR = Path('skills')


@dataclass
class GitHubRef:
    """GitHub repository reference."""
    owner: str
    repo: str
    branch: str
    path: str  # path to skill directory within repo

    @property
    def source_url(self) -> str:
        return f"https://github.com/{self.owner}/{self.repo}"

    @property
    def raw_url(self) -> str:
        return f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/{self.branch}"


def parse_github_url(url: str) -> GitHubRef | None:
    """
    Parse various GitHub URL formats into GitHubRef.

    Supported formats:
    - https://github.com/owner/repo/blob/branch/path/to/SKILL.md
    - https://github.com/owner/repo/tree/branch/path/to/skill
    - https://raw.githubusercontent.com/owner/repo/branch/path/SKILL.md
    - owner/repo/path (short format, assumes main branch)
    - owner/repo (repo root)
    """
    url = url.strip()

    # Short format: owner/repo or owner/repo/path
    if not url.startswith(('http://', 'https://')):
        parts = url.split('/')
        if len(parts) >= 2:
            owner, repo = parts[0], parts[1]
            path = '/'.join(parts[2:]) if len(parts) > 2 else ''
            return GitHubRef(owner=owner, repo=repo, branch='main', path=path)
        return None

    parsed = urlparse(url)

    # raw.githubusercontent.com format
    if 'raw.githubusercontent.com' in parsed.netloc:
        parts = parsed.path.strip('/').split('/')
        if len(parts) >= 3:
            owner, repo, branch = parts[0], parts[1], parts[2]
            path_parts = parts[3:]
            # Remove SKILL.md from path if present
            if path_parts and path_parts[-1] == 'SKILL.md':
                path_parts = path_parts[:-1]
            path = '/'.join(path_parts)
            return GitHubRef(owner=owner, repo=repo, branch=branch, path=path)
        return None

    # github.com format
    if 'github.com' not in parsed.netloc:
        return None

    parts = parsed.path.strip('/').split('/')
    if len(parts) < 2:
        return None

    owner, repo = parts[0], parts[1]

    # Simple repo URL: github.com/owner/repo
    if len(parts) == 2:
        return GitHubRef(owner=owner, repo=repo, branch='main', path='')

    # URL with blob/tree: github.com/owner/repo/blob/branch/path
    if len(parts) >= 4 and parts[2] in ('blob', 'tree'):
        branch = parts[3]
        path_parts = parts[4:]
        # Remove SKILL.md from path if present
        if path_parts and path_parts[-1] == 'SKILL.md':
            path_parts = path_parts[:-1]
        path = '/'.join(path_parts)
        return GitHubRef(owner=owner, repo=repo, branch=branch, path=path)

    return None


def extract_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None
    try:
        data = yaml.safe_load(match.group(1))
        return data if isinstance(data, dict) else None
    except yaml.YAMLError:
        return None


def extract_meta(skill_path: Path) -> dict | None:
    """Extract metadata from _meta.md file."""
    meta_file = skill_path / '_meta.md'
    if not meta_file.exists():
        return None
    content = meta_file.read_text(encoding='utf-8')
    return extract_frontmatter(content)


def parse_version(version_str: str | None) -> tuple[int, int, int] | None:
    """Parse semver version string to tuple."""
    if not version_str:
        return None
    match = re.match(r'^v?(\d+)\.(\d+)\.(\d+)', str(version_str))
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    return None


def compare_versions(local: str | None, remote: str | None) -> str:
    """Compare versions and return status: 'same', 'minor', 'major', 'unknown'."""
    local_v = parse_version(local)
    remote_v = parse_version(remote)

    if not local_v or not remote_v:
        return 'unknown'

    if local_v == remote_v:
        return 'same'

    if remote_v[0] > local_v[0]:
        return 'major'

    return 'minor'


def get_target_dir(global_install: bool) -> Path:
    """Get target skills directory based on scope."""
    if global_install:
        return GLOBAL_SKILLS_DIR
    return LOCAL_SKILLS_DIR.resolve()


# === GitHub API functions ===

def github_request(url: str, accept: str = 'application/vnd.github+json') -> requests.Response | None:
    """Make authenticated GitHub API request."""
    headers = {'Accept': accept}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'

    try:
        response = requests.get(url, headers=headers, timeout=60, allow_redirects=True)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None


def download_zipball(ref: GitHubRef) -> bytes | None:
    """Download repository zipball."""
    url = f"https://api.github.com/repos/{ref.owner}/{ref.repo}/zipball/{ref.branch}"
    response = github_request(url)
    return response.content if response else None


def fetch_remote_file(ref: GitHubRef, filename: str) -> str | None:
    """Fetch single file content from GitHub."""
    url = f"{ref.raw_url}/{ref.path}/{filename}" if ref.path else f"{ref.raw_url}/{filename}"
    response = github_request(url, accept='text/plain')
    return response.text if response else None


# === Install command ===

def cmd_install(args):
    """Install skill from GitHub URL."""
    ref = parse_github_url(args.url)
    if not ref:
        print(f"❌ Cannot parse URL: {args.url}")
        sys.exit(1)

    target_dir = get_target_dir(args.is_global)

    print(f"📦 Installing from {ref.owner}/{ref.repo}")
    if ref.path:
        print(f"   Path: {ref.path}")

    # Fetch SKILL.md to get skill name
    skill_md = fetch_remote_file(ref, 'SKILL.md')
    if not skill_md:
        print("❌ SKILL.md not found in repository")
        sys.exit(1)

    frontmatter = extract_frontmatter(skill_md)
    skill_name = frontmatter.get('name') if frontmatter else None

    if not skill_name:
        # Fallback to directory name
        skill_name = ref.path.split('/')[-1] if ref.path else ref.repo

    skill_name = skill_name.lower().replace(' ', '-')
    skill_dest = target_dir / skill_name

    if skill_dest.exists() and not args.force:
        print(f"⚠️  Skill '{skill_name}' already exists at {skill_dest}")
        print("   Use --force to overwrite")
        sys.exit(1)

    # Download zipball
    print(f"📥 Downloading {ref.owner}/{ref.repo}@{ref.branch}...")
    zipball = download_zipball(ref)
    if not zipball:
        sys.exit(1)

    # Extract skill
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        zip_path = tmp_path / 'repo.zip'
        zip_path.write_bytes(zipball)

        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(tmp_path)

        # Find extracted directory
        extracted_dirs = [d for d in tmp_path.iterdir() if d.is_dir()]
        if not extracted_dirs:
            print("❌ Failed to extract archive")
            sys.exit(1)

        repo_root = extracted_dirs[0]
        source_dir = repo_root / ref.path if ref.path else repo_root

        if not source_dir.exists():
            print(f"❌ Path '{ref.path}' not found in repository")
            sys.exit(1)

        # Check for SKILL.md
        if not (source_dir / 'SKILL.md').exists():
            print(f"❌ SKILL.md not found in {ref.path or 'repository root'}")
            sys.exit(1)

        # Create target directory
        target_dir.mkdir(parents=True, exist_ok=True)
        if skill_dest.exists():
            shutil.rmtree(skill_dest)

        # Copy files
        exclude = {'__pycache__', '.DS_Store', '.git', '.obsidian'}
        shutil.copytree(source_dir, skill_dest, ignore=shutil.ignore_patterns(*exclude))

        # Create/update _meta.md with source info
        version = frontmatter.get('version') if frontmatter else None
        create_meta(skill_dest, ref, version)

    print(f"✅ Installed '{skill_name}' to {skill_dest}")
    if version:
        print(f"   Version: {version}")


def create_meta(skill_path: Path, ref: GitHubRef, version: str | None):
    """Create or update _meta.md with source information."""
    meta_file = skill_path / '_meta.md'
    today = date.today().isoformat()

    # Check if _meta.md exists and has frontmatter
    existing_meta = extract_meta(skill_path) or {}

    # Merge with new source info
    meta = {
        'source': ref.source_url,
        'source_path': ref.path,
        'installed': existing_meta.get('installed', today),
        'updated': today,
    }
    if version:
        meta['version'] = version

    # Build content
    yaml_content = yaml.dump(meta, default_flow_style=False, allow_unicode=True, sort_keys=False)
    content = f"---\n{yaml_content}---\n"

    meta_file.write_text(content, encoding='utf-8')


# === Update command ===

def cmd_update(args):
    """Update skill(s) from source."""
    target_dir = get_target_dir(args.is_global)

    if not target_dir.exists():
        print(f"❌ Skills directory not found: {target_dir}")
        sys.exit(1)

    if args.all:
        skills = find_skills_with_source(target_dir)
        if not skills:
            print("No skills with source found")
            sys.exit(0)

        print(f"\n🔄 Updating {len(skills)} skills...\n")

        success = 0
        for skill_path in skills:
            if update_single_skill(skill_path, args.force):
                success += 1

        print(f"\n📊 Updated: {success}/{len(skills)}")
        sys.exit(0 if success == len(skills) else 1)

    elif args.name:
        skill_path = target_dir / args.name
        if not skill_path.exists():
            print(f"❌ Skill not found: {args.name}")
            sys.exit(1)

        success = update_single_skill(skill_path, args.force)
        sys.exit(0 if success else 1)

    else:
        print("❌ Specify skill name or use --all")
        sys.exit(1)


def update_single_skill(skill_path: Path, force: bool = False) -> bool:
    """Update single skill from its source."""
    skill_name = skill_path.name
    meta = extract_meta(skill_path)

    if not meta:
        print(f"⚠️  {skill_name}: _meta.md not found")
        return False

    source = meta.get('source')
    if not source:
        print(f"⚠️  {skill_name}: no source specified")
        return False

    source_path = meta.get('source_path', '')
    local_version = meta.get('version')

    # Parse source URL
    ref = parse_github_url(source)
    if not ref:
        print(f"❌ {skill_name}: cannot parse source URL")
        return False

    ref.path = source_path

    print(f"📥 {skill_name}: checking {ref.owner}/{ref.repo}...")

    # Fetch remote SKILL.md to check version
    skill_md = fetch_remote_file(ref, 'SKILL.md')
    if not skill_md:
        print(f"❌ {skill_name}: cannot fetch remote SKILL.md")
        return False

    remote_fm = extract_frontmatter(skill_md)
    remote_version = remote_fm.get('version') if remote_fm else None

    # Compare versions
    status = compare_versions(local_version, remote_version)

    if status == 'same':
        print(f"✓  {skill_name}: already up to date ({local_version})")
        return True

    if status == 'major' and not force:
        print(f"⚠️  {skill_name}: MAJOR update {local_version} → {remote_version}")
        print(f"   Use --force to update")
        return False

    if status == 'unknown':
        print(f"   {skill_name}: version unknown, updating anyway")
    else:
        print(f"   {skill_name}: {local_version or '?'} → {remote_version or '?'}")

    # Download and update
    zipball = download_zipball(ref)
    if not zipball:
        return False

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        zip_path = tmp_path / 'repo.zip'
        zip_path.write_bytes(zipball)

        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(tmp_path)

        extracted_dirs = [d for d in tmp_path.iterdir() if d.is_dir()]
        if not extracted_dirs:
            print(f"❌ {skill_name}: failed to extract")
            return False

        repo_root = extracted_dirs[0]
        source_dir = repo_root / ref.path if ref.path else repo_root

        if not source_dir.exists():
            print(f"❌ {skill_name}: source path not found")
            return False

        # Preserve local _meta.md
        meta_backup = (skill_path / '_meta.md').read_text(encoding='utf-8')

        # Copy files
        exclude = {'__pycache__', '.DS_Store', '.git', '.obsidian', '_meta.md'}

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

        # Restore _meta.md and update
        (skill_path / '_meta.md').write_text(meta_backup, encoding='utf-8')
        update_meta_version(skill_path, remote_version)

    print(f"✅ {skill_name}: updated to {remote_version or 'latest'}")
    return True


def update_meta_version(skill_path: Path, version: str | None):
    """Update version and date in _meta.md."""
    meta_file = skill_path / '_meta.md'
    if not meta_file.exists():
        return

    content = meta_file.read_text(encoding='utf-8')
    today = date.today().isoformat()

    # Update 'updated' field
    content = re.sub(r'^(updated:\s*)[\d-]+', f'\\g<1>{today}', content, flags=re.MULTILINE)

    # Update 'version' field if exists
    if version:
        if re.search(r'^version:', content, flags=re.MULTILINE):
            content = re.sub(r'^(version:\s*).*$', f'\\g<1>{version}', content, flags=re.MULTILINE)
        else:
            # Add version after source_path or source
            content = re.sub(
                r'^(source_path:.*?)$',
                f'\\g<1>\nversion: {version}',
                content,
                flags=re.MULTILINE
            )

    meta_file.write_text(content, encoding='utf-8')


def find_skills_with_source(skills_dir: Path) -> list[Path]:
    """Find all skills with source specified."""
    skills = []
    for item in sorted(skills_dir.iterdir()):
        if item.is_dir():
            meta = extract_meta(item)
            if meta and meta.get('source'):
                skills.append(item)
    return skills


# === List command ===

def cmd_list(args):
    """List installed skills."""
    target_dir = get_target_dir(args.is_global)

    if not target_dir.exists():
        print(f"No skills directory: {target_dir}")
        sys.exit(0)

    skills = list(target_dir.iterdir())
    skills = [s for s in skills if s.is_dir() and (s / 'SKILL.md').exists()]

    if not skills:
        print(f"No skills found in {target_dir}")
        sys.exit(0)

    scope = "global" if args.is_global else "local"
    print(f"\n📦 Installed skills ({scope}):\n")
    print(f"{'Name':<20} {'Version':<10} {'Source'}")
    print("-" * 70)

    for skill_path in sorted(skills):
        meta = extract_meta(skill_path) or {}
        name = skill_path.name
        version = meta.get('version') or '-'
        source = meta.get('source') or '-'
        if source and source != '-':
            source = source.replace('https://github.com/', '')
        print(f"{name:<20} {version:<10} {source[:38]}")

    print(f"\nTotal: {len(skills)} skills")


# === Check command ===

def cmd_check(args):
    """Check for available updates."""
    target_dir = get_target_dir(args.is_global)

    if not target_dir.exists():
        print(f"❌ Skills directory not found: {target_dir}")
        sys.exit(1)

    skills = find_skills_with_source(target_dir)

    if not skills:
        print("No skills with source found")
        sys.exit(0)

    print(f"\n🔍 Checking updates for {len(skills)} skills...\n")

    updates_available = 0

    for skill_path in skills:
        skill_name = skill_path.name
        meta = extract_meta(skill_path)
        source = meta.get('source', '')
        source_path = meta.get('source_path', '')
        local_version = meta.get('version')

        ref = parse_github_url(source)
        if not ref:
            print(f"⚠️  {skill_name}: invalid source")
            continue

        ref.path = source_path

        # Fetch remote version
        skill_md = fetch_remote_file(ref, 'SKILL.md')
        if not skill_md:
            print(f"⚠️  {skill_name}: cannot check remote")
            continue

        remote_fm = extract_frontmatter(skill_md)
        remote_version = remote_fm.get('version') if remote_fm else None

        status = compare_versions(local_version, remote_version)

        if status == 'same':
            print(f"✓  {skill_name}: {local_version} (up to date)")
        elif status == 'major':
            print(f"⚠️  {skill_name}: {local_version} → {remote_version} (MAJOR)")
            updates_available += 1
        elif status == 'minor':
            print(f"📦 {skill_name}: {local_version} → {remote_version}")
            updates_available += 1
        else:
            print(f"?  {skill_name}: version unknown")

    if updates_available:
        print(f"\n{updates_available} update(s) available. Run 'update --all' to update.")


# === Main ===

def main():
    parser = argparse.ArgumentParser(
        description='Skill Manager — управление внешними skills',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  install anthropics/skills/skills/docx --local
  install https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md --global
  update docx --local
  update --all --local
  list --local
  check --global
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command')

    # Install
    p_install = subparsers.add_parser('install', help='Install skill from URL')
    p_install.add_argument('url', help='GitHub URL or owner/repo/path')
    p_install.add_argument('--force', '-f', action='store_true', help='Overwrite existing')
    p_install.add_argument('--local', dest='is_global', action='store_false', default=False,
                          help='Install to ./skills/ (default)')
    p_install.add_argument('--global', dest='is_global', action='store_true',
                          help='Install to ~/.claude/skills/')

    # Update
    p_update = subparsers.add_parser('update', help='Update skill(s)')
    p_update.add_argument('name', nargs='?', help='Skill name to update')
    p_update.add_argument('--all', '-a', action='store_true', help='Update all skills')
    p_update.add_argument('--force', '-f', action='store_true', help='Force major updates')
    p_update.add_argument('--local', dest='is_global', action='store_false', default=False,
                         help='Update in ./skills/ (default)')
    p_update.add_argument('--global', dest='is_global', action='store_true',
                         help='Update in ~/.claude/skills/')

    # List
    p_list = subparsers.add_parser('list', help='List installed skills')
    p_list.add_argument('--local', dest='is_global', action='store_false', default=False,
                       help='List from ./skills/ (default)')
    p_list.add_argument('--global', dest='is_global', action='store_true',
                       help='List from ~/.claude/skills/')

    # Check
    p_check = subparsers.add_parser('check', help='Check for updates')
    p_check.add_argument('--local', dest='is_global', action='store_false', default=False,
                        help='Check in ./skills/ (default)')
    p_check.add_argument('--global', dest='is_global', action='store_true',
                        help='Check in ~/.claude/skills/')

    args = parser.parse_args()

    if args.command == 'install':
        cmd_install(args)
    elif args.command == 'update':
        cmd_update(args)
    elif args.command == 'list':
        cmd_list(args)
    elif args.command == 'check':
        cmd_check(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
