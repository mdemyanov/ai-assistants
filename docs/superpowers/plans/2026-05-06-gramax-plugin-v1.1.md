# Gramax Plugin v1.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Закрыть 8 из 9 находок из `pg_vector_service/docs/gramax-skills-update.md` и зарелизить плагин Gramax 1.1.0, защитив будущие проекты от тех же ошибок.

**Architecture:** Трёхслойное закрепление знания: SKILL.md (агент видит при загрузке) + references/ (детали) + validate_structure.py (машинная проверка). Документация ведёт правила, validate_structure ловит нарушения перед публикацией.

**Tech Stack:** Markdown, YAML, Python 3.10+, `uv run`, stdlib `unittest`, `pyyaml`.

**Spec:** [docs/superpowers/specs/2026-05-06-gramax-plugin-v1.1-design.md](../specs/2026-05-06-gramax-plugin-v1.1-design.md)

---

## File Structure

```
plugins/gramax/
├── CHANGELOG.md                              [MODIFY]
├── scripts/
│   ├── validate_structure.py                 [MODIFY]
│   └── tests/
│       ├── __init__.py                       [CREATE]
│       ├── test_validate_structure.py        [CREATE]
│       └── fixtures/
│           ├── good/                         [CREATE]
│           │   ├── .doc-root.yaml
│           │   ├── article.md
│           │   └── section/
│           │       ├── _index.md
│           │       └── child.md
│           └── bad/                          [CREATE]
│               ├── .doc-root.yaml
│               ├── flat-notation.md          (V3)
│               ├── invalid-property.md       (V4)
│               ├── invalid-value.md          (V5)
│               └── orphan-section/           (V1: missing _index.md)
│                   └── child.md
└── skills/writer/
    ├── SKILL.md                              [MODIFY]
    └── references/
        ├── blocks.md                         [MODIFY]
        ├── doc-root-schema.md                [CREATE]
        └── structure.md                      [MODIFY]
```

---

## Task 1: SKILL.md — Frontmatter section (object-нотация + `_index.md` без properties)

**Files:**
- Modify: `plugins/gramax/skills/writer/SKILL.md:85-99`

- [ ] **Step 1: Replace Frontmatter section**

Find the existing block (lines 85-99 starting with `## Frontmatter` and ending with `- \`properties\` — опционально`). Replace it with:

````markdown
## Frontmatter

Каждый `.md` **обязан** начинаться с frontmatter. Формат отличается для статей и `_index.md`.

### Статья (любой `.md`, кроме `_index.md`)

```yaml
---
order: 1
title: "Заголовок статьи"
properties:
  - name: <Имя property из .doc-root.yaml>
    value: [<значение из enum>]
  - name: <следующий property>
    value: [<значение>]
---
```

- `order` — числовой порядок в навигации (целые или десятичные для вставки)
- `title` — заголовок на языке страницы; в кавычках если содержит `:` или начинается с цифры
- `properties` — список объектов `{name, value: [...]}`. **Object-нотация — единственно поддерживаемая для нового контента.** Имя должно совпадать с `name:` property в `.doc-root.yaml`. `value:` всегда массив (поддерживает мульти-select).

### `_index.md` (любая папка кроме корня каталога)

```yaml
---
order: 1
title: Название раздела
---
```

`_index.md` **не должен содержать** блок `properties:` — раздел не имеет собственных property, они определяются на статьях. Для фильтров по разделу — `<view>` блоки в теле (см. ниже).

### Антипаттерн: плоская нотация (LEGACY)

```yaml
properties:
  - Тип контента: ADR
  - Фаза: PoC
```

Встречается в старых каталогах. Gramax парсит, но рендерит непредсказуемо при несовпадении регистра ключей. **Не использовать в новом контенте.** При работе с legacy — мигрировать пакетно.
````

- [ ] **Step 2: Verify SKILL.md still parses (frontmatter intact)**

Run: `python3 -c "import yaml; t=open('plugins/gramax/skills/writer/SKILL.md').read(); end=t.find('\n---', 3); print(yaml.safe_load(t[3:end]))"`

Expected: dict with `name: writer` and `description:` printed.

- [ ] **Step 3: Verify line count**

Run: `wc -l plugins/gramax/skills/writer/SKILL.md`

Expected: ~245 lines (was 218, +27 from this task).

---

## Task 2: SKILL.md — Add subfolder `_index.md` rule in Структура каталога

**Files:**
- Modify: `plugins/gramax/skills/writer/SKILL.md` (Структура каталога section, after line "Корень каталога (где `.doc-root.yaml`) НЕ должен содержать `_index.md`.")

- [ ] **Step 1: Add new bullet + paragraph after the existing "Корень каталога" rule**

Find the line:
```
- **Корень каталога (где `.doc-root.yaml`) НЕ должен содержать `_index.md`.**
```

Insert immediately after it:
````markdown
- **Каждая подпапка с `.md`-файлами или вложенными папками ОБЯЗАНА содержать `_index.md`.** Без него Gramax не строит навигацию — папка не видна в дереве, статьи внутри недоступны.

Минимальный шаблон `_index.md` для подпапки-коллекции:

```yaml
---
order: <число>
title: <Название раздела>
---

<Одно-два предложения, что здесь хранится.>

| Файл | Описание |
|------|----------|
| [Название](файл.md) | Краткое описание |
```
````

