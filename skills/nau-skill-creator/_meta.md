---
id: nau-skill-creator
version: 1.0.0
created: 2025-05-28
updated: 2025-05-28
author: Max Demyanov
status: active
type: skill
tags: [skill, meta, prompt-engineering, automation]
---

# NAU Skill Creator

Создание эффективных skills для Claude Desktop через структурированный 5-этапный процесс.

## Назначение

Автоматизация создания skills с соблюдением best practices Anthropic:
- Concise is Key — экономия контекстного окна
- Progressive Disclosure — трёхуровневая загрузка
- Degrees of Freedom — адаптивная детализация

## Компоненты

| Компонент | Назначение |
|-----------|------------|
| SKILL.md | Основные инструкции и workflow |
| references/anatomy.md | Детальная анатомия skill |
| references/patterns.md | Паттерны структур и вывода |
| assets/skill-template.md | Шаблон SKILL.md |
| scripts/init_skill.py | Инициализация нового skill |
| scripts/quick_validate.py | Валидация структуры |

## Связанные элементы

- [[prompt-creator]] — создание промтов (аналогичный процесс)
- [[prompt-review]] — анализ и улучшение промтов
