# Changelog

## 1.0.0 — 2026-04-19

Первая версия плагина. Замещает монолитный `skills/gramax/` (архивирован в `archive/gramax-v1.0.0/`).

### Skills
- `writer` — расширенный writer с поддержкой drawio, staging, структурных правил
- `comments-read` — операционный workflow чтения комментариев
- `comments-write` — операционный workflow add/reply/edit/delete

### Scripts
- `drawio_convert.py` — конвертация `.drawio` → SVG с правильной обработкой кириллицы
- `slugify.py` — транслит кириллицы → latin-slug
- `validate_structure.py` — валидация каталога Gramax (с `--fix --yes`)
- `parse_comments.py` — парсинг комментариев (JSON/report, фильтры)
- `gen_comment_id.py` — генерация 5-символьных ID с проверкой уникальности
- `validate_comments.py` — парность md↔yaml, обязательные поля

### Контент (новое по сравнению с `skills/gramax/`)
- Запрет `_index.md` в корне каталога
- Markdown-admonitions (`:::info`, `:::tip`)
- Block-комментарии `[comment:id]...[/comment]`
- Расширенные таблицы `{% table %}`
- Стилизация (`<color>`, `<highlight>`)
- Формулы (inline/block/legacy)
- Типы note: `warning`, `danger`, `note`
- Staging-checklist (удаление `.DS_Store`, `CLAUDE.md`, сохранение `.gramax/`)
