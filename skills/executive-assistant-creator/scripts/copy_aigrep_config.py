#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0"]
# ///

"""
Copy aigrep configuration for a new vault.

This script sets up aigrep configuration for a new vault by copying
and updating existing settings.
"""

import os
import sys
import yaml
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

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


def find_aigrep_config() -> Optional[Path]:
    """
    Find existing aigrep configuration file.

    Returns:
        Path to config file or None if not found
    """
    possible_locations = [
        Path.home() / ".claude" / "aigrep" / "config.yaml",
        Path.home() / ".config" / "aigrep" / "config.yaml",
        Path.home() / ".aigrep" / "config.yaml",
        Path.home() / ".local" / "share" / "aigrep" / "config.yaml",
    ]

    for config_path in possible_locations:
        if config_path.exists():
            print_success(f"Found existing config: {config_path}")
            return config_path

    return None


def load_yaml_config(config_path: Path) -> Optional[Dict[str, Any]]:
    """
    Load YAML configuration file.

    Args:
        config_path: Path to config file

    Returns:
        Config dictionary or None on error
    """
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config if config else {}
    except yaml.YAMLError as e:
        print_error(f"Invalid YAML in config: {str(e)}")
        return None
    except Exception as e:
        print_error(f"Failed to load config: {str(e)}")
        return None


def save_yaml_config(config_path: Path, config: Dict[str, Any]) -> bool:
    """
    Save YAML configuration file.

    Args:
        config_path: Path to config file
        config: Config dictionary

    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure parent directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        print_success(f"Config saved to {config_path}")
        return True
    except Exception as e:
        print_error(f"Failed to save config: {str(e)}")
        return False


def create_aigrep_config(
    vault_name: str,
    vault_path: str,
    existing_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create or update aigrep configuration.

    Args:
        vault_name: Name of the vault
        vault_path: Path to vault directory
        existing_config: Optional existing config to use as template

    Returns:
        New configuration dictionary
    """
    # Start with existing config or create new
    if existing_config:
        config = existing_config.copy()
        print_info("Using existing config as template")
    else:
        config = {}

    # Update vault settings
    config["vault_name"] = vault_name
    config["vault_path"] = vault_path

    # Ensure paths section exists
    if "paths" not in config:
        config["paths"] = {}

    # Update index path
    if "index_path" not in config:
        config["index_path"] = str(Path(vault_path) / ".aigrep" / "index.json")

    # Add timestamp
    config["last_updated"] = datetime.now().isoformat()

    # Ensure directories are created
    vault_path_obj = Path(vault_path)
    vault_path_obj.mkdir(parents=True, exist_ok=True)

    index_dir = Path(config["index_path"]).parent
    index_dir.mkdir(parents=True, exist_ok=True)

    print_success(f"Configuration created for vault: {vault_name}")

    return config


def initialize_vault_structure(vault_path: str) -> bool:
    """
    Initialize vault directory structure (folders 00-99).

    Args:
        vault_path: Path to vault directory

    Returns:
        True if successful, False otherwise
    """
    try:
        vault_path_obj = Path(vault_path)

        # Create numbered folders (00-99)
        for i in range(100):
            folder = vault_path_obj / f"{i:02d}"
            folder.mkdir(parents=True, exist_ok=True)

        print_success(f"Vault structure initialized: {vault_path}")
        return True
    except Exception as e:
        print_error(f"Failed to initialize vault structure: {str(e)}")
        return False


def main() -> int:
    """Main function."""
    print(f"\n{BOLD}Setting up aigrep configuration for new vault{RESET}\n")

    # Get vault details
    vault_name = input("Enter vault name (e.g., 'my-vault'): ").strip()
    if not vault_name:
        print_error("Vault name cannot be empty")
        return 1

    default_path = str(Path.home() / ".claude" / "vault")
    vault_path_input = input(f"Enter vault path [{default_path}]: ").strip()
    vault_path = vault_path_input if vault_path_input else default_path

    print(f"\n{BOLD}Configuration Details{RESET}")
    print(f"Vault name: {vault_name}")
    print(f"Vault path: {vault_path}\n")

    # Try to find existing config
    existing_config = None
    existing_config_path = find_aigrep_config()

    if existing_config_path:
        use_existing = input("Use existing config as template? [y/N]: ").strip().lower()
        if use_existing == "y":
            existing_config = load_yaml_config(existing_config_path)
            if existing_config is None:
                return 1

    # Create new config
    config = create_aigrep_config(vault_name, vault_path, existing_config)

    # Determine config save location
    config_dir = Path.home() / ".claude" / "aigrep"
    config_path = config_dir / "config.yaml"

    print_info(f"Saving config to {config_path}")

    # Save config
    if not save_yaml_config(config_path, config):
        return 1

    # Initialize vault structure
    print_info("Initializing vault directory structure...")
    if not initialize_vault_structure(vault_path):
        return 1

    # Create index file
    index_path = Path(config["index_path"])
    try:
        if not index_path.exists():
            with open(index_path, "w") as f:
                json.dump({"version": "1.0", "entries": []}, f, indent=2)
            print_success(f"Index file created: {index_path}")
    except Exception as e:
        print_warning(f"Could not create index file: {str(e)}")

    print(f"\n{BOLD}Configuration Complete{RESET}")
    print_success("aigrep vault is ready to use")
    print_info("Next steps:")
    print("  1. Start adding documents to the vault")
    print(f"  2. Configure in Claude Desktop MCP settings")
    print(f"  3. Use aigrep skill to search your vault")

    return 0


if __name__ == "__main__":
    sys.exit(main())
