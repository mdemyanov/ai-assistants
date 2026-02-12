---
id: naumen-smp-scripting
version: 1.1.0
source: library
created: 2026-02-02
updated: 2026-02-02
author: mdemyanov
status: active
type: skill
tags: [naumen, smp, groovy, scripting, api]
---

# Naumen SMP Scripting

Skill для разработки Groovy-скриптов Naumen SMP.

## Установка

```bash
cp -r "/Users/mdemyanov/Documents/AI assistants/skills/naumen-smp-scripting" ~/.claude/skills/
```

## Назначение

- Генерация скриптов по описанию задачи
- Подбор методов API
- Объяснение и анализ кода
- Рефакторинг (устаревшие методы -> рекомендуемые)
- Отладка и поиск ошибок
- Валидация на антипаттерны

## Компоненты

| Файл | Назначение |
|------|-----------|
| SKILL.md | Workflow, quick reference, антипаттерны |
| references/api-quick-ref.md | ТОП-20 методов API с примерами |
| references/script-categories.md | 13 категорий скриптов + переменные |
| references/patterns-antipatterns.md | Типовые решения и ошибки |
| references/api-search-guide.md | Поиск в полной документации |
| references/examples/ | Готовые примеры по категориям |
| references/script-types/ | Спецификации 13 типов скриптов |
| references/validation-checklist.md | Чек-лист проверок |

## Источники данных

- /Users/mdemyanov/Devel/naumen-ecosystem/naumen-smp/script/ (152 файла)
- metody-api.md (575KB) — полный справочник API
- kategorii-skriptov.md — категории скриптов
- tipovye-oshibki-i-sposoby-ikh-ispravleniya.md — типовые ошибки

## Связанные элементы

- [[gramax]] — для документирования скриптов

## Changelog

### 1.1.0 (2026-02-02)
- Добавлена папка script-types/ с 13 спецификациями типов скриптов
- Добавлен validation-checklist.md (проверки производительности, безопасности, корректности)
- Обновлён SKILL.md — интегрирована навигация по типам скриптов
- Типы: filter, computed-attribute, default-value, event-action-system, event-action-user, status-action, condition-script, scheduler-task, import-config, mail-processing, report-template, script-module, access-rights

### 1.0.0 (2026-02-02)
- Инициализация skill
- SKILL.md с workflow и quick reference
- references/ с документацией API и категориями скриптов
- examples/ с готовыми примерами