- [ ] **Step 2: Verify line count**

Run: `wc -l plugins/gramax/skills/writer/SKILL.md`

Expected: ~265 lines (+18 from this task).

- [ ] **Step 3: Commit Tasks 1 and 2**

```bash
git add plugins/gramax/skills/writer/SKILL.md
git commit -m "$(cat <<'EOF'
docs(gramax/writer): add object-нотацию frontmatter и правило _index.md в подпапках

Закрывает блокеры рендера #1, #2 из gramax-skills-update.md:
- Frontmatter теперь явно разделён на статьи (object properties) и _index.md (без properties)
- Антипаттерн плоской нотации помечен как LEGACY
- Подпапки обязаны иметь _index.md (без него навигация Gramax ломается)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: structure.md — Renaming + subfolder rules

**Files:**
- Modify: `plugins/gramax/skills/writer/references/structure.md:92-116`

- [ ] **Step 1: Replace section "Правила корня каталога" with expanded "Правила `_index.md`"**

Find the section starting with `## Правила корня каталога` (line 92) and ending before `## Примеры структур` (line 118). Replace the entire section with:

````markdown
## Правила `_index.md`

### Корень каталога — `_index.md` запрещён

На уровне корня каталога (где лежит `.doc-root.yaml`) `_index.md` **НЕ должно быть**. Статьи размещаются как:
- `leaf.md` — листовая статья
- `section/` — директория со своей `_index.md` и дочерними

**Правильно:**
```
catalog/
├── .doc-root.yaml
├── simple-page.md
└── main-section/
    ├── _index.md
    ├── child-1.md
    └── child-2.md
```

**Неправильно:**
```
catalog/
├── .doc-root.yaml
├── _index.md          ← НЕТ!
├── child-1.md
└── child-2.md
```

### Подпапки — `_index.md` обязателен

В **любой** подпапке каталога (содержащей `.md` файлы или вложенные папки) `_index.md` обязателен. Без него Gramax не строит навигацию — папка не видна в дереве, статьи внутри недоступны.

**Сценарии:**

| Тип подпапки | Шаблон `_index.md` |
|--------------|--------------------|
| Коллекция однотипных статей (`adr/`, `runbooks/`) | `order` + `title` + описание + таблица файлов |
| Статья с подстатьями (`api-reference/`) | `order` + `title` + контент-как-у-обычной-статьи |
| Узел иерархии без своего контента | `order` + `title` + `<view>` для генерации списка |

`_index.md` подпапки **никогда** не содержит `properties:` — раздел не является сущностью с типом/статусом, эти атрибуты живут на статьях.

### Сравнение: корень vs подпапка

| | `_index.md` в корне (рядом с `.doc-root.yaml`) | `_index.md` в подпапке |
|-|---|---|
| Обязателен? | ❌ Запрещён | ✅ Обязателен |
| `properties:` | — | Не должен содержать |
| Назначение | — | Титул раздела + навигация |
````

- [ ] **Step 2: Verify file is readable markdown**

Run: `head -1 plugins/gramax/skills/writer/references/structure.md && tail -20 plugins/gramax/skills/writer/references/structure.md`

Expected: starts with `# Операции со структурой Gramax-каталога`, ends with the existing "Примеры структур" section intact.

---

## Task 4: doc-root-schema.md — New reference file

**Files:**
- Create: `plugins/gramax/skills/writer/references/doc-root-schema.md`

- [ ] **Step 1: Create the file with full schema reference**

````markdown
# `.doc-root.yaml` — schema reference

Конфигурация каталога Gramax. Лежит в корне (рядом с `.doc-root.yaml` НЕ должно быть `_index.md`).

## Корневые ключи

| Ключ | Тип | Обязательное | Назначение |
|------|-----|--------------|------------|
| `title` | string | да | Заголовок каталога в Gramax UI |
| `description` | string | да | Описание для каталог-листа |
| `language` | string | да | Основной язык (`ru` / `en`) |
| `syntax` | enum | да | `XML` (активирует `<note>`, `<tabs>`, `<view>`) или `Markdown` |
| `code` | string | нет | Короткий идентификатор каталога (для cross-каталожных ссылок) |
| `style` | string | нет | Цвет заголовка каталога: `blue`, `blue-green`, `green`, `purple` etc. |
| `supportedLanguages` | array | нет | Список поддерживаемых языков; `[]` = без ограничений |
| `properties` | array | нет | Определения property для frontmatter (см. ниже) |
| `filterProperties` | array | нет | Имена property для боковой панели фильтров: `[Тип контента, Фаза]` |
| `editors` | array | нет | Email'ы с правами публикации |

## Property-определение

```yaml
properties:
  - name: <имя property>
    type: <Enum | String>
    style: <цвет бейджа>
    icon: <Lucide-иконка>
    values:
      - <значение 1>
      - <значение 2>
```

| Поле | Обязательное | Назначение |
|------|--------------|------------|
| `name` | да | Имя property; используется в frontmatter статей в `- name: <X>` |
| `type` | да | `Enum` для select из `values:`; `String` для свободного текста |
| `style` | нет | Цвет бейджа в frontmatter и sidebar |
| `icon` | нет | Lucide-иконка рядом с бейджем |
| `values` | для `Enum` | Массив строк — допустимые значения |

## Палитра `style:`

