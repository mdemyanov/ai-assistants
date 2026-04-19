# Миграция: skills/gramax → plugins/gramax/

Этот skill был заменён Claude Code плагином `gramax` в `plugins/gramax/` на 2026-04-19.

## Где найти новое

### Skills

| Было (skills/gramax/) | Стало |
|-----------------------|-------|
| Общий skill `gramax` | 3 фокусированных skill-а в плагине `gramax` |
| Создание/редактирование документов | `/gramax:writer` — `plugins/gramax/skills/writer/SKILL.md` |
| Чтение комментариев (не было отдельно) | `/gramax:comments-read` — `plugins/gramax/skills/comments-read/SKILL.md` |
| Запись комментариев (не было отдельно) | `/gramax:comments-write` — `plugins/gramax/skills/comments-write/SKILL.md` |

### References

| Было (references/blocks.md) | Стало |
|------------------------------|-------|
| Один blocks.md | 4 reference в `plugins/gramax/skills/writer/references/`: |
|  | — `blocks.md` (полный справочник блоков) |
|  | — `drawio.md` (конвертация `.drawio` → SVG) |
|  | — `structure.md` (операции со структурой) |
|  | — `staging.md` (pre-publish чеклист) |

### Скрипты (новое)

- `plugins/gramax/scripts/drawio_convert.py` — конвертация `.drawio` → SVG с правильной обработкой кириллицы
- `plugins/gramax/scripts/slugify.py` — транслит для имён файлов
- `plugins/gramax/scripts/validate_structure.py` — staging-валидация (с `--fix --yes`)
- `plugins/gramax/scripts/parse_comments.py` — парсер комментариев (JSON/report/summary, фильтры)
- `plugins/gramax/scripts/gen_comment_id.py` — генерация ID с проверкой уникальности
- `plugins/gramax/scripts/validate_comments.py` — парность `<comment>` ↔ yaml

## Установка плагина

```
/plugin marketplace add mdemyanov/ai-assistants
/plugin install gramax@ai-assistants
```

После установки доступны `/gramax:writer`, `/gramax:comments-read`, `/gramax:comments-write`.

## Почему разделили

- Операции с комментариями требуют отдельного workflow (превью, генерация ID, валидация) — это плохо смешивается со справочным skill-ом
- Skill для writer оставался компактным (≤500 строк SKILL.md + 4 references), операции read/write комментариев получили свои focused skill-ы
- Добавлены новые технические детали (drawio-конвертация с кириллицей, staging-чеклист, запрет `_index.md` в корне)
