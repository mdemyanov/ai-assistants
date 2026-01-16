# Справочник MCP Tools aigrep v2.0

Полный справочник всех доступных инструментов.

---

## Поиск

### search_vault

**Основной инструмент поиска** в одном vault'е.

```python
search_vault(
    vault_name: str,              # Имя vault'а
    query: str,                   # Запрос + фильтры
    limit: int = 10,              # Максимум результатов
    search_type: str = "hybrid",  # hybrid | vector | fts
    detail_level: str = "auto"    # auto | full | snippets | metadata
)
```

**Примеры:**
```python
search_vault("my-vault", "Python async")
search_vault("my-vault", "type:person")
search_vault("my-vault", "links:vshadrin type:1-1")
search_vault("my-vault", "риски проекта", limit=5, search_type="vector")
```

> **v2.0:** Поиск по свойствам ускорен в 50x благодаря SQLite индексам.

### search_multi_vault

Поиск по **нескольким vault'ам** одновременно.

```python
search_multi_vault(
    vault_names: list[str],  # Список vault'ов
    query: str,              # Запрос
    limit: int = 10
)
```

### search_text

**Текстовый поиск** (ripgrep/grep) без индекса.

```python
search_text(
    vault_name: str,
    query: str,
    case_sensitive: bool = False,
    whole_word: bool = False,
    context_lines: int = 2,
    file_pattern: str = "*.md",
    max_results: int = 100
)
```

**Когда использовать:**
- Точное совпадение текста
- Поиск кода/технических терминов
- Когда семантический поиск не находит

### search_regex

Поиск по **regex паттерну**.

```python
search_regex(
    vault_name: str,
    pattern: str,              # Regex паттерн
    context_lines: int = 2,
    file_pattern: str = "*.md",
    max_results: int = 100
)
```

**Примеры:**
```python
search_regex("vault", r"def\s+\w+\(")      # Определения функций
search_regex("vault", r"TODO|FIXME")        # TODO и FIXME
search_regex("vault", r"\[\[.*?\]\]")       # Все wikilinks
```

### find_files

Поиск **файлов по имени** и/или содержимому.

```python
find_files(
    vault_name: str,
    name_pattern: str,            # Glob паттерн
    content_contains: str = None  # Опционально
)
```

**Примеры:**
```python
find_files("vault", "*.md")
find_files("vault", "**/test*.py", content_contains="async def")
find_files("vault", "README.md")
```

---

## Граф связей

### find_connected

Найти **связанные документы** через wikilinks.

```python
find_connected(
    vault_name: str,
    document_path: str,           # Путь к документу
    direction: str = "both",      # incoming | outgoing | both
    depth: int = 1,               # 1 = прямые, 2 = связи связей
    limit: int = 50
)
```

**Примеры:**
```python
find_connected("vault", "People/Иван.md")
find_connected("vault", "Projects/Alpha.md", "incoming")  # Кто ссылается
find_connected("vault", "Notes/Meeting.md", "outgoing")   # На кого ссылается
```

### get_backlinks

Получить все **входящие ссылки** (аналог панели Backlinks в Obsidian).

```python
get_backlinks(
    vault_name: str,
    document_path: str
)
```

### find_orphans

Найти документы **без входящих ссылок**.

```python
find_orphans(
    vault_name: str,
    doc_type: str = None  # Опционально
)
```

### find_broken_links

Найти **битые wikilinks** — ссылки на несуществующие документы.

```python
find_broken_links(vault_name: str)
```

---

## Dataview-like запросы

### dataview_query

**SQL-подобные запросы** по документам vault'а.

```python
dataview_query(
    vault_name: str,
    query: str = None,           # Полный SQL-like запрос
    select: str = "*",           # Поля
    from_type: str = None,       # Фильтр по типу
    from_path: str = None,       # Фильтр по пути
    where: str = None,           # Условия
    sort_by: str = None,
    sort_order: str = "desc",
    limit: int = 50
)
```

**Примеры:**
```python
# Полный синтаксис
dataview_query("vault", query="SELECT * FROM type:1-1 WHERE status != done SORT BY date DESC")

# Отдельные параметры
dataview_query("vault", from_type="person", where="role = manager", sort_by="name")

# Комбинация
dataview_query("vault", select="title,status", from_path="Projects", where="status = active")
```

> **v2.0:** Запросы по свойствам выполняются через SQLite (~10ms вместо ~500ms).

### get_vault_schema

Получить **схему frontmatter** vault'а — все поля, типы, примеры значений.

```python
get_vault_schema(
    vault_name: str,
    doc_type: str = None,     # Опционально
    top_values: int = 10      # Примеров значений
)
```

**Когда использовать:**
- Понять структуру данных vault'а
- Узнать доступные поля для фильтрации
- Найти возможные значения полей

### list_by_property