Подтверждённые в production-эталоне `naumen-ecosystem/business-requirements/.doc-root.yaml`:

`gray`, `green`, `light-green`, `blue`, `light-blue`, `blue-green`, `purple`, `light-purple`, `orange`, `dark-orange`, `light-pink`

**Семантика по аналогии с эталоном:**

- **categorical** (что это) — `green`, `light-blue`, `purple`
- **lifecycle** (где в цикле) — `light-green`, `dark-orange`
- **priority / attention** — `orange`, `dark-orange`, `light-pink`
- **metadata** (id, технические поля) — `gray`

## Иконки

Любая иконка из набора Lucide (`https://lucide.dev/icons`). Часто используемые из эталона:

`hash`, `layers`, `package`, `box`, `folder`, `user`, `users`, `zap`, `briefcase`, `link`, `repeat`, `play`, `target`, `circle-check`, `alert-triangle`, `git-branch`, `file-text`, `check-circle`, `user-check`

## Полный пример

```yaml
title: pg_vector_service
description: Knowledge base for pg_vector_service
language: ru
syntax: XML
style: blue
supportedLanguages: []

properties:
  - name: Тип контента
    type: Enum
    style: green
    icon: file-text
    values:
      - Требование
      - Архитектура
      - ADR

  - name: Статус
    type: Enum
    style: dark-orange
    icon: check-circle
    values:
      - Draft
      - Approved
      - Superseded

filterProperties: [Тип контента]
editors:
  - user@example.com
```

## Антипаттерны

### `required:` на property

Не используется в production-эталонах. Все 16 properties в `business-requirements/.doc-root.yaml` без `required:`. Gramax не делает с ним ничего полезного — пропускать.

### `type: select` с `values: [{name: X}]`

Встречается в `naumen-smp-mcp` как эксперимент. **Не приживается в production-каталогах.** Использовать `type: Enum` со строковым массивом `values:`.
````

- [ ] **Step 2: Verify file**

Run: `wc -l plugins/gramax/skills/writer/references/doc-root-schema.md`

Expected: ~110 lines.

---

## Task 5: SKILL.md — Brief `.doc-root.yaml` section + production эталоны

**Files:**
- Modify: `plugins/gramax/skills/writer/SKILL.md` (after Frontmatter section, before Нейминг)

- [ ] **Step 1: Insert new section after Frontmatter**

Find the line `## Нейминг файлов и папок` and insert this section immediately above it:

````markdown
## `.doc-root.yaml` — кратко

Конфигурация каталога. Лежит в корне.

```yaml
title: My catalog
description: Описание для каталог-листа
language: ru
syntax: XML

properties:
  - name: Тип контента
    type: Enum
    style: green
    icon: file-text
    values: [Требование, ADR, Архитектура]

filterProperties: [Тип контента]
```

**Ключевое:**
- `properties` — список **объектов** с `name/type/style/icon/values`. То же `name:` используется в frontmatter статей.
- `style:` — цвет бейджа property (`green`, `blue`, `purple`, etc.). Палитра из 11 значений.
- `icon:` — любая иконка из Lucide (`https://lucide.dev/icons`).
- `filterProperties` — имена property, отображаемых в боковой панели фильтров.

Полный справочник (все ключи, палитра, антипаттерны) → `references/doc-root-schema.md`.
````

- [ ] **Step 2: Add Production эталоны section at end of file**

Find the last section `## Ресурсы` and after the existing bullets list, append:

````markdown

## Production эталоны

Канонический референс структуры — `/Users/mdemyanov/Devel/naumen-ecosystem/business-requirements/`. Production-каталог бизнес-документации SMRM (200+ JTBD/BRQ/процессов): object-нотация frontmatter, `style:` + `icon:` на каждом property, `<view>`-дашборды в `_index.md`. При сомнениях о формате — сверяйся с этим эталоном.
````

- [ ] **Step 3: Verify line count**

Run: `wc -l plugins/gramax/skills/writer/SKILL.md`

Expected: ~300 lines.

---

## Task 6: SKILL.md — расширенный `<view>` + cross-каталожные ссылки

**Files:**
- Modify: `plugins/gramax/skills/writer/SKILL.md` (Краткий справочник блоков + Ссылки)

- [ ] **Step 1: Replace `<view>` row in блоки table**

Find the row in `## Краткий справочник блоков`:
```
| Список дочерних | `<view defs="hierarchy=none" display="List"/>` | Генерация списка в `_index.md` |
```

Replace with:
```
| `<view>` | См. ниже | Динамический список с фильтрами по property |
```

- [ ] **Step 2: Add Дашборды через `<view>` subsection**

Immediately after the table (before "**UI-токены:**"), insert:

````markdown
### Дашборды через `<view>`

Используется в `_index.md` для списков статей с фильтрацией и группировкой:

```markdown
<view defs="Тип контента=ADR&Архитектура&none" groupby="Статус" display="List"/>
```

- `defs="<property>=<v1>&<v2>&none"` — фильтр по property; `none` означает «и статьи без значения». Несколько фильтров через `,`.
- `groupby="<property>"` — группировка результата.
- `display="List"` — представление.

**Когда использовать:** в корневом `_index.md` каталога (дашборд всех статей) или в крупных разделах (>20 статей). Малые разделы (<10 статей) — избыточно.

Подробности и примеры → `references/blocks.md`.
````

