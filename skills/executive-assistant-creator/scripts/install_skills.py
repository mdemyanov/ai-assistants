#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests>=2.28"]
# ///

"""
Install required skills for executive-assistant-creator.

This script downloads 7 skills from GitHub repositories and installs them
to ~/.claude/skills/
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional
import requests
from urllib.parse import urljoin

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_success(msg: str) -> None:
    """Print success message in green."""
    print(f"{GREEN}✓{RESET} {msg}")


def print_error(msg: str) -> None:
    """Print error message in red."""
    print(f"{RED}✗{RESET} {msg}", file=sys.stderr)


def print_warning(msg: str) -> None:
    """Print warning message in yellow."""
    print(f"{YELLOW}⚠{RESET} {msg}")


def print_info(msg: str) -> None:
    """Print info message."""
    print(f"{BOLD}→{RESET} {msg}")


def get_skills_dir() -> Path:
    """Get or create ~/.claude/skills directory."""
    skills_dir = Path.home() / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    return skills_dir


def clone_skill_from_github(
    repo_url: str, skill_path: str, skill_name: str, target_dir: Path
) -> bool:
    """
    Clone a skill from GitHub repository.

    Args:
        repo_url: GitHub repository URL
        skill_path: Path to skill within repo (e.g., 'skills/aigrep')
        skill_name: Name of the skill
        target_dir: Target directory to clone to

    Returns:
        True if successful, False otherwise
    """
    print_info(f"Installing {skill_name}...")

    skill_target = target_dir / skill_name

    # If already exists, skip
    if skill_target.exists():
        print_warning(f"{skill_name} already exists, skipping")
        return True

    try:
        # Use sparse checkout for efficiency
        temp_dir = Path("/tmp") / f"github-{skill_name}-{os.urandom(4).hex()}"
        temp_dir.mkdir(exist_ok=True)

        # Initialize sparse git repo
        subprocess.run(
            ["git", "clone", "--depth", "1", "--filter=blob:none",
             "--sparse", repo_url, str(temp_dir)],
            check=True,
            capture_output=True,
            timeout=30
        )

        # Checkout the specific path
        subprocess.run(
            ["git", "-C", str(temp_dir), "sparse-checkout", "set", skill_path],
            check=True,
            capture_output=True,
            timeout=30
        )

        # Copy skill to target
        source = temp_dir / skill_path
        if source.exists():
            # Copy the skill content (get the last component as the skill dir)
            skill_source = source if source.name == skill_name else source / skill_name
            if not skill_source.exists():
                # The skill dir might be the immediate child
                skill_source = source
            shutil.copytree(skill_source, skill_target)
            print_success(f"{skill_name} installed to {skill_target}")
        else:
            print_error(f"Could not find {skill_path} in {repo_url}")
            return False

        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
        return True

    except subprocess.TimeoutExpired:
        print_error(f"Timeout cloning {skill_name}")
        return False
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to clone {skill_name}: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as e:
        print_error(f"Error installing {skill_name}: {str(e)}")
        return False


def install_with_uv(package_name: str) -> bool:
    """
    Install a tool using uv.

    Args:
        package_name: Package name (e.g., 'tg-parser')

    Returns:
        True if successful, False otherwise
    """
    print_info(f"Installing {package_name} with uv...")

    try:
        subprocess.run(
            ["uv", "tool", "install", package_name],
            check=True,
            capture_output=True,
            timeout=60
        )
        print_success(f"{package_name} installed via uv")
        return True
    except FileNotFoundError:
        print_error("uv is not installed. Please install uv first: pip install uv")
        return False
    except subprocess.TimeoutExpired:
        print_error(f"Timeout installing {package_name} with uv")
        return False
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install {package_name}: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as e:
        print_error(f"Error installing {package_name}: {str(e)}")
        return False


def main() -> int:
    """Main function."""
    print(f"\n{BOLD}Installing skills for executive-assistant-creator{RESET}\n")

    skills_dir = get_skills_dir()
    print_info(f"Skills directory: {skills_dir}\n")

    # Define skills to install
    # Format: (repo_url, skill_path, skill_name, install_method)
    skills = [
        ("https://github.com/mdemyanov/ai-assistants", "skills/aigrep", "aigrep", "clone"),
        ("https://github.com/mdemyanov/ai-assistants", "skills/correspondence-2", "correspondence-2", "clone"),
        ("https://github.com/mdemyanov/ai-assistants", "skills/meeting-prep", "meeting-prep", "clone"),
        ("https://github.com/mdemyanov/ai-assistants", "skills/meeting-debrief", "meeting-debrief", "clone"),
        ("https://github.com/mdemyanov/ai-assistants", "skills/tg-parser", "tg-parser", "uv"),
        ("https://github.com/anthropics/skills", "skills/xlsx", "xlsx", "clone"),
        ("https://github.com/anthropics/skills", "skills/docx", "docx", "clone"),
    ]

    results = {}

    for repo_url, skill_path, skill_name, method in skills:
        if method == "clone":
            results[skill_name] = clone_skill_from_github(
                repo_url, skill_path, skill_name, skills_dir
            )
        elif method == "uv":
            results[skill_name] = install_with_uv(skill_name)

    # Summary
    print(f"\n{BOLD}Installation Summary{RESET}")
    print("-" * 50)

    successful = sum(1 for v in results.values() if v)
    total = len(results)

    for skill_name, success in results.items():
        status = f"{GREEN}✓{RESET}" if success else f"{RED}✗{RESET}"
        print(f"{status} {skill_name}")

    print("-" * 50)
    print(f"Installed: {successful}/{total}")

    if successful == total:
        print_success("All skills installed successfully!")
        return 0
    else:
        print_error(f"Failed to install {total - successful} skill(s)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
