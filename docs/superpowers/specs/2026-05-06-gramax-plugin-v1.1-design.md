---
title: Gramax Plugin v1.1 — Schema Alignment & Validation
date: 2026-05-06
status: design
related:
  - source: /Users/mdemyanov/Devel/pg_vector_service/docs/gramax-skills-update.md
  - adr: pg_vector_service/content/00-project/adr/028-gramax-schema-alignment-v2.md
---

# Gramax Plugin v1.1 — Schema Alignment & Validation

## Контекст

При работе с проектом `pg_vector_service` (89 файлов, 75 статей) выявились пробелы в текущем `gramax@ai-assistants` плагине: writer SKILL не описывает корректный формат `properties` (object vs flat), не упоминает обязательность `_index.md` в подпапках, не содержит справочника по `.doc-root.yaml` схеме (палитра `style:`, иконки, ключи). После сверки с production-эталоном `naumen-ecosystem/business-requirements/` зафиксированы 9 необходимых изменений (см. источник в `related:`). Текущий релиз — `1.0.0` от 2026-04-19.

Цель — обновить плагин до **1.1.0**, закрыв 8 из 9 изменений (P0+P1+точечные P2), и закрепить знание через три слоя (SKILL.md → references/ → validate_structure.py), чтобы новые проекты не повторяли проблемы `pg_vector_service` в первый день работы с каталогом.

## Цели

1. Документация writer-skill отражает реальный поддерживаемый формат frontmatter и каталога Gramax.
2. `validate_structure.py` ловит блокирующие ошибки структуры до пуша.
3. Подпапка без `_index.md` и битые ссылки на схему фиксируются как `error`.
4. Legacy-форматы (плоская нотация frontmatter) фиксируются как `warning`, не ломая существующие каталоги.
5. SKILL.md остаётся ≤ 500 строк (фактически — ~315 после правок).

## Не-цели

- Реализация CLI `--migrate-frontmatter` для миграции legacy-каталогов (отдельный спек, когда возникнет конкретный кандидат).
- Изменения в `comments-read` / `comments-write` skills.
- Полноценная pytest-инфраструктура для плагина (только smoke-тест для validate_structure.py).
- Версионный bump до `2.0.0` — изменения backward-compatible.

## Архитектура

```
plugins/gramax/
├── CHANGELOG.md                              [UPDATE: запись 1.1.0]
├── scripts/
│   ├── validate_structure.py                 [UPDATE: 5 новых проверок]
│   └── tests/
│       └── test_validate_structure.py        [NEW: smoke-тест]
└── skills/writer/
    ├── SKILL.md                              [UPDATE: 6 секций]
    └── references/
        ├── blocks.md                         [UPDATE: расширенный <view>]
        ├── doc-root-schema.md                [NEW: полный справочник]
        ├── structure.md                      [UPDATE: правила _index.md]
        ├── drawio.md                         [unchanged]
        └── staging.md                        [unchanged]
```

**Принцип трёх слоёв:** одно правило закрепляется минимум в двух местах — описание в skill (SKILL.md или references/) и автоматическая проверка в validator. Validator важнее: если агент пропустит правило в инструкции, валидатор поймает перед публикацией.

## Изменения по файлам

### 1. `skills/writer/SKILL.md`

| Секция | Изменение | Объём |
|--------|-----------|-------|
| Frontmatter (строки 85–99) | Разделить на «Статья» (object-нотация) и «`_index.md`» (без properties). Антипаттерн плоской нотации с `LEGACY` маркером. | +30 строк |
| Структура каталога (строки 43–83) | Правило: каждая подпапка с `.md` обязана иметь `_index.md`. Минимальный шаблон. | +20 строк |
| `.doc-root.yaml` — кратко (новая, после Frontmatter) | 4–5 ключевых фактов: object-нотация properties, `style:`/`icon:` валидны на property, `filterProperties` для боковой панели, ссылка на полный справочник. Один компактный пример. | +25 строк |
| Краткий справочник блоков (строки 169–185) | Расширить строку про `<view>`: атрибуты `defs`, `groupby`, `display`. Один пример. Подробности → `references/blocks.md`. | +10 строк |
| Ссылки (строки 125–130) | Cross-каталожные ссылки: только inline code, не markdown link. | +5 строк |
| Production эталоны (новая секция в конце) | Канонический референс — `naumen-ecosystem/business-requirements/`. Один абзац. | +8 строк |

