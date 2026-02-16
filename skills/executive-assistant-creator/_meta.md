---
id: executive-assistant-creator
version: 2.0.0
created: 2025-12-09
updated: 2026-02-16
author: Max Demyanov
status: active
type: skill
tags: [skill, assistant, executive, onboarding, obsidian, aigrep, johnny-decimal, automation]
---

# Executive Assistant Creator

Автоматический установщик персонального AI-ассистента для руководителя.

## Описание

Автоматизированное создание и установка полноценного AI-ассистента на базе Claude Desktop + Obsidian. Устанавливает 7 навыков, создаёт структуру vault по Johnny Decimal (00-99), генерирует системный промт и настраивает MCP серверы за 15-30 минут.

### Workflow (6 этапов):

1. Определение роли и контекста
2. Выбор структуры базы знаний (Johnny Decimal 00-99)
3. Генерация системного промта
4. Генерация CLAUDE.md v3.0
5. Техническая настройка Obsidian + aigrep
6. **Автоматическая установка 7 навыков** (NEW)

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

### v2.0.0 (2026-02-16)

**Автоматизация и Johnny Decimal:**

**Major Changes:**
- **Автоматическая установка 7 навыков** через скрипты (install_assistant.py, install_skills.py)
- **Johnny Decimal структура (00-99)** вместо простой нумерации (01-07)
- **Контекст для skills** в CLAUDE.md v3.0 (vault_name, directories, path patterns)
- **Slash-команды** с маппингом на навыки

**Новые компоненты:**
- `references/johnny-decimal-guide.md` — руководство по Johnny Decimal с миграцией
- `scripts/install_assistant.py` — главный оркестратор установки
- `scripts/install_skills.py` — установка навыков через прямую загрузку из GitHub
- `scripts/setup_mcp.py` — автоматическая настройка MCP серверов
- `scripts/copy_aigrep_config.py` — копирование настроек aigrep
- `scripts/verify_installation.py` — проверка успешности установки

**Обновлённые файлы:**
- `SKILL.md` — добавлен Этап 6 (автоустановка), "Быстрый старт", обновлены антипаттерны
- `templates/claude-md-template.md` — v3.0 с Johnny Decimal, контекстом для skills, slash-командами

**Навыки для установки:**
1. aigrep (семантический поиск)
2. correspondence-2 (деловая переписка)
3. meeting-prep (подготовка к встречам)
4. meeting-debrief (постобработка встреч)
5. tg-parser (обработка Telegram)
6. xlsx (работа с Excel)
7. docx (работа с Word)

**Результат:** Время установки 1-2 часа → 15-30 минут

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
