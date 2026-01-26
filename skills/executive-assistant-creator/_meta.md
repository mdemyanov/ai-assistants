---
id: executive-assistant-creator
version: 1.1.0
created: 2025-12-09
updated: 2026-01-16
author: Max Demyanov
status: active
type: skill
tags: [skill, assistant, executive, onboarding, obsidian, aigrep]
---

# Executive Assistant Creator

Skill для создания персонального AI-ассистента руководителя.

## Описание

Помогает любому руководителю создать и настроить персонального AI-ассистента на базе Claude Desktop + Obsidian через структурированный процесс:

1. Определение роли и контекста
2. Выбор структуры базы знаний
3. Генерация системного промта
4. Генерация CLAUDE.md
5. Техническая настройка

## Целевая аудитория

- CTO / Технический директор
- CPO / Директор по продукту
- COO / Операционный директор
- HR Director / Директор по персоналу
- Руководитель проекта / PMO
- Любой руководитель с базой знаний в Obsidian

## Основано на

Материалы из `Naumen CTO/0_ASSETS/`:
- AI_ASSISTANT_GUIDE.md
- SYSTEM_PROMPT_TEMPLATE.md
- CLAUDE_MD_TEMPLATE.md
- TECH_SETUP_QUICKSTART.md
- WORK_PATTERNS.md

## Связанные материалы

- [[SKILL]] — основной файл skill
- [[prompt-creator/_meta|prompt-creator]] — создание промтов (можно использовать совместно)
- [[aigrep/_meta|aigrep]] — работа с базой знаний через MCP

## Changelog

### v1.1.0 (2026-01-16)

**Миграция на aigrep:**
- Обновлена техническая настройка: obsidian-mcp → aigrep MCP server
- Упрощена установка: UV + Ollama вместо Obsidian плагинов
- Обновлены команды поиска: `search_vault_smart/simple` → `aigrep:search_vault`
- Обновлены шаблоны: claude-md-template.md, tech-setup.md

### v1.0.0 (2025-12-09)

- Начальная версия
- 5-этапный workflow создания ассистента
- Поддержка ролей: CTO, CPO, COO, HR, PM
- Шаблоны: system-prompt, claude-md, tech-setup
