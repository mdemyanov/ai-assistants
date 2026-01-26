# Техническая настройка AI-ассистента

**Время настройки:** ~1-2 часа

---

## Быстрый старт

### 1. Установка Obsidian

1. Скачать: https://obsidian.md/download
2. Создать новый vault (папку):
   ```
   ~/Documents/[Название вашей базы]/
   ```
3. Открыть vault в Obsidian

### 2. Установка плагинов Obsidian

`Settings → Community plugins → Browse`

| Плагин | Зачем | Настройка |
|--------|-------|-----------|
| **Dataview** | Динамические запросы | Включить JavaScript Queries |
| **Templater** | Шаблоны с переменными | Указать папку шаблонов |

### 3. Установка aigrep MCP server

aigrep — семантический поиск по базе знаний через MCP.

**Требования:**
- Homebrew (macOS)
- Ollama для локальных эмбеддингов

```bash
# Установить Homebrew (если нет)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установить Ollama
brew install ollama

# Запустить Ollama и загрузить модель
ollama serve &
ollama pull mxbai-embed-large

# Установить UV (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 4. Установка Claude Desktop

1. Скачать: https://claude.ai/download
2. Установить, войти в аккаунт

### 5. Настройка MCP в Claude

Создать/отредактировать файл конфигурации:

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Содержимое:**
```json
{
  "mcpServers": {
    "aigrep": {
      "command": "uvx",
      "args": ["--from", "aigrep", "aigrep-mcp"],
      "env": {
        "AIGREP_VAULTS": "/путь/к/vault:Название_vault"
      }
    }
  }
}
```

**⚠️ Замените:**
- `/путь/к/vault` — на реальный путь к вашему Obsidian vault
- `Название_vault` — имя для обращения к vault (без пробелов)

**Пример:**
```json
"AIGREP_VAULTS": "/Users/john/Documents/MyKnowledge:MyKB"
```

### 6. Первый запуск и индексация

1. Полностью закрыть Claude Desktop
2. Убедиться, что Ollama запущен (`ollama serve`)
3. Запустить Claude Desktop
4. При первом обращении aigrep проиндексирует vault (может занять несколько минут)
5. Проверить в чате:
   ```
   Покажи статистику vault
   ```

---

## Структура папок

Создать в vault:

```
Vault/
├── 01_CONTEXT/
│   ├── role_scope.md
│   ├── constraints.md
│   └── stakeholders.md
├── 02_DOMAIN/              # Переименовать под роль
├── 03_METHODOLOGY/
├── 04_TEMPLATES/
│   ├── template_1-1.md
│   ├── template_person.md
│   └── template_decision.md
├── 05_DECISIONS/
├── 06_CURRENT/
│   └── priorities.md
├── 07_PEOPLE/
├── Dashboard.md
├── CLAUDE.md
└── SYSTEM_PROMPT.md
```

---

## Troubleshooting

### MCP не подключается

**Проверка 1:** Ollama запущен?
```bash
curl http://localhost:11434/api/tags
```
Должен вернуть список моделей.

**Проверка 2:** UV установлен?
```bash
uv --version
```

**Проверка 3:** aigrep работает?
```bash
uvx --from aigrep aigrep-mcp --help
```

### Несколько vault'ов

В переменной `AIGREP_VAULTS` через запятую:
```json
{
  "mcpServers": {
    "aigrep": {
      "command": "uvx",
      "args": ["--from", "aigrep", "aigrep-mcp"],
      "env": {
        "AIGREP_VAULTS": "/path/to/vault1:Vault1,/path/to/vault2:Vault2"
      }
    }
  }
}
```

### Dataview не показывает данные

1. Проверить frontmatter (--- в начале и конце)
2. Проверить регистр полей (важен!)
3. Проверить путь в запросе FROM

---

## Чек-лист настройки

### Obsidian
- [ ] Установлен Obsidian
- [ ] Создан vault
- [ ] Установлен Dataview
- [ ] Установлен Templater

### aigrep
- [ ] Установлен Homebrew
- [ ] Установлен Ollama
- [ ] Загружена модель mxbai-embed-large
- [ ] Установлен UV

### Claude Desktop
- [ ] Установлен Claude Desktop
- [ ] Создан claude_desktop_config.json
- [ ] Указан путь к vault в AIGREP_VAULTS
- [ ] Перезапущен Claude Desktop

### Проверка
- [ ] Claude видит vault (vault_stats работает)
- [ ] Семантический поиск работает (search_vault)
- [ ] Файлы читаются корректно

---

## Полезные команды aigrep

```
# Семантический поиск (по смыслу)
aigrep:search_vault
  vault_name: "MyKB"
  query: "проблемы с производительностью"
  search_type: "hybrid"
  limit: 10

# Текстовый поиск (точное совпадение)
aigrep:search_vault
  vault_name: "MyKB"
  query: "Иванов"
  search_type: "fts"
  limit: 10

# Статистика vault
aigrep:vault_stats
  vault_name: "MyKB"

# Список vault'ов
aigrep:list_vaults
```

---

## Опциональные расширения

### Docling MCP (конвертация PDF/DOCX)

```json
{
  "mcpServers": {
    "docling-mcp": {
      "command": "uvx",
      "args": ["--from", "docling-mcp", "docling-mcp-server"]
    }
  }
}
```

Требует установки UV:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