- [ ] **Step 3: Add cross-каталожное ограничение в Ссылки**

Find the `## Ссылки` section. After the existing bullet list, append:

````markdown

**Cross-каталожные ссылки:** только inline code, не markdown link. Gramax не резолвит markdown-ссылки между разными `.doc-root.yaml`-каталогами:

❌ `[Документ](other-catalog/path/to/file.md)` — не работает
✅ `` `other-catalog/path/to/file.md` `` — работает (читается как путь)
````

- [ ] **Step 4: Verify line count and structure**

Run: `wc -l plugins/gramax/skills/writer/SKILL.md && grep -c '^## ' plugins/gramax/skills/writer/SKILL.md`

Expected: ~325 lines, 12 top-level sections.

- [ ] **Step 5: Commit Tasks 3, 4, 5, 6 together**

```bash
git add plugins/gramax/skills/writer/SKILL.md \
        plugins/gramax/skills/writer/references/structure.md \
        plugins/gramax/skills/writer/references/doc-root-schema.md
git commit -m "$(cat <<'EOF'
docs(gramax/writer): add doc-root-schema reference + расширить SKILL.md

Закрывает находки #3, #4, #5, #6 из gramax-skills-update.md:
- Новый references/doc-root-schema.md — полный справочник конфигурации
- SKILL.md: краткое описание .doc-root.yaml + ссылка на полный справочник
- SKILL.md: расширенный <view> с фильтрами и группировкой
- SKILL.md: cross-каталожные ссылки только inline code (markdown link не резолвится)
- SKILL.md: новая секция Production эталоны
- structure.md: разделены правила _index.md в корне vs подпапках

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: blocks.md — Расширенный `<view>` раздел

**Files:**
- Modify: `plugins/gramax/skills/writer/references/blocks.md`

- [ ] **Step 1: Find current `<view>` mention**

Run: `grep -n '<view' plugins/gramax/skills/writer/references/blocks.md`

Expected: shows current location of `<view>` references.

- [ ] **Step 2: Add full `<view>` section**

If `<view>` is mentioned briefly somewhere, replace that brief mention. If absent — append the section at the end of file. The full section content:

````markdown
## Дашборды через `<view>`

Динамический список статей с фильтрами и группировкой. Используется в `_index.md`.

### Синтаксис

```markdown
<view defs="Тип контента=ADR&Архитектура&none" groupby="Статус" display="List"/>
```

### Атрибуты

| Атрибут | Назначение |
|---------|------------|
| `defs` | Фильтр: `"property1=val1&val2&none, property2=val3"`. Внутри property-фильтра `&` — OR; между разными property `,` — AND. `none` означает «и статьи без значения этого property». |
| `groupby` | Имя property для группировки результата (опц.) |
| `display` | Представление; на сегодня поддерживается `List` |

### Примеры из эталона `business-requirements/_index.md`

```markdown
### BRQ по статусу

<view defs="Тип сущности=Стейкхолдер&JTBD&Цель&Процесс&none" groupby="Статус" display="List"/>

### BRQ по продуктам

<view defs="Тип сущности=Стейкхолдер&JTBD&Цель&Процесс&none" groupby="Продукты" display="List"/>
```

### Когда использовать

- ✅ Корневой `_index.md` каталога — дашборды всех статей
- ✅ `_index.md` крупного раздела (>20 статей) — для группировки
- ❌ Малые разделы (<10 статей) — избыточно, проще ручная таблица

### Связь со схемой

Имена property в `defs=` и `groupby=` должны совпадать с `name:` property в `.doc-root.yaml` (точно, с учётом регистра). См. `references/doc-root-schema.md`.
````

- [ ] **Step 3: Verify file**

Run: `wc -l plugins/gramax/skills/writer/references/blocks.md && grep -c '^## ' plugins/gramax/skills/writer/references/blocks.md`

Expected: file extended; section count increased by 1.

- [ ] **Step 4: Commit Task 7**

```bash
git add plugins/gramax/skills/writer/references/blocks.md
git commit -m "$(cat <<'EOF'
docs(gramax/writer): expand <view> reference в blocks.md

Полное описание атрибутов defs/groupby/display, примеры из production-эталона,
правила связи имён property со схемой .doc-root.yaml.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: validate_structure.py — Test fixtures

**Files:**
- Create: `plugins/gramax/scripts/tests/__init__.py` (empty marker)
- Create: `plugins/gramax/scripts/tests/fixtures/good/.doc-root.yaml`
- Create: `plugins/gramax/scripts/tests/fixtures/good/article.md`
- Create: `plugins/gramax/scripts/tests/fixtures/good/section/_index.md`
- Create: `plugins/gramax/scripts/tests/fixtures/good/section/child.md`
- Create: `plugins/gramax/scripts/tests/fixtures/bad/.doc-root.yaml`
- Create: `plugins/gramax/scripts/tests/fixtures/bad/flat-notation.md`
- Create: `plugins/gramax/scripts/tests/fixtures/bad/invalid-property.md`
- Create: `plugins/gramax/scripts/tests/fixtures/bad/invalid-value.md`
- Create: `plugins/gramax/scripts/tests/fixtures/bad/orphan-section/child.md`

- [ ] **Step 1: Create `__init__.py` (empty)**

```bash
touch plugins/gramax/scripts/tests/__init__.py
```