Итог: 218 → ~315 строк.

### 2. `skills/writer/references/structure.md`

- Раздел «Правила корня каталога» (строки 92–116) → переименовать в «Правила `_index.md`».
- Параграф «Подпапки — `_index.md` обязателен»: таблица по типам подпапок (коллекция / статья с подстатьями / узел иерархии) + шаблоны.
- Сравнительная таблица «корень vs подпапка».
- ~+45 строк.

### 3. `skills/writer/references/blocks.md`

- Расширенный раздел «Дашборды через `<view>`»: атрибуты, синтаксис фильтров (`defs="X=A&B&none"`), группировка, примеры из эталона `business-requirements/_index.md`.
- Когда использовать (>20 статей в разделе) / когда не (<10 статей).
- ~+30 строк.

### 4. `skills/writer/references/doc-root-schema.md` — NEW

Полный справочник конфигурации каталога:

- **Корневые ключи**: `title`, `description`, `code` (опц.), `style`, `language`, `supportedLanguages`, `syntax`, `properties`, `filterProperties`, `editors`.
- **Property-определение**: `name`, `type: Enum|String`, `style`, `icon`, `values`. `required:` — явно помечен как «не используется в эталонах».
- **Палитра `style:`** (11 значений): `gray`, `green`, `light-green`, `blue`, `light-blue`, `blue-green`, `purple`, `light-purple`, `orange`, `dark-orange`, `light-pink`. Семантика по аналогии с эталоном (categorical / lifecycle / priority / metadata).
- **Иконки**: набор Lucide (`https://lucide.dev/icons`). Часто используемые из эталона.
- **Полный пример** из `pg_vector_service/.doc-root.yaml` (упрощённая версия).
- **Антипаттерны**: `required:` (не приживается), `type: select` с `values: [{name: X}]` (экспериментальный, не в production).

~120 строк.

### 5. `scripts/validate_structure.py`

Добавить 5 проверок:

| ID | Проверка | Уровень | Сообщение |
|----|----------|---------|-----------|
| **V1** | Каждая подпапка с `.md` или подпапками содержит `_index.md` | error | `<dir>/: missing _index.md (Gramax не покажет раздел в навигации)` |
| **V2** | `_index.md` подпапки не содержит блок `properties:` в frontmatter | error | `<file>: _index.md не должен содержать properties:` |
| **V3** | Frontmatter статей — object-нотация (`- name: X / value: [Y]`), не плоская (`- X: Y`) | warning | `<file>: устаревшая плоская нотация properties; см. SKILL.md → Frontmatter` |
| **V4** | `properties.name` ссылаются на имена, объявленные в `.doc-root.yaml` | error | `<file>: property "<X>" не объявлен в .doc-root.yaml` |
| **V5** | Значения property входят в `values:` соответствующего `Enum` | error | `<file>: property "<X>" имеет значение "<Y>", не входит в [<list>]` |

**Дифференциация уровней:** V1, V2 = функциональные блокеры рендера → error; V3 = legacy-стиль (рендерится, просто непредсказуемо) → warning; V4, V5 = битые ссылки на схему → error.

**Дополнительно:** в `check_doc_root` сделать `code` опциональным (эталон `business-requirements/.doc-root.yaml` его не имеет — текущий валидатор противоречит эталону).

**Реализация:**

- `load_property_schema(root)` — парсит `.doc-root.yaml` один раз, возвращает `{property_name: {type, values}}`. Кэш для V4/V5.
- V1: после `rglob("*.md")` собрать множество папок с `.md` или вложенными папками; для каждой кроме корня и `.gramax/*` проверить наличие `_index.md`.
- V2: в `check_frontmatter` различать по `md_file.name == "_index.md"`. Если индекс — `properties` запрещены.
- V3: если `fm["properties"]` существует и хоть один элемент — словарь без ключей `name`/`value` → warning.
- V4/V5: для object-нотации сверка с кэшем схемы.

