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
| **Local REST API** | HTTP API для Claude | Включить HTTPS, скопировать API Key |
| **MCP Tools** | MCP-сервер | — |

### 3. Настройка Local REST API

`Settings → Local REST API`:
- ✅ Enable HTTPS
- Порт: 27124 (по умолчанию)
- **Скопировать API Key** — понадобится далее

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
    "obsidian-mcp": {
      "command": "/путь/к/vault/.obsidian/plugins/mcp-tools/bin/mcp-server",
      "args": [],
      "env": {
        "OBSIDIAN_API_KEY": "ваш-api-key-из-local-rest-api",
        "OBSIDIAN_API_URL": "https://127.0.0.1:27124"
      }
    }
  }
}
```

**⚠️ Замените:**
- `/путь/к/vault/` — на реальный путь к вашему vault
- `ваш-api-key` — на API Key из Local REST API

### 6. Перезапуск и проверка

1. Полностью закрыть Claude Desktop
2. Убедиться, что Obsidian запущен с открытым vault
3. Запустить Claude Desktop
4. Проверить в чате:
   ```
   Покажи список файлов в корне vault
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

**Проверка 1:** Obsidian запущен?
```bash
# macOS
lsof -i :27124
```

**Проверка 2:** API Key корректный?
```bash
curl -k -H "Authorization: Bearer YOUR_API_KEY" \
  https://127.0.0.1:27124/
```
Должен вернуть: `{"authenticated": true}`

**Проверка 3:** Путь к mcp-server корректный?
```bash
ls -la /путь/к/vault/.obsidian/plugins/mcp-tools/bin/mcp-server
```

### Несколько vault'ов

Каждому vault — свой порт:
- Vault 1: порт 27124
- Vault 2: порт 27125

В конфиге — отдельные записи:
```json
{
  "mcpServers": {
    "vault1-mcp": {
      "env": { "OBSIDIAN_API_URL": "https://127.0.0.1:27124" }
    },
    "vault2-mcp": {
      "env": { "OBSIDIAN_API_URL": "https://127.0.0.1:27125" }
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
- [ ] Установлен Local REST API
- [ ] Установлен MCP Tools
- [ ] Настроен Local REST API (API Key скопирован)

### Claude Desktop
- [ ] Установлен Claude Desktop
- [ ] Создан claude_desktop_config.json
- [ ] Указан путь к mcp-server
- [ ] Указан API Key и URL
- [ ] Перезапущен Claude Desktop

### Проверка
- [ ] Claude видит файлы vault
- [ ] Семантический поиск работает
- [ ] Файлы создаются корректно

---

## Полезные команды Claude

```
# Семантический поиск по смыслу
search_vault_smart: "проблемы с производительностью"

# Текстовый поиск
search_vault_simple: "Иванов"

# Список файлов в папке
list_vault_files: directory="07_PEOPLE"

# Чтение файла
get_vault_file: filename="Dashboard.md"
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