- [ ] **Step 2: Create `good/.doc-root.yaml`**

```yaml
title: Good test catalog
description: Valid fixture
language: ru
syntax: XML

properties:
  - name: Тип контента
    type: Enum
    style: green
    icon: file-text
    values:
      - Требование
      - ADR

filterProperties: [Тип контента]
```

- [ ] **Step 3: Create `good/article.md`**

```markdown
---
order: 1
title: "Тестовая статья"
properties:
  - name: Тип контента
    value: [ADR]
---

Содержание.
```

- [ ] **Step 4: Create `good/section/_index.md`**

```markdown
---
order: 2
title: Раздел
---

Описание раздела.
```

- [ ] **Step 5: Create `good/section/child.md`**

```markdown
---
order: 1
title: "Дочерняя статья"
properties:
  - name: Тип контента
    value: [Требование]
---

Содержание.
```

- [ ] **Step 6: Create `bad/.doc-root.yaml`**

```yaml
title: Bad test catalog
description: Fixture с нарушениями
language: ru
syntax: XML

properties:
  - name: Тип контента
    type: Enum
    style: green
    icon: file-text
    values:
      - ADR
      - Требование

filterProperties: [Тип контента]
```

- [ ] **Step 7: Create `bad/flat-notation.md` (V3 violation)**

```markdown
---
order: 1
title: "Плоская нотация"
properties:
  - Тип контента: ADR
---

Должно вызвать V3 warning.
```

- [ ] **Step 8: Create `bad/invalid-property.md` (V4 violation)**

```markdown
---
order: 2
title: "Несуществующий property"
properties:
  - name: НесуществующийProperty
    value: [X]
---

Должно вызвать V4 error.
```

- [ ] **Step 9: Create `bad/invalid-value.md` (V5 violation)**

```markdown
---
order: 3
title: "Значение вне enum"
properties:
  - name: Тип контента
    value: [НетВЕнаме]
---

Должно вызвать V5 error.
```

- [ ] **Step 10: Create `bad/orphan-section/child.md` (V1 violation: no _index.md in parent)**

```markdown
---
order: 1
title: "Сирота"
---

Должно вызвать V1 error: orphan-section/ без _index.md.
```

Note: deliberately NO `bad/orphan-section/_index.md`.

- [ ] **Step 11: Verify all fixtures created**

Run: `find plugins/gramax/scripts/tests/fixtures -type f | sort`

Expected: 9 files (1 yaml + 4 md in good, 1 yaml + 4 md in bad).

---

## Task 9: validate_structure.py — Smoke test skeleton

**Files:**
- Create: `plugins/gramax/scripts/tests/test_validate_structure.py`

- [ ] **Step 1: Write the smoke test**

```python
"""Smoke tests for validate_structure.py."""

import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "validate_structure.py"
FIXTURES = Path(__file__).parent / "fixtures"


def run_validator(target: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["uv", "run", str(SCRIPT), str(target), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class GoodCatalogTests(unittest.TestCase):
    def test_good_catalog_passes(self):
        result = run_validator(FIXTURES / "good")
        self.assertEqual(result.returncode, 0, f"stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertEqual(result.stdout.strip(), "", "Good catalog should produce no messages")


class BadCatalogTests(unittest.TestCase):
    def setUp(self):
        self.result = run_validator(FIXTURES / "bad")

    def test_exits_nonzero(self):
        self.assertNotEqual(self.result.returncode, 0)

    def test_v1_orphan_section(self):
        self.assertIn("orphan-section", self.result.stdout)
        self.assertIn("missing _index.md", self.result.stdout)

    def test_v3_flat_notation(self):
        self.assertIn("flat-notation.md", self.result.stdout)
        self.assertIn("плоская нотация", self.result.stdout)

    def test_v4_invalid_property(self):
        self.assertIn("invalid-property.md", self.result.stdout)
        self.assertIn("не объявлен", self.result.stdout)

    def test_v5_invalid_value(self):
        self.assertIn("invalid-value.md", self.result.stdout)
        self.assertIn("не входит", self.result.stdout)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify all V1, V3, V4, V5 fail (expected — checks not implemented yet)**

Run: `python3 plugins/gramax/scripts/tests/test_validate_structure.py -v 2>&1 | tail -20`

Expected: `BadCatalogTests` fail (V1, V3, V4, V5 not yet detected). `GoodCatalogTests` may pass (good catalog has no violations against current validator).

Note: also expect `test_v2_index_with_properties` to be missing — V2 is tested by absence of properties in `_index.md`; since `good/section/_index.md` already follows the rule, V2 doesn't have a dedicated bad fixture. Skip — V2 covered by inverse logic in good fixture.

- [ ] **Step 3: Add V2 violation fixture and test**

Create `plugins/gramax/scripts/tests/fixtures/bad/orphan-section/_index.md` is wrong — that would fix V1. Instead, add a separate fixture: create `plugins/gramax/scripts/tests/fixtures/bad/index-with-properties/_index.md`:

```markdown
---
order: 1
title: "_index.md с properties (V2)"
properties:
  - name: Тип контента
    value: [ADR]
---

V2 violation.
```

Add a sibling article so the section isn't empty:

`plugins/gramax/scripts/tests/fixtures/bad/index-with-properties/article.md`:

```markdown
---
order: 1
title: "Статья"
properties:
  - name: Тип контента
    value: [ADR]
