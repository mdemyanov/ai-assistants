---
id: tg-parser
version: 1.0.0
created: 2026-01-20
updated: 2026-01-20
author: Max Demyanov
status: active
type: skill
tags: [telegram, parsing, export, chat, mcp, cli, digest, knowledge-base]
tg_parser_version: 1.2.0
---

# tg-parser

## Description

Skill для обработки JSON-экспортов Telegram Desktop через инструмент tg-parser. Поддерживает два режима работы: MCP tools для Claude Desktop и CLI через Bash для Claude Code. Автоматически определяет доступный режим.

## Triggers / Use Cases

- "разбери телеграм чат"
- "экспорт из телеграма"
- "сделай дайджест чата"
- "кто упоминается в чате"
- "разбей форум по топикам"
- "подготовь чат для базы знаний"
- "статистика чата за неделю"
- "найди решения в переписке"

## Components

| Component | Purpose |
|-----------|---------|
| SKILL.md | Основные инструкции, workflow, примеры |
| references/filters.md | Детальное описание 9 фильтров |
| references/cli-reference.md | Справочник CLI команд |
| references/output-formats.md | Форматы вывода |

## Dependencies

- **tg-parser** v1.2.0+ — CLI/MCP инструмент
- Установка: `pip install tg-parser` или `uv tool install tg-parser`
- MCP setup: `tg-parser mcp-config --apply`

## Changelog

### v1.0.0 (2026-01-20)
- Initial release
- Dual-mode support: MCP tools + CLI
- 7 use cases: дайджест, лог решений, анализ топиков, активность, упоминания, KB, заметки
- 9 фильтров: дата, отправитель, топик, содержимое, упоминания, вложения, реакции, пересылка, сервисные
- 4 формата вывода: markdown, json, csv, kb-template
- 4 стратегии chunking: fixed, conversation, topic, daily
- References: filters, cli-reference, output-formats
