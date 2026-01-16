# Auto-Intent Detection

Как система автоматически определяет тип запроса и выбирает оптимальную стратегию.

---

## Типы Intent

| Intent | Когда срабатывает | Стратегия | Пример |
|--------|-------------------|-----------|--------|
| **METADATA_FILTER** | Только фильтры в запросе | document-level | `type:person`, `tags:meeting` |
| **KNOWN_ITEM** | ID файла/документа | document-level | `vshadrin`, `smp`, `guide_adr` |
| **SEMANTIC** | Обычный текстовый запрос | chunk-level | `проблемы интеграции` |
| **EXPLORATORY** | Вопросы "что/как/почему" | chunk-level | `что такое интеграция` |
| **PROCEDURAL** | How-to запросы | document-level | `как настроить` |

---

## Document-level vs Chunk-level

### Document-level

**Возвращает целые документы.** Используется когда:
- Нужен конкретный документ (KNOWN_ITEM)
- Фильтрация по метаданным (METADATA_FILTER)
- Процедурные запросы (PROCEDURAL)

**Преимущества:**
- Полный контекст документа
- Корректные связи и frontmatter
- Быстрее для фильтров

### Chunk-level

**Возвращает релевантные фрагменты.** Используется когда:
- Семантический поиск по содержанию (SEMANTIC)
- Исследовательские запросы (EXPLORATORY)

**Преимущества:**
- Точнее находит релевантный контент
- Работает с длинными документами
- Лучше для RAG

---

## Как влияет detail_level

```python
search_vault(vault_name, query, detail_level="auto")
```

| detail_level | Что возвращает |
|--------------|----------------|
| `auto` | Система выбирает на основе intent |
| `full` | Полный контент документов |
| `snippets` | Только snippets (превью) |
| `metadata` | Только метаданные |

**Рекомендация:** Используй `auto` (по умолчанию) — система оптимизирует.

---

## Логика определения Intent

### 1. METADATA_FILTER

Срабатывает когда запрос состоит **только из фильтров**:

```python
"type:person"                    # METADATA_FILTER
"tags:meeting"                   # METADATA_FILTER
"type:1-1 links:vshadrin"       # METADATA_FILTER
"type:person Иван"              # Не только фильтры → SEMANTIC
```

### 2. KNOWN_ITEM

Срабатывает когда запрос похож на **ID документа**:
- Короткий (1-2 слова)
- Без пробелов или с подчёркиванием
- Латиница или транслит

```python
"vshadrin"          # KNOWN_ITEM
"guide_adr"         # KNOWN_ITEM
"smrm-ecosystem"    # KNOWN_ITEM
"Всеволод Шадрин"   # Русский текст → SEMANTIC
```

### 3. PROCEDURAL

Срабатывает на **how-to паттерны**:
- Начинается с "как", "how to"
- Запросы про инструкции, гайды

```python
"как создать ADR"           # PROCEDURAL
"how to configure"          # PROCEDURAL
"инструкция по настройке"   # PROCEDURAL
```

**Ограничение:** Целевой документ может не попасть в топ. Если есть гайд — используй ID напрямую.

### 4. EXPLORATORY

Срабатывает на **вопросительные запросы**:
- Начинается с "что", "какие", "почему", "what", "why"
- Открытые вопросы

```python
"что такое интеграция"          # EXPLORATORY
"какие есть продукты"           # EXPLORATORY
"почему выбрали Python"         # EXPLORATORY
```

### 5. SEMANTIC

**Дефолтный intent** для остальных запросов:

```python
"риски проекта PSB"             # SEMANTIC
"проблемы интеграции"           # SEMANTIC
"архитектура экосистемы"        # SEMANTIC
```

---

## Оптимизация запросов

### Для точного документа

```python
# Может не сработать
search_vault("vault", "профиль Шадрина")

# Гарантированно сработает
search_vault("vault", "vshadrin")
```

### Для списка документов

```python
# Семантический поиск — может пропустить
search_vault("vault", "все люди в команде")

# Точный фильтр
search_vault("vault", "type:person")
```

### Для хронологии

```python
# Фильтр дат работает нестабильно
search_vault("vault", "type:1-1 created:>2024-12-01")

# Специализированный инструмент
timeline("vault", doc_type="1-1", after="2024-12-01")
```

---

## Отладка Intent

Если результаты неожиданные:

1. **Проверь определённый intent:**
   - Много результатов → вероятно SEMANTIC
   - Один документ → вероятно KNOWN_ITEM
   - Документы целиком → document-level

2. **Уточни запрос:**
   - Добавь фильтры для сужения
   - Используй ID если знаешь
   - Переключись на специализированный инструмент

3. **Попробуй явно указать search_type:**
   ```python
   search_vault("vault", query, search_type="fts")    # Полнотекстовый
   search_vault("vault", query, search_type="vector") # Векторный
   search_vault("vault", query, search_type="hybrid") # Гибридный (default)
   ```