---

Контент.
```

Add test method to `BadCatalogTests`:

```python
    def test_v2_index_with_properties(self):
        self.assertIn("index-with-properties/_index.md", self.result.stdout)
        self.assertIn("не должен содержать properties", self.result.stdout)
```

- [ ] **Step 4: Re-run to confirm new V2 test also fails (not implemented)**

Run: `python3 plugins/gramax/scripts/tests/test_validate_structure.py BadCatalogTests -v 2>&1 | tail -15`

Expected: `test_v2_index_with_properties` also fails.

- [ ] **Step 5: Commit Tasks 8 + 9 (failing tests)**

```bash
git add plugins/gramax/scripts/tests/
git commit -m "$(cat <<'EOF'
test(gramax/scripts): smoke tests + fixtures для validate_structure

Тесты для проверок V1-V5 + good-каталог. На этом коммите BadCatalogTests
ожидаемо красные — проверки V1-V5 ещё не реализованы.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 10: validate_structure.py — V1 (subfolder `_index.md` required)

**Files:**
- Modify: `plugins/gramax/scripts/validate_structure.py`

- [ ] **Step 1: Add `check_subfolders_have_index` function**

Insert after `check_no_index_in_root` (around line 51):

```python
def check_subfolders_have_index(root: Path, issues: list[Issue]):
    """V1: каждая подпапка с .md или вложенными папками обязана иметь _index.md."""
    for subdir in root.rglob("*"):
        if not subdir.is_dir():
            continue
        if ".gramax" in subdir.parts:
            continue
        if subdir == root:
            continue
        # has any .md file or any subdirectory inside
        has_content = any(
            child.is_dir() or (child.is_file() and child.suffix == ".md")
            for child in subdir.iterdir()
            if child.name != "_index.md"
        )
        if not has_content:
            continue
        if not (subdir / "_index.md").exists():
            issues.append(Issue("error", subdir, "missing _index.md (Gramax не покажет раздел в навигации)"))
```

- [ ] **Step 2: Wire it into `validate()`**

Find in `validate()`:
```python
    check_no_index_in_root(root, issues)
    for md in root.rglob("*.md"):
```

Insert between them:
```python
    check_subfolders_have_index(root, issues)
```

- [ ] **Step 3: Run V1 test**

Run: `python3 plugins/gramax/scripts/tests/test_validate_structure.py BadCatalogTests.test_v1_orphan_section -v`

Expected: PASS.

- [ ] **Step 4: Run good catalog test**

Run: `python3 plugins/gramax/scripts/tests/test_validate_structure.py GoodCatalogTests -v`

Expected: PASS (good catalog has `_index.md` in section/).

---

## Task 11: validate_structure.py — V2 (`_index.md` без properties)

**Files:**
- Modify: `plugins/gramax/scripts/validate_structure.py`

- [ ] **Step 1: Modify `check_frontmatter` to differentiate `_index.md`**

Replace the existing `check_frontmatter` function:

```python
def check_frontmatter(md_file: Path, issues: list[Issue]):
    text = md_file.read_text(encoding="utf-8")
    fm = extract_frontmatter(text)
    if fm is None:
        issues.append(Issue("error", md_file, "missing or invalid frontmatter"))
        return
    for field in ("order", "title"):
        if field not in fm:
            issues.append(Issue("error", md_file, f"frontmatter missing field: {field}"))
    if md_file.name == "_index.md" and "properties" in fm:
        issues.append(Issue("error", md_file, "_index.md не должен содержать properties:"))
```

- [ ] **Step 2: Run V2 test**

Run: `python3 plugins/gramax/scripts/tests/test_validate_structure.py BadCatalogTests.test_v2_index_with_properties -v`

Expected: PASS.

- [ ] **Step 3: Run good catalog test (regression check)**

Run: `python3 plugins/gramax/scripts/tests/test_validate_structure.py GoodCatalogTests -v`

Expected: PASS.

---

## Task 12: validate_structure.py — V3 (плоская нотация warning)

**Files:**
- Modify: `plugins/gramax/scripts/validate_structure.py`

- [ ] **Step 1: Extend `check_frontmatter` with V3 detection**

After the V2 check (the `_index.md` properties block), add:

```python
    # V3: плоская нотация — предупреждение
    if md_file.name != "_index.md" and "properties" in fm:
        props = fm["properties"]
        if isinstance(props, list):
            for entry in props:
                if isinstance(entry, dict) and "name" not in entry:
                    issues.append(
                        Issue("warning", md_file,
                              "устаревшая плоская нотация properties; см. SKILL.md → Frontmatter")
                    )
                    break
```

- [ ] **Step 2: Run V3 test**

Run: `python3 plugins/gramax/scripts/tests/test_validate_structure.py BadCatalogTests.test_v3_flat_notation -v`

Expected: PASS.

- [ ] **Step 3: Run good catalog test**

Run: `python3 plugins/gramax/scripts/tests/test_validate_structure.py GoodCatalogTests -v`

Expected: PASS — good fixtures use object-нотацию.

---

## Task 13: validate_structure.py — V4, V5 (property names + values match schema)

**Files:**
- Modify: `plugins/gramax/scripts/validate_structure.py`

- [ ] **Step 1: Add `load_property_schema` function**

Insert after `check_doc_root` (around line 46):

