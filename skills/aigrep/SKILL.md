---
name: aigrep
description: Работа с локальными базами знаний Obsidian через MCP. Используй при любых запросах к vault'ам — поиск, индексация, анализ связей, dataview-запросы, timeline. Триггеры — "найди в заметках", "поиск в vault", "что я писал о...", "кто ссылается на...", "покажи недавние изменения", "связанные документы".
---

# aigrep — Работа с базами знаний

AI-powered semantic search для Obsidian vault'ов через MCP. **Версия:** 2.0.9

## Core Principles

1. **ID > Name** — Поиск по ID документа (vshadrin, psb) работает точнее, чем по имени (Всеволод Шадрин)
2. **Фильтры > Семантика** — Для списков используй `type:`, `tags:`, `links:` вместо семантического поиска
3. **Auto-intent** — Система автоматически выбирает стратегию (document-level vs chunk-level)
4. **Vault из контекста** — Имя vault'а берётся из системного промта или через `list_vaults()`
5. **Multi-Provider** — Embedding, chat и enrichment работают через Ollama или Yandex Cloud
6. **Hybrid Storage** — SQLite для метаданных + LanceDB для векторов = быстрый поиск по свойствам

## Быстрый выбор инструмента

| Задача | Инструмент |
|--------|------------|
| Поиск по теме/содержанию | `search_vault` |
| Найти конкретный документ | `search_vault` с ID |
| Все документы типа | `search_vault` с `type:X` |
| Документы за период | `timeline` или `recent_changes` |
| Кто ссылается на документ | `get_backlinks` или `find_connected` |
| Структура данных vault | `get_vault_schema` |
| Статистика по полю | `aggregate_by_property` |
| SQL-подобный запрос | `dataview_query` |
| Текстовый grep | `search_text` или `search_regex` |
| Экспорт данных | `export_to_csv` |

## Формирование запросов

### Фильтры (в строке query)

```
type:person           # По типу документа
tags:meeting          # По тегу
links:vshadrin        # Документы, ссылающиеся на vshadrin
created:>2024-01-01   # По дате (работает нестабильно)
```

**Комбинации:**
```
type:1-1 links:amuratov           # 1-1 с Муратовым
tags:project OR tags:meeting      # Проекты ИЛИ встречи
type:task NOT tags:done           # Незавершённые задачи
```

### Паттерны запросов

| Цель | Паттерн |
|------|---------|
| Найти человека | `{id}` — `vshadrin`, `amuratov` |
| Найти проект | `{id}` — `psb`, `smrm-ecosystem` |
| Найти гайд | `guide_{topic}` — `guide_adr` |
| Все люди | `type:person` |
| Все 1-1 | `type:1-1` |
| Связи человека | `links:{id}` |
| По теме | Семантический запрос |

> Подробнее: `references/query-patterns.md`

## Workflow: Поиск информации

1. **Определи vault** — из системного промта или `list_vaults()`
2. **Выбери стратегию:**
   - Конкретный документ → ID или `type:` фильтр
   - Тема/содержание → семантический запрос
   - Связи → `find_connected` / `get_backlinks`
   - Хронология → `timeline` / `recent_changes`
3. **Выполни запрос** — `search_vault` или специализированный инструмент
4. **При пустых результатах:**
   - Проверь ID написание
   - Попробуй более широкий запрос
   - Используй `search_text` для точного совпадения

## Workflow: Анализ vault'а

1. `get_vault_schema` — понять структуру полей
2. `aggregate_by_property` — статистика по полю
3. `find_orphans` — документы без связей
4. `find_broken_links` — битые ссылки

## Архитектура v2.0

### Hybrid Storage (SQLite + LanceDB)

- **SQLite** — метаданные, frontmatter, свойства документов, кэш embeddings
- **LanceDB** — векторный поиск, семантический поиск
- **Dual-Write** — данные записываются параллельно в обе БД

### Incremental Indexing

