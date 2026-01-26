---
id: aigrep
version: 1.3.1
created: 2026-01-06
updated: 2026-01-21
author: Max Demyanov
status: active
type: skill
tags: [skill, obsidian, knowledge-base, mcp, search, sqlite, lancedb, aigrep, cli]
aigrep_version: 2.0.9
---

# Метаданные skill aigrep

## Changelog

### 1.3.1 (2026-01-21)
- **CLI для Claude Code:** добавлена секция с CLI-командами для операций, недоступных через MCP
- Документированы: doctor, watch, install-service, cluster, config
- Добавлена таблица "CLI vs MCP: когда что использовать"

### 1.3.0 (2026-01-16)
- **Переименование:** obsidian-kb → aigrep (соответствует актуальному названию проекта)
- Поддержка aigrep v2.0.9
- Все MCP-вызовы обновлены: `obsidian-kb:` → `aigrep:`
- Обновлена документация и примеры

### 1.2.0 (2026-01-11)
- Поддержка obsidian-kb v2.0.7 (Storage Layer Release)
- Документирована архитектура Hybrid Storage (SQLite + LanceDB)
- Добавлен Core Principle #6: Hybrid Storage
- Документированы улучшения производительности v2.0:
  - Инкрементальная индексация (~5 сек для 10 файлов)
  - Поиск по свойствам (~10ms вместо ~500ms)
  - Агрегация (~20ms вместо ~1s)
- Документированы: FileWatcher, Embedding Cache, Dual-Write, Дедупликация задач
- Добавлен `list_yandex_models` в tools-reference
- Обновлены примеры с указанием версий

### 1.1.0 (2026-01-07)
- Поддержка obsidian-kb v1.0.0 (Multi-Provider Production Release)
- Добавлен Core Principle #5: Multi-Provider
- Обновлён `set_provider` — теперь влияет и на enrichment
- Документированы `enrichment_stats` в `get_job_status`
- Добавлены параметры adaptive rate limiting

### 1.0.0 (2026-01-06)
- Initial release
- Поддержка obsidian-kb v0.9.1
- 50+ MCP инструментов документированы
- Паттерны запросов (ID > Name)
- Intent detection описан
- Справочник tools-reference.md

## Совместимость

| aigrep | Skill |
|--------|-------|
| 2.0.x | 1.3.x |
| 1.0.x | 1.1.x |
| 0.9.x | 1.0.x |
| < 0.9 | Не поддерживается |

## Зависимости

- MCP сервер aigrep v2.0+
- SQLite (встроен)
- Ollama с моделью mxbai-embed-large (или Yandex Cloud)

## Файлы

```
aigrep/
├── SKILL.md                    # ~500 слов, ~2 мин чтения
├── _meta.md                    # Этот файл
└── references/
    ├── tools-reference.md      # ~2000 слов, полный справочник v2.0
    ├── query-patterns.md       # 900 слов, паттерны запросов
    └── intent-detection.md     # 600 слов, auto-intent
```

## Использование в промтах

Для vault-specific промтов добавьте секцию:

```markdown
## База знаний

- **Vault:** {vault_name}
- **Skill:** aigrep v1.3.0 (см. SKILL.md)

### Структура папок
{описание структуры}

### Схема ID
{как формируются ID документов}
```
