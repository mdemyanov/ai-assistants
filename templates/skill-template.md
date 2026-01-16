---
tags: [template, skill]
created: 2025-05-28
updated: 2025-05-28
---

# Шаблон Skill

> Используй этот шаблон для создания skills в формате Anthropic.
> После создания — добавь запись в [[REGISTRY]].

---

## Структура директории Skill

```
skill-name/
├── SKILL.md              # Обязательно (этот файл)
├── scripts/              # Исполняемый код (опционально)
├── references/           # Документация для контекста (опционально)
└── assets/               # Файлы для вывода (опционально)
```

---

## SKILL.md Template

```markdown
---
name: [skill-name]
description: [Comprehensive description — это главный триггер! Включи: что делает skill + когда его использовать + конкретные триггеры]
---

# [Skill Name]

[Brief overview — 1-2 sentences]

## Workflow

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Key Instructions

[Essential guidance — только то, что Claude не знает]

## Resources

- `scripts/` — [если есть]
- `references/` — [если есть]
- `assets/` — [если есть]

## Examples

**Input:** [Example request]
**Output:** [What skill produces]
```

---

## Metadata для Obsidian

Добавь в отдельный файл `_meta.md` в папке skill:

```yaml
---
id: [unique-id]
version: 1.0.0
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
author: Max Demyanov
status: draft | active | deprecated
type: skill
tags: [skill, tag1, tag2]
---
```

---

## Чеклист перед публикацией

- [ ] `name` в frontmatter соответствует папке
- [ ] `description` содержит триггеры использования
- [ ] SKILL.md < 500 строк
- [ ] Нет дублирования информации между SKILL.md и references/
- [ ] Скрипты протестированы
- [ ] Добавлена запись в [[REGISTRY]]

---

## Связанные материалы

- [[techniques-reference]] — Техники для инструкций
- [[REGISTRY]] — Реестр всех skills
