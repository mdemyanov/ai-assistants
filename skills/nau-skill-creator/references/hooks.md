# Хуки (Hooks)

Хуки — shell-скрипты, которые автоматически выполняются до или после определённых событий в Claude Code.

## Типы хуков

| Тип | Когда срабатывает | Применение |
|-----|------------------|-----------|
| `pre-tool` | Перед вызовом инструмента | Валидация, логирование |
| `post-tool` | После вызова инструмента | Пост-обработка, уведомления |
| `user-prompt-submit` | При отправке сообщения пользователем | Обогащение контекста |
| `notification` | При уведомлении от Claude | Интеграции |

## Структура `.claude/hooks/`

```
.claude/
└── hooks/
    ├── pre-tool/
    │   ├── validate-edit.sh
    │   └── log-bash.sh
    ├── post-tool/
    │   ├── format-code.sh
    │   └── notify-slack.sh
    └── user-prompt-submit/
        └── enrich-context.sh
```

## Создание хука

### Базовый шаблон

```bash
#!/usr/bin/env bash
# Hook: [название]
# Type: [pre-tool|post-tool|user-prompt-submit]
# Description: [что делает]

set -euo pipefail

# Входные данные приходят через stdin как JSON
INPUT=$(cat)

# Парсинг с jq
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input // empty')

# Логика хука
# ...

# Результат — JSON в stdout
echo '{"status": "ok"}'
```

### Pre-tool хук

```bash
#!/usr/bin/env bash
# Hook: validate-edit
# Type: pre-tool
# Description: Проверяет что редактируемый файл не в protected paths

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

if [[ "$TOOL_NAME" == "Edit" || "$TOOL_NAME" == "Write" ]]; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

    # Проверка protected paths
    if [[ "$FILE_PATH" == *"/secrets/"* ]]; then
        echo '{"status": "blocked", "message": "Cannot edit files in /secrets/"}'
        exit 0
    fi
fi

echo '{"status": "ok"}'
```

### Post-tool хук

```bash
#!/usr/bin/env bash
# Hook: format-code
# Type: post-tool
# Description: Форматирует код после Write/Edit

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

if [[ "$TOOL_NAME" == "Edit" || "$TOOL_NAME" == "Write" ]]; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

    # Определяем форматтер по расширению
    case "$FILE_PATH" in
        *.py) python -m black "$FILE_PATH" 2>/dev/null || true ;;
        *.js|*.ts) npx prettier --write "$FILE_PATH" 2>/dev/null || true ;;
        *.go) gofmt -w "$FILE_PATH" 2>/dev/null || true ;;
    esac
fi

echo '{"status": "ok"}'
```

### User-prompt-submit хук

```bash
#!/usr/bin/env bash
# Hook: enrich-context
# Type: user-prompt-submit
# Description: Добавляет контекст к запросу пользователя

set -euo pipefail

INPUT=$(cat)
USER_PROMPT=$(echo "$INPUT" | jq -r '.prompt')

# Добавляем информацию о текущей ветке
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

# Возвращаем обогащённый промт
jq -n --arg prompt "$USER_PROMPT" --arg branch "$BRANCH" \
    '{"prompt": ($prompt + "\n\n[Current branch: " + $branch + "]")}'
```

## Конфигурация хуков

### settings.json

```json
{
  "hooks": {
    "pre-tool": {
      "enabled": true,
      "timeout_ms": 5000
    },
    "post-tool": {
      "enabled": true,
      "timeout_ms": 10000
    }
  }
}
```

### Включение/отключение

- Хук активен если файл исполняемый (`chmod +x`)
- Отключить: убрать execute permission или добавить `.disabled` к имени

## JSON-схема входных данных

### pre-tool / post-tool

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.py",
    "old_string": "...",
    "new_string": "..."
  },
  "session_id": "abc123"
}
```

### user-prompt-submit

```json
{
  "prompt": "Текст сообщения пользователя",
  "session_id": "abc123"
}
```

## JSON-схема ответа

```json
{
  "status": "ok"           // Продолжить выполнение
}

{
  "status": "blocked",     // Заблокировать операцию
  "message": "Причина"     // Сообщение для Claude
}

{
  "prompt": "Новый промт"  // Для user-prompt-submit
}
```

## Интеграция со Skills

### Когда использовать хуки vs skills

| Задача | Хук | Skill |
|--------|-----|-------|
| Валидация перед операцией | Да | Нет |
| Автоформатирование кода | Да | Нет |
| Логирование действий | Да | Нет |
| Сложная бизнес-логика | Нет | Да |
| Интерактивный диалог | Нет | Да |

### Связка skill + hook

Skill может требовать определённые хуки:

```markdown
## Требования

Для работы skill требуется хук `post-tool/format-code.sh`.
Установите из `templates/hook-template/`.
```

## Лучшие практики

1. **Быстрота** — хуки должны выполняться <5 сек
2. **Идемпотентность** — повторный запуск безопасен
3. **Graceful degradation** — при ошибке возвращай `{"status": "ok"}`
4. **Логирование** — пиши логи в stderr, не stdout
5. **Зависимости** — минимизируй внешние зависимости

## Отладка

```bash
# Тест хука вручную
echo '{"tool_name": "Edit", "tool_input": {"file_path": "/test.py"}}' | ./validate-edit.sh

# Проверка синтаксиса
shellcheck ./validate-edit.sh

# Логи
tail -f ~/.claude/logs/hooks.log
```