Получить документы по **значению свойства frontmatter**.

```python
list_by_property(
    vault_name: str,
    property_key: str,        # status, role, priority...
    property_value: str = None,  # Если None — все с этим полем
    limit: int = 50
)
```

**Примеры:**
```python
list_by_property("vault", "status", "in-progress")
list_by_property("vault", "role")  # Все с полем role
list_by_property("vault", "priority", "high", limit=10)
```

### aggregate_by_property

**Агрегация** — количество документов для каждого значения свойства.

```python
aggregate_by_property(
    vault_name: str,
    property_key: str,
    doc_type: str = None
)
```

**Примеры:**
```python
aggregate_by_property("vault", "status")  # Распределение по статусам
aggregate_by_property("vault", "priority", "task")  # Приоритеты задач
aggregate_by_property("vault", "role", "person")  # Роли людей
```

> **v2.0:** Агрегация выполняется через SQLite (~20ms вместо ~1s).

### get_frontmatter

Получить **frontmatter конкретного файла**.

```python
get_frontmatter(
    vault_name: str,
    file_path: str  # Относительный путь
)
```

---

## Хронология

### timeline

**Хронологическая лента** документов.

```python
timeline(
    vault_name: str,
    doc_type: str = None,
    date_field: str = "created",  # created | modified | кастомное
    after: str = None,            # ISO или "last_week", "last_month"
    before: str = None,
    limit: int = 50
)
```

**Примеры:**
```python
timeline("vault", "meeting", date_field="date", after="2024-12-01")
timeline("vault", after="last_week")
timeline("vault", doc_type="task", date_field="modified")
```

### recent_changes

Документы, **изменённые за N дней**.

```python
recent_changes(
    vault_name: str,
    days: int = 7,
    doc_type: str = None
)
```

---

## Управление vault'ами

### list_vaults

Список **проиндексированных vault'ов** со статистикой.

```python
list_vaults()
```

### vault_stats

**Детальная статистика** vault'а.

```python
vault_stats(vault_name: str)
```

Возвращает: файлы, чанки, размер, теги, даты.

### add_vault_to_config

**Добавить vault** в конфигурацию.

```python
add_vault_to_config(
    vault_path: str,
    vault_name: str = None,    # Если None — имя директории
    auto_index: bool = True    # Автоиндексация
)
```

### check_vault_in_config

Проверить наличие vault в конфигурации.

```python
check_vault_in_config(
    vault_path: str = None,
    vault_name: str = None
)
```

### list_configured_vaults

Список vault'ов **из конфигурации** (не только проиндексированных).

```python
list_configured_vaults()
```

### delete_vault

**Удалить vault** из индекса (файлы не затрагиваются).

```python
delete_vault(vault_name: str)
```

---

## Индексация

### index_documents

**Индексация документов** (инкрементальная или полная).

```python
index_documents(
    vault_name: str,
    paths: list[str] = None,       # None = все изменённые
    force: bool = False,           # Принудительно
    enrichment: str = "contextual", # none | contextual | full
    background: bool = True
)
```

**Примеры:**
```python
index_documents("my-vault")  # Все изменённые
index_documents("my-vault", paths=["file1.md"], force=True)
index_documents("my-vault", enrichment="full", background=False)
```

> **v2.0:** Инкрементальная индексация — только изменённые файлы (~5 сек для 10 файлов).
> Embedding Cache предотвращает повторную векторизацию неизменённых файлов.

### reindex_vault

**Полная переиндексация** (требует подтверждения).

```python
reindex_vault(
    vault_name: str,
    confirm: bool = False,         # Обязательно True!
    enrichment: str = "contextual"
)
```

### index_status

**Статус индексации**.

```python
index_status(
    vault_name: str = None,
    job_id: str = None
)
```

### get_job_status

**Статус фоновых задач**.

```python
get_job_status(
    job_id: str = None,
    vault_name: str = None
)
```

Ответ включает `enrichment_stats`:
- `total_chunks` — всего чанков
- `enriched_ok` — успешно обогащено
- `enriched_fallback` — обогащено с fallback
- `errors` — список ошибок

### cancel_job

**Отменить фоновую задачу** (graceful shutdown).

```python
cancel_job(job_id: str)
```

- Pending задачи — немедленная отмена
- Running задачи — завершает текущий документ и останавливается
- Частично проиндексированные данные сохраняются

### preview_chunks

**Превью разбиения** документа на чанки (без сохранения).

```python
preview_chunks(
    vault_name: str,
    file_path: str,
    strategy: str = "auto"  # auto | headers | semantic | fixed
)
```

### enrich_document

**Обогащение** конкретного документа.

```python
enrich_document(
    vault_name: str,
    file_path: str,
    enrichment_type: str = "all"  # context | summary | all
)
```

---

## Провайдеры LLM