```python
def load_property_schema(root: Path) -> dict[str, dict] | None:
    """Возвращает {property_name: {type, values}} из .doc-root.yaml.

    None — если schema нечитабельна или содержит экспериментальный type: select.
    """
    yaml_file = root / ".doc-root.yaml"
    try:
        data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    props = data.get("properties", [])
    if not isinstance(props, list):
        return None
    schema: dict[str, dict] = {}
    for p in props:
        if not isinstance(p, dict) or "name" not in p:
            continue
        # detect experimental type: select with values: [{name: X}]
        values = p.get("values", [])
        if any(isinstance(v, dict) for v in values):
            return None
        schema[p["name"]] = {
            "type": p.get("type", "String"),
            "values": [str(v) for v in values],
        }
    return schema
```

- [ ] **Step 2: Modify `validate()` to load schema and pass to `check_frontmatter`**

Replace the loop in `validate()`:

```python
    for md in root.rglob("*.md"):
        if ".gramax" in md.parts:
            continue
        check_frontmatter(md, issues)
        check_tags(md, issues)
```

with:

```python
    schema = load_property_schema(root)
    if schema is None:
        issues.append(Issue("warning", root / ".doc-root.yaml",
                            "schema использует экспериментальный формат values; V4/V5 пропущены"))
    for md in root.rglob("*.md"):
        if ".gramax" in md.parts:
            continue
        check_frontmatter(md, issues, schema)
        check_tags(md, issues)
```

- [ ] **Step 3: Update `check_frontmatter` signature and add V4/V5 logic**

Change signature: `def check_frontmatter(md_file: Path, issues: list[Issue], schema: dict | None = None):`

After the V3 check, add:

```python
    # V4, V5: properties соответствуют schema
    if md_file.name != "_index.md" and schema is not None and "properties" in fm:
        props = fm["properties"]
        if isinstance(props, list):
            for entry in props:
                if not isinstance(entry, dict) or "name" not in entry:
                    continue  # plain notation already reported by V3
                pname = entry["name"]
                if pname not in schema:
                    issues.append(
                        Issue("error", md_file,
                              f'property "{pname}" не объявлен в .doc-root.yaml')
                    )
                    continue
                schema_def = schema[pname]
                if schema_def["type"] != "Enum":
                    continue
                allowed = schema_def["values"]
                values = entry.get("value", [])
                if not isinstance(values, list):
                    values = [values]
                for v in values:
                    if str(v) not in allowed:
                        issues.append(
                            Issue("error", md_file,
                                  f'property "{pname}" имеет значение "{v}", '
                                  f'не входит в [{", ".join(allowed)}]')
                        )
```

- [ ] **Step 4: Run V4 and V5 tests**

Run: `python3 plugins/gramax/scripts/tests/test_validate_structure.py BadCatalogTests.test_v4_invalid_property BadCatalogTests.test_v5_invalid_value -v`

Expected: both PASS.

- [ ] **Step 5: Run full test suite**

Run: `python3 plugins/gramax/scripts/tests/test_validate_structure.py -v`

Expected: all 6 tests PASS (good × 1 + bad × 5: V1, V2, V3, V4, V5).

---

## Task 14: validate_structure.py — `code` опционально в `.doc-root.yaml`

**Files:**
- Modify: `plugins/gramax/scripts/validate_structure.py:42`

- [ ] **Step 1: Remove `code` from required fields**

Find:
```python
    for field in ("code", "title", "language", "syntax"):
```

Replace with:
```python
    for field in ("title", "language", "syntax"):
```

- [ ] **Step 2: Verify good fixture (without `code`) still passes**

Confirm `plugins/gramax/scripts/tests/fixtures/good/.doc-root.yaml` has no `code` field. If it does, remove it:

```bash
grep '^code:' plugins/gramax/scripts/tests/fixtures/good/.doc-root.yaml
```

Expected: no output (no match).

- [ ] **Step 3: Run full test suite**

Run: `python3 plugins/gramax/scripts/tests/test_validate_structure.py -v`

Expected: all PASS.

- [ ] **Step 4: Commit Tasks 10-14 (validator changes)**

```bash
git add plugins/gramax/scripts/validate_structure.py \
        plugins/gramax/scripts/tests/fixtures/
git commit -m "$(cat <<'EOF'
feat(gramax/scripts): validate_structure V1-V5 + code опционально

Закрывает находку #8 из gramax-skills-update.md:
- V1 (error): подпапки с .md обязаны иметь _index.md
- V2 (error): _index.md не должен содержать properties:
- V3 (warning): обнаружение устаревшей плоской нотации frontmatter
- V4 (error): property name должен быть объявлен в .doc-root.yaml
- V5 (error): значение Enum-property должно входить в values:
- check_doc_root: code сделано опциональным (соответствует production-эталону)
- Экспериментальный type: select с values:[{name:X}] — V4/V5 skip с warning

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 15: CHANGELOG.md — Запись 1.1.0

**Files:**
- Modify: `plugins/gramax/CHANGELOG.md`

- [ ] **Step 1: Insert 1.1.0 entry above 1.0.0**

Find the line `## 1.0.0 — 2026-04-19`. Insert above it:

````markdown
## 1.1.0 — 2026-05-06

Schema alignment с production-эталоном `naumen-ecosystem/business-requirements/`. Закрывает 8 из 9 находок из `pg_vector_service/docs/gramax-skills-update.md` (см. ADR-028 проекта pg_vector_service).

