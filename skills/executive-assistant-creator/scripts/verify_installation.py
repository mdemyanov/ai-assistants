#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""
Verify successful installation of executive-assistant-creator.

This script checks that all required components are properly installed
and configured.
"""

import os
import sys
import json
import platform
from pathlib import Path
from typing import Optional, List, Tuple

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
    print(f"{RED}✗{RESET} {msg}")


def print_warning(msg: str) -> None:
    """Print warning message in yellow."""
    print(f"{YELLOW}⚠{RESET} {msg}")


def print_info(msg: str) -> None:
    """Print info message."""
    print(f"{BOLD}→{RESET} {msg}")


def get_claude_config_path() -> Optional[Path]:
    """Get path to claude_desktop_config.json based on OS."""
    system = platform.system()

    if system == "Darwin":  # macOS
        config_path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Linux":
        config_path = Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
    elif system == "Windows":
        config_path = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    else:
        return None

    return config_path


class VerificationReport:
    """Manage verification report."""

    def __init__(self):
        self.checks: List[Tuple[str, bool, str]] = []

    def add_check(self, name: str, success: bool, message: str) -> None:
        """Add a check result."""
        self.checks.append((name, success, message))

    def print_report(self) -> None:
        """Print formatted report."""
        print(f"\n{BOLD}Verification Report{RESET}")
        print("=" * 60)

        for name, success, message in self.checks:
            status = f"{GREEN}✓{RESET}" if success else f"{RED}✗{RESET}"
            print(f"{status} {name}")
            if message:
                print(f"  {message}")

        print("=" * 60)

        passed = sum(1 for _, success, _ in self.checks if success)
        total = len(self.checks)

        print(f"\n{BOLD}Summary{RESET}: {passed}/{total} checks passed")

        if passed == total:
            print_success("All checks passed!")
        else:
            print_warning(f"{total - passed} check(s) failed")

    def all_passed(self) -> bool:
        """Return True if all checks passed."""
        return all(success for _, success, _ in self.checks)


def verify_vault_structure(vault_path: Path) -> Tuple[bool, str]:
    """Verify vault directory structure (folders 00-99)."""
    if not vault_path.exists():
        return False, f"Vault path does not exist: {vault_path}"

    # Check for numbered folders
    folders_found = 0
    for i in range(100):
        folder = vault_path / f"{i:02d}"
        if folder.exists() and folder.is_dir():
            folders_found += 1

    if folders_found == 100:
        return True, f"All 100 folders (00-99) found"
    else:
        return False, f"Only {folders_found}/100 folders found"


def verify_vault_files(vault_path: Path) -> Tuple[bool, str]:
    """Verify required files in vault."""
    required_files = ["SYSTEM_PROMPT.md", "CLAUDE.md"]
    missing = []

    for filename in required_files:
        file_path = vault_path / filename
        if not file_path.exists():
            missing.append(filename)

    if not missing:
        return True, "All required files found"
    else:
        return False, f"Missing files: {', '.join(missing)}"


def verify_skills_installed() -> Tuple[bool, str]:
    """Verify all 7 skills are installed."""
    skills_dir = Path.home() / ".claude" / "skills"
    required_skills = [
        "aigrep",
        "correspondence-2",
        "meeting-prep",
        "meeting-debrief",
        "tg-parser",
        "xlsx",
        "docx",
    ]

    if not skills_dir.exists():
        return False, f"Skills directory does not exist: {skills_dir}"

    installed_skills = []
    for skill_name in required_skills:
        skill_path = skills_dir / skill_name
        if skill_path.exists() and skill_path.is_dir():
            installed_skills.append(skill_name)

    if len(installed_skills) == len(required_skills):
        return True, f"All {len(required_skills)} skills installed"
    else:
        missing = [s for s in required_skills if s not in installed_skills]
        return False, f"Missing skills: {', '.join(missing)}"


def verify_skill_structure(skill_name: str) -> Tuple[bool, str]:
    """Verify a skill has required structure."""
    skill_path = Path.home() / ".claude" / "skills" / skill_name

    if not skill_path.exists():
        return False, f"Skill not found: {skill_name}"

    # Check for SKILL.md
    if not (skill_path / "SKILL.md").exists():
        return False, f"SKILL.md not found in {skill_name}"

    return True, f"{skill_name} structure valid"


def verify_mcp_configured() -> Tuple[bool, str]:
    """Verify MCP configuration in Claude Desktop."""
    config_path = get_claude_config_path()

    if config_path is None:
        return False, "Could not determine config path for your OS"

    if not config_path.exists():
        return False, f"Claude Desktop config not found: {config_path}"

    try:
        with open(config_path, "r") as f:
            config = json.load(f)

        if "mcpServers" not in config:
            return False, "No mcpServers section in config"

        if "aigrep" not in config["mcpServers"]:
            return False, "aigrep MCP not configured"

        aigrep_config = config["mcpServers"]["aigrep"]
        if "command" not in aigrep_config:
            return False, "aigrep MCP missing command configuration"

        return True, "aigrep MCP properly configured"

    except json.JSONDecodeError:
        return False, "Invalid JSON in Claude Desktop config"
    except Exception as e:
        return False, f"Error reading config: {str(e)}"


def verify_aigrep_config() -> Tuple[bool, str]:
    """Verify aigrep configuration file."""
    possible_configs = [
        Path.home() / ".claude" / "aigrep" / "config.yaml",
        Path.home() / ".config" / "aigrep" / "config.yaml",
        Path.home() / ".aigrep" / "config.yaml",
    ]

    for config_path in possible_configs:
        if config_path.exists():
            return True, f"aigrep config found: {config_path}"

    return False, "aigrep configuration not found"


def verify_uv_installed() -> Tuple[bool, str]:
    """Verify uv is installed."""
    try:
        import subprocess
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.decode().strip()
            return True, f"uv installed: {version}"
        else:
            return False, "uv found but returned error"
    except FileNotFoundError:
        return False, "uv not found in PATH. Install with: pip install uv"
    except Exception as e:
        return False, f"Error checking uv: {str(e)}"


def main() -> int:
    """Main function."""
    print(f"\n{BOLD}Verifying executive-assistant-creator installation{RESET}\n")

    report = VerificationReport()

    # Get vault path
    vault_path = Path.home() / ".claude" / "vault"

    # Verification checks
    print_info("Running verification checks...\n")

    # 1. Vault structure
    success, message = verify_vault_structure(vault_path)
    report.add_check("Vault structure (00-99 folders)", success, message)

    # 2. Vault files
    success, message = verify_vault_files(vault_path)
    report.add_check("Vault files (SYSTEM_PROMPT.md, CLAUDE.md)", success, message)

    # 3. Skills installed
    success, message = verify_skills_installed()
    report.add_check("All 7 skills installed", success, message)

    # 4. Individual skill structures
    skills_dir = Path.home() / ".claude" / "skills"
    if skills_dir.exists():
        for skill_name in ["aigrep", "correspondence-2", "meeting-prep"]:
            success, message = verify_skill_structure(skill_name)
            report.add_check(f"Skill structure: {skill_name}", success, "")

    # 5. MCP configuration
    success, message = verify_mcp_configured()
    report.add_check("MCP configuration in Claude Desktop", success, message)

    # 6. aigrep configuration
    success, message = verify_aigrep_config()
    report.add_check("aigrep configuration file", success, message)

    # 7. uv installed
    success, message = verify_uv_installed()
    report.add_check("uv package manager", success, message)

    # Print report
    report.print_report()

    # Print next steps
    if report.all_passed():
        print(f"\n{BOLD}Next Steps{RESET}")
        print("1. Restart Claude Desktop")
        print("2. Start using the executive-assistant-creator skill")
        print("3. Access aigrep for vault search")
        return 0
    else:
        print(f"\n{BOLD}Troubleshooting{RESET}")
        print("Review failed checks above and:")
        print("1. Run install_skills.py to install missing skills")
        print("2. Run setup_mcp.py to configure MCP servers")
        print("3. Run copy_aigrep_config.py to set up aigrep")
        print("4. Check file permissions and disk space")
        return 1


if __name__ == "__main__":
    sys.exit(main())
