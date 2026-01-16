#!/usr/bin/env bash
# Hook: [название]
# Type: [pre-tool|post-tool|user-prompt-submit]
# Description: [что делает хук]
#
# Входные данные: JSON через stdin
# Выходные данные: JSON через stdout
#
# Примеры входных данных:
#
# pre-tool / post-tool:
# {
#   "tool_name": "Edit",
#   "tool_input": {"file_path": "/path/to/file.py", ...},
#   "session_id": "abc123"
# }
#
# user-prompt-submit:
# {
#   "prompt": "Текст сообщения пользователя",
#   "session_id": "abc123"
# }
#
# Примеры ответов:
#
# Продолжить выполнение:
# {"status": "ok"}
#
# Заблокировать операцию (только pre-tool):
# {"status": "blocked", "message": "Причина блокировки"}
#
# Изменить промт (только user-prompt-submit):
# {"prompt": "Модифицированный промт"}

set -euo pipefail

# Читаем входные данные
INPUT=$(cat)

# Парсим с помощью jq
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
# TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input // empty')
# SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')
# PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty')

# ==============================================================================
# ЛОГИКА ХУКА
# ==============================================================================

# Пример: логирование всех Edit операций
if [[ "$TOOL_NAME" == "Edit" ]]; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Edit: $FILE_PATH" >> /tmp/claude-hooks.log
fi

# Пример: блокировка записи в protected paths
# if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
#     FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
#     if [[ "$FILE_PATH" == *"/secrets/"* || "$FILE_PATH" == *"/.env"* ]]; then
#         echo '{"status": "blocked", "message": "Cannot modify protected files"}'
#         exit 0
#     fi
# fi

# Пример: обогащение промта (для user-prompt-submit)
# PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty')
# BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
# jq -n --arg prompt "$PROMPT" --arg branch "$BRANCH" \
#     '{"prompt": ($prompt + "\n\n[Branch: " + $branch + "]")}'
# exit 0

# ==============================================================================
# ВОЗВРАЩАЕМ РЕЗУЛЬТАТ
# ==============================================================================

# По умолчанию — продолжить выполнение
echo '{"status": "ok"}'
