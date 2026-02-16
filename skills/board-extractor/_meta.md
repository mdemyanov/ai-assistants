---
id: board-extractor
version: 1.0.0
created: 2026-02-04
updated: 2026-02-12
author: Max Demyanov
status: active
type: skill
tags: [skill, extraction, gramax, requirements, business-analysis]
---

# board-extractor

Извлечение бизнес- и dev-сущностей из досок (Miro/Figma PDF, Markdown, Confluence) и конвертация в Gramax-формат.

## Описание

Автоматизирует извлечение требований из досок и конвертацию в структурированный Gramax-формат с распределением по двум каталогам (business-requirements и dev-requirements).

### Поддерживаемые форматы входных данных:
- PDF экспорты (Miro, Figma)
- Markdown файлы
- Confluence экспорты

### Сущности для извлечения:
**Business:**
- Стейкхолдер
- JTBD (Jobs To Be Done)
- Цель
- BRQ (Business Requirement)
- Процесс

**Dev:**
- Эпик
- User Story
- Модуль
- FR (Functional Requirement)
- NFR (Non-Functional Requirement)

## Changelog

### v1.0.0 (2026-02-12)

Initial release.

**Возможности:**
- Интерактивное создание сущностей через `/board`
- Автоматическое извлечение через `/extract`
- Поддержка PDF, Markdown, Confluence
- Распределение по business/dev каталогам
- Генерация Gramax-совместимого формата
- Библиотека шаблонов для всех типов сущностей
- Примеры для каждого типа
