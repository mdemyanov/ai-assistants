---
id: prompt-creator
version: 1.1.0
created: 2025-05-28
updated: 2025-05-28
author: Max Demyanov
status: active
type: skill
tags: [skill, prompt-engineering, meta, creation]
---

# Prompt Creator

Skill для создания эффективных системных промтов через структурированный 4-этапный процесс.

## Структура

```
prompt-creator/
├── SKILL.md              # Основные инструкции
├── references/
│   ├── techniques.md     # Справочник техник prompt engineering
│   └── questions.md      # Вопросы для сбора требований
└── assets/
    └── prompt-template.md # Шаблоны промтов разной сложности
```

## Связанные материалы

- [[prompt-review/_meta|prompt-review]] — Анализ и улучшение существующих промтов
- [[skill-creator/_meta|skill-creator]] — Создание skills (родственный skill)
- [[techniques-reference]] — Общий справочник техник

## Changelog

### 1.1.0 (2025-05-28)
- Добавлена секция "Core Principles" с 3 ключевыми принципами
- Добавлена таблица "Degrees of Freedom" для выбора уровня детализации
- Добавлен выбор структуры промта (минимальная/стандартная/расширенная)
- Расширен description в frontmatter — добавлены поддерживаемые структуры
- Workflow переименован для консистентности со skill-creator
- Улучшены таблицы и чеклисты
- Добавлен антипаттерн "объяснение того, что Claude знает"

### 1.0.0 (2025-05-28)
- Инициализация skill
- Создан на основе мета-промта для создания ассистентов
- 4 этапа: анализ → проектирование → создание → валидация
- Добавлены справочники техник и вопросов
- Добавлены шаблоны промтов трёх уровней сложности