- **FileWatcher** — мониторинг изменений в реальном времени (watchdog)
- **ChangeDetector** — определение изменений по content hash
- **Embedding Cache** — повторная индексация без пересчёта embeddings (≥95% cache hit)

### Производительность v2.0

| Операция | v1.0 | v2.0 |
|----------|------|------|
| Полная индексация (1000 файлов) | ~5 мин | ~2 мин |
| Инкрементальная (10 файлов) | ~5 мин | ~5 сек |
| Поиск по свойству | ~500ms | ~10ms |
| Агрегация по полю | ~1s | ~20ms |

## Индексация

### Автоматическая индексация

С v2.0 изменения отслеживаются автоматически:
- FileWatcher мониторит vault в реальном времени
- Изменённые файлы индексируются с debounce (10 сек)
- Дедупликация задач — одинаковые задачи объединяются

### Ручная индексация

```python
# Инкрементальная — только изменённые файлы
index_documents("vault")

# Принудительная переиндексация файлов
index_documents("vault", paths=["file.md"], force=True)

# Полная переиндексация (требует confirm=True)
reindex_vault("vault", confirm=True)
```

### Статус индексации

```python
# Статус всех задач
get_job_status()

# Статус конкретной задачи (включает enrichment_stats)
get_job_status(job_id="xxx")

# Отмена задачи (graceful shutdown)
cancel_job(job_id="xxx")
```

## Ограничения и известные проблемы

- **Даты** — фильтр `created:>` работает нестабильно, используй `timeline`
- **Имена** — поиск по русским именам ненадёжен, используй ID
- **links:** — фильтр требует полный путь (не `links:vshadrin`, а `links:10_PEOPLE/vshadrin/vshadrin`)
- **test_retrieval** — функция падает с AttributeError в v2.0.9
- **Комбинация фильтров** — `type:X links:Y` может работать некорректно, разделяй на 2 запроса
- **Enrichment** — по умолчанию отключен, указывай `enrichment="contextual"` при reindex
- **Миграция** — при обновлении с v1.x требуется полная переиндексация

> Подробнее: `references/known-issues.md`

## CLI команды (для Claude Code)

При работе в Claude Code (с доступом к Bash) некоторые операции удобнее через CLI.

> **Путь:** CLI требует `uv run aigrep` из директории проекта или глобальной установки.

### Диагностика

```bash
uv run aigrep doctor                    # Полная проверка системы
uv run aigrep doctor --check ollama     # Только Ollama
uv run aigrep doctor --json             # JSON для парсинга
```

### Фоновые процессы (CLI only)

```bash
uv run aigrep watch --vault "X"         # Автообновление при изменениях
uv run aigrep install-service           # Установить автозапуск (macOS)
uv run aigrep service-status            # Статус сервиса
```

### Тонкая настройка индексации

```bash
uv run aigrep reindex --vault "X" --max-workers 4 --no-enrichment
uv run aigrep index --vault "X" --path "/path" --enrichment-strategy fast
```

### Кластеризация (CLI only)

```bash
uv run aigrep cluster --vault "X"       # Группировка похожих документов
```

### Конфигурация

```bash
uv run aigrep config show               # Текущая конфигурация
uv run aigrep config add-vault --name "X" --path "/path"
uv run aigrep claude-config --apply     # Применить конфиг для Claude Desktop
```

### CLI vs MCP: когда что использовать

| Задача | Рекомендация |
|--------|--------------|
| Поиск, граф связей, dataview | **MCP** — богаче API |
| Диагностика, watch, сервисы | **CLI** — больше контроля |
| Переиндексация с параметрами | **CLI** — max-workers, clustering |
| Управление провайдерами | **MCP** — удобнее в контексте агента |

## Resources

- `references/tools-reference.md` — полный справочник 50+ инструментов
- `references/query-patterns.md` — детальные паттерны запросов
- `references/intent-detection.md` — как работает auto-intent
- `references/known-issues.md` — известные проблемы и workarounds
