---
name: tg-parser
description: Обработка экспортов Telegram Desktop через tg-parser. Используй при "разбери телеграм чат", "экспорт из телеграма", "сделай дайджест чата", "кто упоминается в чате", "разбей по топикам форум", "подготовь для базы знаний", "статистика чата". Два режима — MCP tools (Claude Desktop) и CLI через Bash (Claude Code). Use cases — дайджест, лог решений, анализ топиков, активность участников, упоминания, подготовка KB, заметки из обсуждений.
---

# tg-parser — Обработка экспортов Telegram

Парсинг и анализ JSON-экспортов Telegram Desktop через MCP или CLI. **tg-parser:** v1.2.0

## Core Principles

1. **Tool Detection First** — Определи режим работы (MCP/CLI) перед началом
2. **Filters > Full Parse** — Фильтруй данные на этапе парсинга, не после
3. **Output Format Matters** — Markdown для анализа, JSON/CSV для интеграций, KB для базы знаний
4. **Chunk Large Exports** — >50MB = используй chunking или streaming

## Определение режима работы

### Алгоритм

**Claude Desktop (MCP предпочтителен):**
1. Попробуй вызвать `tg-parser:get_chat_statistics` с путём к файлу
2. Успех → режим MCP
3. Ошибка "tool not found" → проверь CLI

**Claude Code / Bash:**
1. `tg-parser --version`
2. Успех → режим CLI
3. Ошибка → предложи установку: `pip install tg-parser` или `uv tool install tg-parser`

### Таблица эквивалентов

| Задача | MCP Tool | CLI Command |
|--------|----------|-------------|
| Парсинг с фильтрами | `parse_telegram_export` | `tg-parser parse` |
| Разбивка на чанки | `chunk_telegram_export` | `tg-parser chunk` |
| Статистика чата | `get_chat_statistics` | `tg-parser stats` |
| Список участников | `list_chat_participants` | `tg-parser stats` |
| Список топиков | `list_chat_topics` | `tg-parser split-topics --list` |
| Анализ упоминаний | `list_mentioned_users` | `tg-parser mentions` |

## Быстрый выбор workflow

| Use Case | Фильтры | Формат | Chunking |
|----------|---------|--------|----------|
| Еженедельный дайджест | `--last-days 7` | markdown | — |
| Лог решений | `--contains "решили\|договорились\|утвердили"` | markdown | — |
| Анализ топика форума | `--topics "название"` или `split-topics` | markdown | topic |
| Активность участников | — | stats → json | — |
| Отслеживание упоминаний | `--mentions @user` | markdown | — |
| Подготовка для KB | фильтры по теме | kb-template | daily |
| Заметки из обсуждений | `--senders`, `--contains` | markdown | conversation |

## Workflow: Обработка чата

### 1. Получи путь к файлу экспорта

**Входные данные:**
- JSON-файл из Telegram Desktop (Export chat history → JSON)
- Типичный путь: `~/Downloads/ChatExport_YYYY-MM-DD/result.json`

### 2. Определи цель обработки

| Цель | Уточняющий вопрос |
|------|-------------------|
| Дайджест | За какой период? |
| Поиск решений | Какие ключевые слова/паттерны? |
| По топикам | Конкретный топик или все? |
| Статистика | Общая или по участнику? |
| KB | Какая структура целевой KB? |

### 3. Выбери фильтры

> Детали: `references/filters.md`

**Основные:**
- `--date-from YYYY-MM-DD` / `--date-to YYYY-MM-DD` — период
- `--last-days N` / `--last-hours N` — относительный период
- `--senders "Имя1,Имя2"` — конкретные отправители
- `--topics "Топик1,Топик2"` — топики форума
- `--contains "regex"` — поиск по содержимому

**Дополнительные:**
- `--mentions @username` — где упоминается
- `--has-attachment` — только с вложениями
- `--has-reactions` — только с реакциями
- `--exclude-forwards` — без пересланных
- `--include-service` — включить сервисные сообщения

### 4. Выбери формат вывода

| Формат | Когда использовать | Опция |
|--------|-------------------|-------|
| markdown | Анализ Claude, чтение | `-f markdown` |
| json | Программная обработка | `-f json` |
| csv | Excel, импорт | `-f csv` |
| kb-template | Obsidian/Notion | `-f kb` |

### 5. Примени chunking (для больших файлов)

| Стратегия | Когда | Опция |
|-----------|-------|-------|
| fixed | Равные части | `--strategy fixed --max-tokens 4000` |
| conversation | По диалогам | `--strategy conversation` |
| topic | По топикам форума | `--strategy topic` |
| daily | По дням | `--strategy daily` |

### 6. Выполни команду

**MCP режим:**
```
tg-parser:parse_telegram_export
  input_path: "/path/to/result.json"
  last_days: 7
  output_format: "markdown"
```

**CLI режим:**
```bash
tg-parser parse /path/to/result.json \
  --last-days 7 \
  -f markdown \
  -o ./output/
```

### 7. Проанализируй результат

После получения данных:
- **Дайджест** → суммаризация ключевых тем, участников, решений
- **Лог решений** → структурированный список с датами и ответственными
- **KB** → адаптация под структуру целевой базы знаний

## Примеры по use cases

### Еженедельный дайджест

**MCP:**
```
tg-parser:parse_telegram_export
  input_path: "/path/to/result.json"
  last_days: 7
  output_format: "markdown"
```

**CLI:**
```bash
tg-parser parse /path/to/result.json --last-days 7 -f markdown -o ./digest/
```

### Лог решений

**MCP:**
```
tg-parser:parse_telegram_export
  input_path: "/path/to/result.json"
  contains: "решили|договорились|утвердили|одобрено"
  output_format: "markdown"
```

**CLI:**
```bash
tg-parser parse /path/to/result.json \
  --contains "решили|договорились|утвердили|одобрено" \
  -f markdown -o ./decisions/
```

### Разбивка форума по топикам

**MCP:**
```
tg-parser:chunk_telegram_export
  input_path: "/path/to/result.json"
  strategy: "topic"
  output_format: "markdown"
```

**CLI:**
```bash
tg-parser split-topics /path/to/result.json -o ./topics/
```

### Статистика чата

**MCP:**
```
tg-parser:get_chat_statistics
  input_path: "/path/to/result.json"
  include_top_senders: true
  group_by_topic: true
```

**CLI:**
```bash
tg-parser stats /path/to/result.json --format table --top-senders 10
```

### Подготовка для базы знаний

**CLI:**
```bash
tg-parser parse /path/to/result.json \
  --date-from 2026-01-01 \
  --topics "architecture,decisions" \
  --exclude-service \
  -f kb \
  -o ./kb/

tg-parser chunk ./kb/full.md \
  --strategy daily \
  --max-tokens 4000 \
  -o ./kb/chunks/
```

## Ограничения

- **Только JSON-экспорты** из Telegram Desktop (не API-экспорты)
- **Streaming** для >50MB — только CLI режим (`--streaming`)
- **Regex фильтры** чувствительны к регистру по умолчанию
- **KB-template** требует адаптации под конкретную структуру KB
- **Топики форума** определяются по `topic_created` сервисным сообщениям

## Resources

- `references/filters.md` — детальное описание всех 9 фильтров
- `references/cli-reference.md` — полный справочник CLI команд
- `references/output-formats.md` — форматы вывода и их особенности
