#!/usr/bin/env bash
# Установка git hooks для проекта AI Assistants
# Запуск: ./scripts/install-hooks.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
GIT_HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
SRC_HOOKS_DIR="$SCRIPT_DIR/git-hooks"

echo "Installing git hooks..."

# Проверяем, что мы в git репозитории
if [ ! -d "$PROJECT_ROOT/.git" ]; then
    echo "ERROR: Not a git repository"
    exit 1
fi

# Создаём директорию hooks если не существует
mkdir -p "$GIT_HOOKS_DIR"

# Устанавливаем pre-commit hook
if [ -f "$SRC_HOOKS_DIR/pre-commit" ]; then
    cp "$SRC_HOOKS_DIR/pre-commit" "$GIT_HOOKS_DIR/pre-commit"
    chmod +x "$GIT_HOOKS_DIR/pre-commit"
    echo "Installed: pre-commit"
else
    echo "Warning: pre-commit hook not found in $SRC_HOOKS_DIR"
fi

echo ""
echo "Git hooks installed successfully!"
echo "Hooks location: $GIT_HOOKS_DIR"