### Документация writer-skill
- Frontmatter явно разделён на статьи (object-нотация `properties: [- name/value: [...]]`) и `_index.md` (без `properties:`).
- Антипаттерн плоской нотации помечен как LEGACY.
- Подпапки обязаны содержать `_index.md` (без него Gramax не строит навигацию).
- Новый `references/doc-root-schema.md`: полный справочник конфигурации каталога — корневые ключи, property-определение, палитра `style:` (11 значений), Lucide-иконки, антипаттерны.
- В SKILL.md добавлен компактный раздел `.doc-root.yaml — кратко` со ссылкой на полный справочник.
- Расширен `<view>`: атрибуты `defs`/`groupby`/`display`, синтаксис фильтров, примеры из эталона.
- Cross-каталожные ссылки документированы как inline code (markdown link не резолвится Gramax-ом).
- Новая секция Production эталоны указывает на `naumen-ecosystem/business-requirements/` как канонический референс.

### Валидация
- `validate_structure.py` — пять новых проверок:
  - V1 (error): подпапки с `.md` обязаны иметь `_index.md`.
  - V2 (error): `_index.md` не должен содержать `properties:`.
  - V3 (warning): обнаружение устаревшей плоской нотации frontmatter.
  - V4 (error): `properties.name` должен быть объявлен в `.doc-root.yaml`.
  - V5 (error): значение Enum-property должно входить в `values:`.
- `code` в `.doc-root.yaml` сделано опциональным (соответствует production-эталону `business-requirements`).
- Экспериментальный `type: select` с `values: [{name: X}]` — V4/V5 пропускаются с однократным warning.

### Тесты
- `scripts/tests/test_validate_structure.py` — smoke-тесты на фикстурах good/bad.
- Запуск: `python3 plugins/gramax/scripts/tests/test_validate_structure.py`.

### Не вошло (отложено)
- `--migrate-frontmatter` CLI — отдельный спек, когда возникнет конкретный кандидат миграции.

````

- [ ] **Step 2: Verify CHANGELOG**

Run: `head -40 plugins/gramax/CHANGELOG.md`

Expected: starts with `# Changelog`, then `## 1.1.0 — 2026-05-06` block, then `## 1.0.0 — 2026-04-19`.

- [ ] **Step 3: Commit Task 15**

```bash
git add plugins/gramax/CHANGELOG.md
git commit -m "$(cat <<'EOF'
chore(gramax): release 1.1.0

Schema alignment с production-эталоном. Закрывает 8 из 9 находок из
pg_vector_service/docs/gramax-skills-update.md.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 16: Final acceptance check

- [ ] **Step 1: Запустить smoke-тест целиком**

Run: `python3 plugins/gramax/scripts/tests/test_validate_structure.py -v 2>&1 | tail -10`

Expected: `OK` (6 tests, 0 failures).

- [ ] **Step 2: Прогнать validate_structure.py на good-фикстуре**

Run: `uv run plugins/gramax/scripts/validate_structure.py plugins/gramax/scripts/tests/fixtures/good`

Expected: exit 0, no output.

- [ ] **Step 3: Прогнать validate_structure.py на bad-фикстуре**

Run: `uv run plugins/gramax/scripts/validate_structure.py plugins/gramax/scripts/tests/fixtures/bad 2>&1 | head -20`

Expected: exit 1, минимум 5 строк (ERROR/WARNING) — V1, V2, V3, V4, V5.

- [ ] **Step 4: Проверить размер SKILL.md ≤ 500 строк**

Run: `wc -l plugins/gramax/skills/writer/SKILL.md`

Expected: ≤ 500. Realistically ~325.

- [ ] **Step 5: Проверить git log порядка коммитов**

Run: `git log --oneline -7`

Expected (от свежего к старому):
```
chore(gramax): release 1.1.0
feat(gramax/scripts): validate_structure V1-V5 + code опционально
test(gramax/scripts): smoke tests + fixtures для validate_structure
docs(gramax/writer): expand <view> reference в blocks.md
docs(gramax/writer): add doc-root-schema reference + расширить SKILL.md
docs(gramax/writer): add object-нотацию frontmatter и правило _index.md в подпапках
docs(specs): add Gramax plugin v1.1 design
```

- [ ] **Step 6: Опционально — прогнать на реальном эталоне (если доступен)**

Run: `uv run plugins/gramax/scripts/validate_structure.py /Users/mdemyanov/Devel/naumen-ecosystem/business-requirements 2>&1 | head -20`

Expected: exit 0 (эталон должен пройти валидатор чисто). Если есть warnings — записать их и обсудить с пользователем перед merge.

---

## Acceptance Criteria

1. ✅ Все 8 изменений из find-документа применены (см. Task 1-15).
2. ✅ `validate_structure.py` на тест-фикстуре `bad/` детектит все 5 проверок.
3. ✅ `validate_structure.py` на тест-фикстуре `good/` — exit 0.
4. ✅ SKILL.md ≤ 500 строк (~325 фактически).
5. ✅ CHANGELOG.md содержит запись 1.1.0.
6. ✅ Smoke-тест проходит: `python3 plugins/gramax/scripts/tests/test_validate_structure.py`.
7. ✅ Семь атомарных коммитов поверх spec-коммита.
