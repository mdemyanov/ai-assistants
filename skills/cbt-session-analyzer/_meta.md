---
id: cbt-session-analyzer
version: 1.1.0
created: 2025-01-01
updated: 2025-01-02
author: Max Demyanov
status: active
type: skill
tags: [skill, psychology, cbt, therapy, analysis]
---

# CBT Session Analyzer

Skill для анализа транскриптов КПТ-сессий и формирования когнитивной концептуализации клиента.

## Назначение

- Структурированный разбор терапевтических сессий
- Выявление применённых КПТ-техник
- Отслеживание домашних заданий
- Формирование когнитивной концептуализации

## Целевая аудитория

- Психологи-практики
- Супервизоры
- Студенты КПТ-программ

## Структура

```
cbt-session-analyzer/
├── SKILL.md                              # Основные инструкции
├── _meta.md                              # Этот файл
└── references/
    ├── cbt-techniques.md                 # Справочник КПТ-техник
    ├── cognitive-distortions.md          # Когнитивные искажения (Beck/Burns)
    └── conceptualization-guide.md        # Руководство по концептуализации
```

## Входные данные

TXT-файлы с транскриптами (формат с диаризацией спикеров и таймкодами).
Skill выполняет контекстную коррекцию спикеров при ошибках диаризации.

## Выходные данные

Один markdown-файл — отчёт по сессии в формате МИПЗ.

## Связанные skills

- [[meeting-insights-analyzer/_meta|meeting-insights-analyzer]] — для бизнес-встреч
