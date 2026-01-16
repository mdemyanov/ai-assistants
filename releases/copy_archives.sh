#!/bin/bash
# copy_archives.sh — Копирование архивов skills в releases/dist
#
# Запуск из директории AI assistants:
#   bash releases/copy_archives.sh
#
# Или сгенерируйте архивы напрямую:
#   cd skills && python package_skills.py . ../releases/dist --all

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$BASE_DIR/skills"
DIST_DIR="$SCRIPT_DIR/dist"

echo "📦 Генерация архивов skills..."
echo "   Источник: $SKILLS_DIR"
echo "   Назначение: $DIST_DIR"
echo ""

# Проверяем наличие package_skills.py
if [ ! -f "$SKILLS_DIR/package_skills.py" ]; then
    echo "❌ Не найден package_skills.py в $SKILLS_DIR"
    exit 1
fi

# Создаём директорию dist если нет
mkdir -p "$DIST_DIR"

# Запускаем упаковку
cd "$SKILLS_DIR"
python3 package_skills.py . "$DIST_DIR" --all --no-guide

echo ""
echo "✅ Готово! Архивы в $DIST_DIR:"
ls -la "$DIST_DIR"/*.zip 2>/dev/null || echo "   (архивы не найдены)"
