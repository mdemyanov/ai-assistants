# Паттерны формирования запросов

Детальное руководство по эффективным запросам к aigrep.

---

## Золотое правило: ID > Name

Система оптимизирована для поиска по **идентификаторам документов**. Поиск по русским именам работает нестабильно из-за особенностей embedding модели.

| Не работает надёжно | Работает всегда |
|---------------------|-----------------|
| Всеволод Шадрин | vshadrin |
| Алексей Муратов | amuratov |
| проект Промсвязьбанк | psb |
| экосистема SMRM | smrm-ecosystem |

### Схема формирования ID

**Люди:** первая буква имени + фамилия (транслит)
- Всеволод Шадрин → `vshadrin`
- Ольга Габдрашитова → `ogabdrashitova`

**Проекты/продукты:** короткое англоязычное имя
- Проект ПСБ → `psb`
- Экосистема SMRM → `smrm-ecosystem`

---

## Фильтры в строке запроса

### type: — По типу документа

```python
search_vault("vault", "type:person")      # Все профили людей
search_vault("vault", "type:1-1")         # Все встречи 1-1
search_vault("vault", "type:project")     # Все проекты
search_vault("vault", "type:adr")         # Все ADR
search_vault("vault", "type:meeting")     # Все протоколы встреч
```

**Как узнать доступные типы:**
```python
list_doc_types("vault")
# или
get_vault_schema("vault")
```

### tags: — По тегам

```python
search_vault("vault", "tags:python")
search_vault("vault", "tags:meeting")
search_vault("vault", "tags:urgent")
```

**Не используй #:** `#python` → используй `tags:python`

**Как узнать доступные теги:**
```python
list_tags("vault")
```

### links: — По связям (wikilinks)

Находит документы, которые **ссылаются на указанный**.

```python
search_vault("vault", "links:vshadrin")         # Документы про Шадрина
search_vault("vault", "links:smrm-ecosystem")   # Документы по экосистеме
search_vault("vault", "links:psb")              # Упоминания PSB
```

**Альтернатива для входящих ссылок:**
```python
get_backlinks("vault", "07_PEOPLE/vshadrin/vshadrin.md")
```

### created: / modified: — По датам (нестабильно)

```python
search_vault("vault", "created:>2024-01-01")
search_vault("vault", "modified:<2024-12-31")
```

**Ограничение:** Фильтры по датам работают нестабильно. Рекомендуется использовать:

```python
# Вместо created:>2024-12-20 type:1-1
timeline("vault", doc_type="1-1", after="2024-12-20")

# Вместо modified:>last_week
recent_changes("vault", days=7)
```

---

## Логические операторы

### OR — Один из вариантов

```python
search_vault("vault", "tags:meeting OR tags:1-1")
search_vault("vault", "type:project OR type:initiative")
```

### NOT — Исключение

```python
search_vault("vault", "type:task NOT tags:done")
search_vault("vault", "type:person NOT tags:archived")
```

### Комбинации

```python
search_vault("vault", "type:1-1 links:amuratov created:>2024-12-01")
search_vault("vault", "Python tags:async links:flask-app")
```

---

## Выбор стратегии по типу задачи

### Найти конкретный документ/человека

**Используй ID:**
```python
search_vault("vault", "vshadrin")           # Профиль
search_vault("vault", "psb")                # Проект
search_vault("vault", "guide_adr")          # Гайд
```

### Получить список документов типа

**Используй type: фильтр:**
```python
search_vault("vault", "type:person")
search_vault("vault", "type:1-1")
search_vault("vault", "type:project")
```

### Найти связанные документы

**Используй links: или специализированные инструменты:**
```python
search_vault("vault", "links:vshadrin")

# Или более детально:
find_connected("vault", "07_PEOPLE/vshadrin/vshadrin.md", direction="incoming")
get_backlinks("vault", "07_PEOPLE/vshadrin/vshadrin.md")
```

### Поиск по теме/содержанию

**Семантический запрос:**
```python
search_vault("vault", "риски проекта PSB")
search_vault("vault", "проблемы интеграции продуктов")
search_vault("vault", "архитектура экосистемы")
```

### Поиск по хронологии

**Используй timeline/recent_changes:**
```python
timeline("vault", doc_type="meeting", after="2024-12-01")
recent_changes("vault", days=7)
timeline("vault", after="last_week")
```

### Точное текстовое совпадение

**Используй search_text/search_regex:**
```python
search_text("vault", "TODO")
search_text("vault", "async def", file_pattern="*.py")
search_regex("vault", r"def\s+\w+\(")
```

---

## How-to запросы

Запросы типа "как сделать X" определяют intent корректно, но целевой документ может не попасть в топ результатов.

| Может не найти | Найдёт точно |
|----------------|--------------|
| как создать ADR | `guide_adr` |
| как вести 1-1 | `guide_1-1` |
| как оформить проект | `guide_projects` |

**Решение:** Если есть гайд — используй ID гайда напрямую.

---

## Dataview-подобные запросы

Для сложной фильтрации используй `dataview_query`:

```python
# Все 1-1 не завершённые, сортировка по дате
dataview_query("vault", query="SELECT * FROM type:1-1 WHERE status != done SORT BY date DESC")

# Люди с ролью manager
dataview_query("vault", from_type="person", where="role = manager", sort_by="name")

# Проекты со статусом active
dataview_query("vault", select="title,status", from_type="project", where="status = active")
```

---

## Алгоритм выбора стратегии

```
┌─────────────────────────────────────┐
│ Что ищешь?                          │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Конкретный документ/человек?        │
│ → Используй ID                      │
│   vshadrin, psb, guide_adr          │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Список документов типа?             │
│ → Используй type:                   │
│   type:person, type:1-1             │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Документы за период?                │
│ → Используй timeline                │
│   timeline("vault", after="...")    │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Связанные документы?                │
│ → Используй links: или find_connected│
│   links:vshadrin                    │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Структура/статистика?               │
│ → Используй schema/aggregate        │
│   get_vault_schema, aggregate_by... │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Поиск по теме/содержанию?           │
│ → Семантический запрос              │
│   риски проекта, архитектура        │
└─────────────────────────────────────┘
```

---

## Отладка пустых результатов

1. **Проверь написание ID** — опечатки частая причина
2. **Попробуй более широкий запрос** — убери фильтры
3. **Проверь индексацию** — `vault_stats("vault")`
4. **Используй search_text** — для точного совпадения
5. **Проверь тип документа** — `list_doc_types("vault")`