**Edge case:** если `.doc-root.yaml` использует экспериментальный `type: select` с `values: [{name: X}]` (как `naumen-smp-mcp`), V4/V5 пропускаются с однократным warning «schema использует экспериментальный формат values, проверки V4/V5 пропущены».

**CLI:** без новых флагов. `--strict` и `--fix --yes` работают как раньше.

### 6. `scripts/tests/test_validate_structure.py` — NEW

Smoke-тест без внешних зависимостей (stdlib `unittest`):

- Фикстура `good/` — валидный каталог: `.doc-root.yaml` с двумя property, корректный frontmatter (object-нотация), `_index.md` в подпапке.
- Фикстура `bad/` — каталог со всеми 5 нарушениями.
- Тесты: `good` → exit 0, без сообщений; `bad` → exit 1, в выводе ключевые слова всех 5 проверок.

Запуск: `python3 -m unittest plugins/gramax/scripts/tests/test_validate_structure.py`. Если pytest установлен — также подберёт.

### 7. `CHANGELOG.md`

Запись `1.1.0 — 2026-05-06`, секции:
- **Документация writer-skill**: новая object-нотация frontmatter, правила `_index.md` в подпапках, новый `doc-root-schema.md`, расширенный `<view>`, cross-каталожные ссылки, эталоны.
- **Валидация**: 5 новых проверок (V1–V5), `code` в `.doc-root.yaml` опционально.
- **Эталоны**: явный canonical reference на `naumen-ecosystem/business-requirements/`.

## Порядок коммитов

Атомарные коммиты в одном PR, по семантическим единицам:

1. `docs(gramax/writer): add frontmatter object-нотацию + _index.md правила`
2. `docs(gramax/writer): add doc-root-schema reference`
3. `docs(gramax/writer): expand <view>, cross-каталог ссылки, production эталоны`
4. `docs(gramax/writer): refine structure.md (subfolder rules)`
5. `feat(gramax/scripts): validate_structure V1–V5 + code optional`
6. `test(gramax/scripts): smoke test for validate_structure`
7. `chore(gramax): release 1.1.0 (CHANGELOG)`

**Тегирование релиза:** версия плагина авторитетно фиксируется в `plugins/gramax/CHANGELOG.md`. Решение о git-теге (`v1.1.0` / `v1.1.0-gramax` / без тега) остаётся на этап реализации — нужно проверить текущую конвенцию через `git tag -l` перед пушем. CI/CD проекта (`.github/workflows/release.yml`) реагирует на тег `v*` — рекомендуется не дёргать его без подтверждения, если этот плагин не должен триггерить общий релиз skills.

## Риски

- **V4/V5 ложные срабатывания** на экспериментальной схеме `type: select`. Митигация: skip с однократным warning.
- **V3 шум на legacy-каталогах** (`sd-ai-assistant`). Митигация: warning, не error; пользователь может игнорировать или мигрировать.
- **Объём SKILL.md**: после правок ~315 строк, в пределах лимита 500. Если в будущем потребуются доп. секции — выносить в references/.
- **Эталон может эволюционировать**: ссылка на абсолютный путь `naumen-ecosystem/business-requirements/` хрупка для других машин. Митигация: ссылка как иллюстрация плюс краткий пример embedded в `doc-root-schema.md`, чтобы skill оставался самодостаточным.

## Out of scope

- `--migrate-frontmatter` CLI (#9 из findings) — отдельный спек.
- Доработка `comments-read`/`comments-write` skills.
- Полноценная pytest-инфра.
- Версионный мажор `2.0.0`.

## Критерии приёмки

1. Все 8 изменений документации/валидации применены.
2. `validate_structure.py` на эталоне `business-requirements/` (если есть локально) — exit 0 без warnings/errors.
3. `validate_structure.py` на тест-фикстуре `bad/` — exit 1, все 5 проверок репортятся.
4. SKILL.md ≤ 500 строк.
5. CHANGELOG.md содержит запись 1.1.0.
6. Smoke-тест проходит: `python3 -m unittest plugins/gramax/scripts/tests/test_validate_structure.py`.