### list_providers

Список **доступных провайдеров** (Ollama, Yandex).

```python
list_providers()
```

### list_yandex_models

Список **доступных моделей Yandex Cloud**.

```python
list_yandex_models()
```

Возвращает таблицу с моделями:
- **YandexGPT** (gRPC SDK): `yandexgpt/latest`, `yandexgpt-lite`, `aliceai-llm`
- **Open Source** (OpenAI HTTP): `qwen3-235b-a22b-fp8/latest`, `gpt-oss-120b/latest`, `gemma-3-27b-it/latest`

**Алиасы:** `qwen` → `qwen3-235b-a22b-fp8/latest`, `gemma` → `gemma-3-27b-it/latest`

### set_provider

**Переключить провайдер**.

```python
set_provider(
    provider_name: str,           # ollama | yandex
    provider_type: str,           # embedding | chat | enrichment | both
    vault_name: str = None,       # None = глобально
    model: str = None
)
```

> `provider_type="both"` включает embedding, chat **и enrichment**.

**Примеры:**
```python
set_provider("yandex", "embedding")  # Глобально Yandex для embedding
set_provider("yandex", "chat", model="qwen")  # Qwen для chat
set_provider("ollama", "enrichment")  # Ollama только для enrichment
```

### test_provider

**Тестирование провайдера**.

```python
test_provider(provider_name: str)
```

### provider_health

**Проверка здоровья** всех провайдеров.

```python
provider_health()
```

### estimate_cost

**Оценка стоимости** операции.

```python
estimate_cost(
    vault_name: str,
    operation: str = "reindex",    # reindex | index_new | enrich
    enrichment: str = "contextual"
)
```

---

## Adaptive Rate Limiting

Провайдеры поддерживают **адаптивный rate limiting**:

- При 429 ошибке: RPS уменьшается в 2 раза
- После N успешных запросов: RPS увеличивается на 10%
- Настраиваемые `min_rps`, `max_rps`, `recovery_threshold`

Работает автоматически для Yandex Cloud провайдеров.

---

## Анализ качества

### index_coverage

**Анализ покрытия** индекса.

```python
index_coverage(vault_name: str)
```

### test_retrieval

**Тестирование качества** retrieval.

```python
test_retrieval(
    vault_name: str,
    queries: list[str],
    expected_docs: list[str] = None
)
```

### audit_index

**Аудит качества** индекса.

```python
audit_index(vault_name: str)
```

### cost_report

**Отчёт о затратах** на LLM.

```python
cost_report(
    vault_name: str = None,
    period: str = "month"  # day | week | month | all
)
```

### performance_report

**Отчёт о производительности**.

```python
performance_report(vault_name: str = None)
```

---

## Вспомогательные

### list_tags

Список **тегов** в vault'е.

```python
list_tags(vault_name: str, limit: int = 100)
```

### list_doc_types

Список **типов документов**.

```python
list_doc_types(vault_name: str)
```

### list_links

Список **wikilinks**.

```python
list_links(vault_name: str, limit: int = 100)
```

### search_help

**Справка по синтаксису** поиска.

```python
search_help()
```

### system_health

**Диагностика системы**.

```python
system_health()
```

### get_metrics

**Метрики использования**.

```python
get_metrics(
    days: int = 7,
    limit: int = 10,
    vault_name: str = None
)
```

---

## Batch операции

### export_to_csv

**Экспорт** данных vault'а в CSV.

```python
export_to_csv(
    vault_name: str,
    output_path: str = None,
    doc_type: str = None,
    fields: str = None,       # Через запятую
    where: str = None
)
```

### compare_schemas

**Сравнение схем** нескольких vault'ов.

```python
compare_schemas(vault_names: list[str])
```

---

## Архитектура v2.0

### Hybrid Storage

**SQLite** (быстрые запросы по метаданным):
- `vaults` — список vault'ов
- `documents` — документы с content hash
- `document_properties` — нормализованные свойства frontmatter
- `embedding_cache` — кэш embeddings

**LanceDB** (векторный поиск):
- `chunks` — чанки с embeddings
- Поддержка hybrid search (vector + FTS)

### Dual-Write

При индексации данные записываются параллельно в SQLite и LanceDB:
- Документы и метаданные синхронизируются
- Удаление также синхронизировано
- Ошибки SQLite не блокируют операции (graceful degradation)

### Incremental Indexing

1. **ChangeDetector** определяет изменения по content hash
2. **FileWatcher** мониторит vault в реальном времени
3. **Embedding Cache** предотвращает повторную векторизацию
4. Только изменённые файлы обрабатываются

### Дедупликация задач

- Одинаковые pending задачи объединяются автоматически
- `debounce_seconds=10` — задержка перед запуском
- `polling_interval=300` — проверка изменений каждые 5 минут
