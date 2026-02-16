#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""
Configure MCP servers in Claude Desktop.

This script sets up the aigrep MCP server in claude_desktop_config.json
for both macOS and Linux.
"""

import os
import sys
import json
import platform
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

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


def get_claude_config_path() -> Optional[Path]:
    """
    Get path to claude_desktop_config.json based on OS.

    Returns:
        Path to config file or None if OS not supported
    """
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


def backup_config(config_path: Path) -> bool:
    """
    Create a backup of the original config file.

    Args:
        config_path: Path to config file

    Returns:
        True if backup created or file doesn't exist, False on error
    """
    if not config_path.exists():
        return True

    backup_path = config_path.parent / f"claude_desktop_config.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    try:
        with open(config_path, "r") as f:
            backup_content = f.read()
        with open(backup_path, "w") as f:
            f.write(backup_content)
        print_success(f"Backup created: {backup_path}")
        return True
    except Exception as e:
        print_error(f"Failed to create backup: {str(e)}")
        return False


def load_config(config_path: Path) -> Dict[str, Any]:
    """
    Load Claude Desktop config from JSON file.

    Args:
        config_path: Path to config file

    Returns:
        Config dictionary, or empty dict if file doesn't exist
    """
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            return config
        except json.JSONDecodeError as e:
            print_error(f"Invalid JSON in config file: {str(e)}")
            return {}
    return {}


def save_config(config_path: Path, config: Dict[str, Any]) -> bool:
    """
    Save Claude Desktop config to JSON file.

    Args:
        config_path: Path to config file
        config: Config dictionary

    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure parent directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Validate JSON by attempting to serialize
        json.dumps(config)

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print_success(f"Config saved to {config_path}")
        return True
    except (OSError, json.JSONDecodeError) as e:
        print_error(f"Failed to save config: {str(e)}")
        return False


def setup_aigrep_mcp(config: Dict[str, Any], vault_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Add or update aigrep MCP server configuration.

    Args:
        config: Current config dictionary
        vault_path: Optional path to vault directory

    Returns:
        Updated config dictionary
    """
    # Ensure mcpServers section exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Get vault path
    if vault_path is None:
        vault_path = str(Path.home() / ".claude" / "vault")

    # aigrep MCP configuration
    aigrep_config = {
        "command": "uv",
        "args": ["run", "aigrep"],
        "env": {
            "AIGREP_VAULT_PATH": vault_path
        }
    }

    # Check if aigrep already configured
    if "aigrep" in config["mcpServers"]:
        print_warning("aigrep MCP already configured, updating...")
    else:
        print_info("Adding aigrep MCP configuration...")

    config["mcpServers"]["aigrep"] = aigrep_config
    print_success("aigrep MCP configured")

    return config


def main() -> int:
    """Main function."""
    print(f"\n{BOLD}Setting up MCP servers for Claude Desktop{RESET}\n")

    # Get config path
    config_path = get_claude_config_path()
    if config_path is None:
        print_error("Unsupported operating system")
        return 1

    print_info(f"Config path: {config_path}")

    # Create backup if config exists
    if config_path.exists():
        if not backup_config(config_path):
            return 1

    # Load current config
    config = load_config(config_path)
    print_success("Config loaded")

    # Setup aigrep MCP
    config = setup_aigrep_mcp(config)

    # Save updated config
    if not save_config(config_path, config):
        return 1

    print(f"\n{BOLD}MCP Setup Complete{RESET}")
    print_success("Claude Desktop is ready to use aigrep MCP")
    print_info("Please restart Claude Desktop for changes to take effect")

    return 0


if __name__ == "__main__":
    sys.exit(main())
