---
tags: [index, registry]
created: 2025-05-28
updated: 2026-01-23
---

# Prompt & Skill Registry

Центральный реестр всех промтов и skills с историей версий.

## Активные промты

```dataview
TABLE version as "Version", status as "Status", domain as "Domain", file.mtime as "Updated"
FROM "system-prompts"
WHERE status = "active"
SORT file.mtime DESC
```

## Активные Skills

```dataview
TABLE version as "Version", status as "Status", file.mtime as "Updated"
FROM "skills"
WHERE status = "active"
SORT file.mtime DESC
```

## Все элементы по статусу

```dataview
TABLE type as "Type", version as "Version", status as "Status"
FROM "system-prompts" OR "skills"
SORT status ASC, file.name ASC
```

---

## Быстрая навигация

### Промты
- [[prompt-engineer-assistant_v3.0.0]] — Мета-ассистент v3 (промты, skills, субагенты, хуки, CI/CD)
- [[kb-setup-wizard_v1.0.0]] — Мастер настройки базы знаний руководителя (интерактивный onboarding, установка инструментов, skills)
- [[cbt-therapist-assistant_v1.1.0]] — Ассистент КПТ-психолога (анализ сессий, концептуализация, супервизия)
- [[cbt-cognitive-model-extractor_v1.0.0]] — Экстрактор когнитивной модели (ситуации → АМ → эмоции → физиология)
- [[aigrep-developer_v1.1.0]] — Ассистент разработки aigrep (Python, SQLite + LanceDB, MCP, LLM)

### Skills
- [[nau-skill-creator/_meta|nau-skill-creator]] — Создание skills для Claude Desktop (5 этапов)
- [[prompt-creator/_meta|prompt-creator]] — Создание эффективных промтов (4 этапа)
- [[prompt-review/_meta|prompt-review]] — Анализ и улучшение промтов
- [[correspondence-2/_meta|correspondence-2]] — Деловая переписка (email и мессенджеры)
- [[meeting-insights-analyzer/_meta|meeting-insights-analyzer]] — Анализ транскриптов встреч (коммуникация, лидерство)
- [[meeting-prep/_meta|meeting-prep]] — Подготовка к встречам (1-1, проектные, комитеты)
- [[meeting-debrief/_meta|meeting-debrief]] — Постобработка встреч (договорённости, решения, задачи)
- [[executive-assistant-creator/_meta|executive-assistant-creator]] — Создание AI-ассистента для руководителя (онбординг)
- [[public-speaking/_meta|public-speaking]] — Подготовка публичных выступлений (структура, аргументация, подача)
- [[cbt-session-analyzer/_meta|cbt-session-analyzer]] — Анализ КПТ-сессий (транскрипты, техники, концептуализация)
- [[aigrep/_meta|aigrep]] — Работа с базами знаний через aigrep MCP (SQLite + LanceDB, семантический поиск)
- [[tg-parser/_meta|tg-parser]] — Обработка экспортов Telegram Desktop (MCP + CLI, дайджесты, фильтрация, chunking)
- [[infoinstyle/_meta|infoinstyle]] — Адаптация текстов под инфостиль (убрать ИИ-паттерны, канцелярит, добавить конкретику)

### Шаблоны
- [[prompt-template]] — Шаблон для системных промтов
- [[skill-template]] — Шаблон для skills
- [[techniques-reference]] — Справочник техник prompt engineering
- [[templates/subagent-template/SUBAGENT|subagent-template]] — Шаблон для субагентов
- [[templates/hook-template/hook|hook-template]] — Шаблон для хуков

### Инструменты
- [[scripts/install|install.sh]] — Установка skills через curl
- [[scripts/ai-skills-cli|ai-skills-cli.py]] — Python CLI для управления skills
- [[scripts/validate_all|validate_all.py]] — Валидация всех skills

### Dev Tasks
- [[dev-tasks/README|README]] — Инструкция по созданию заданий на разработку
- [[dev-tasks/_template/TASK|_template]] — Шаблон задания для Cursor/Claude Code
- [[dev-tasks/chistova16-site/TASK|chistova16-site]] — Hugo-сайт для ЖК «Волжская Life» (ТСН паркинга, К1, К2 + внешние ссылки К3-7)
- [[dev-tasks/gramax-sync/TASK|gramax-sync]] — CLI для управления репозиториями РИТМ (clone/pull/commit/push + MCP)

### Релизы
- [[releases/RELEASE_GUIDE|RELEASE_GUIDE]] — Руководство по выпуску версий
- [[releases/CHANGELOG|CHANGELOG]] — История релизов
- [[releases/INSTALLATION|INSTALLATION]] — Инструкция по установке

---

## Changelog

### 2026-01-23
- Добавлен skill [[infoinstyle/_meta|infoinstyle]] v1.0.0:
  - Адаптация ИИ-текстов под инфостиль по методологии Ильяхова
  - 20 паттернов ИИ-текста по 4 категориям: Content, Language, Style, Communication
  - Три режима: quick (критичное), standard (полный workflow), deep (переработка)
  - References: ai-patterns.md (диагностика), ilyahov-rules.md (правила трансформации)
  - Assets: examples-before-after.md (6 примеров до/после)
  - Добавлена команда `/edit` (алиас `/e`) в CLAUDE.md

### 2026-01-20
- Добавлен skill [[tg-parser/_meta|tg-parser]] v1.0.0:
  - Обработка JSON-экспортов Telegram Desktop через tg-parser (v1.2.0)
  - Dual-mode: MCP tools (Claude Desktop) + CLI через Bash (Claude Code)
  - Автоопределение режима работы
  - 7 use cases: дайджест, лог решений, анализ топиков, активность, упоминания, KB, заметки
  - 9 фильтров: дата, отправитель, топик, содержимое, упоминания, вложения, реакции, пересылка, сервисные
  - 4 формата вывода: markdown, json, csv, kb-template
  - 4 стратегии chunking: fixed, conversation, topic, daily
  - References: filters.md, cli-reference.md, output-formats.md

### 2026-01-16
- Добавлен промт [[kb-setup-wizard_v1.0.0]] v1.0.0:
  - Интерактивный мастер настройки базы знаний руководителя
  - 7 этапов: onboarding → структура → файлы → инструменты → skills → MCP → верификация
  - Установка: Homebrew, Ollama, UV, aigrep
  - Skills: meeting-prep, meeting-debrief, correspondence-2, public-speaking, aigrep
  - Встроенные шаблоны: CLAUDE.md, CLAUDE_DESKTOP.md, Dashboard.md, 5 типов документов
  - Структура Johnny Decimal (00-99)
  - Для нетехнических руководителей: пошаговые инструкции с пояснениями

- **Ренейминг obsidian-kb → aigrep:**
  - Skill `obsidian-kb` переименован в `aigrep`
  - Все MCP-вызовы обновлены: `obsidian-kb:` → `aigrep:`
  - Устаревший API заменён: `search_vault_smart/simple` → `search_vault(search_type=...)`
  - Обновлены skills: meeting-prep, meeting-debrief
  - Обновлены промты: prompt-engineer-assistant
  - Developer prompt переименован: obsidian-kb-developer → aigrep-developer

- **MAJOR RELEASE v3.0.0** — CI/CD, субагенты, хуки, Claude Code:
  - Добавлен [[CLAUDE.md]] — конфигурация проекта для Claude Code
    - Маршрутизация задач к skills
    - Slash-команды для быстрого доступа
    - Стандарты и ограничения
  - Обновлён промт [[prompt-engineer-assistant_v3.0.0]] до v3.0.0:
    - Добавлены команды `/new subagent`, `/new hook`, `/release`
    - Расширена маршрутизация skills с субагентами и хуками
    - Добавлена секция CI/CD и структура проекта
    - Старая версия v2.0.0 → archive/
  - Обновлён skill [[nau-skill-creator/_meta|nau-skill-creator]]:
    - Добавлен `references/subagents.md` — гайд по созданию субагентов
    - Добавлен `references/hooks.md` — гайд по созданию хуков
    - Добавлена секция "Расширенные возможности" в SKILL.md
  - Обновлён skill [[prompt-creator/_meta|prompt-creator]]:
    - Добавлена секция "Интеграции" (CLAUDE.md, делегирование к skills)
  - Добавлены GitHub Actions:
    - `.github/workflows/release.yml` — автоматический релиз при теге v*
    - `.github/workflows/validate.yml` — валидация на PR
  - Добавлены CLI инструменты:
    - `scripts/install.sh` — установка skills через curl
    - `scripts/ai-skills-cli.py` — Python CLI для управления skills
    - `scripts/validate_all.py` — валидация всех skills
  - Добавлены шаблоны:
    - `templates/subagent-template/` — шаблон субагента
    - `templates/hook-template/` — шаблон хука

### 2026-01-11
- Добавлен dev-task [[dev-tasks/chistova16-site/TASK|chistova16-site]]:
  - Hugo-сайт для ЖК «Волжская Life» (chistova16.ru)
  - Полный контент: паркинг, К1, К2 (ТСН)
  - Внешние ссылки: К3-7 (УК/ГБУ)
  - Разделы: новости, документы, отчёты, ОСС (MM-YYYY), FAQ, тарифы, контакты
  - Агрегированная лента новостей всего ЖК
  - GitHub Actions → Yandex Object Storage
- Обновлён промт [[aigrep-developer_v1.1.0]] до v1.1.0:
  - Поддержка aigrep v2.0.7 (Storage Layer Release)
  - Документирована архитектура Hybrid Storage (SQLite + LanceDB)
  - Обновлёна структура проекта: storage/sqlite/, indexing/
  - Добавлены новые компоненты: SQLiteManager, EmbeddingCache, ChangeDetector, FileWatcher
  - Документированы паттерны: Dual-Write, Incremental Indexing, Дедупликация задач
  - Обновлены метрики производительности v2.0
  - Тесты: 1026+ → 1535+
  - Старая версия → archive/
- Обновлён skill [[aigrep/_meta|aigrep]] до v1.2.0:
  - Поддержка aigrep v2.0.7 (Storage Layer Release)
  - Документирована архитектура Hybrid Storage (SQLite + LanceDB)
  - Добавлен Core Principle #6: Hybrid Storage
  - Документированы улучшения производительности v2.0:
    - Инкрементальная индексация (~5 сек для 10 файлов)
    - Поиск по свойствам (~10ms вместо ~500ms)
    - Агрегация (~20ms вместо ~1s)
  - Документированы: FileWatcher, Embedding Cache, Dual-Write, Дедупликация задач
  - Добавлен `list_yandex_models` в tools-reference
  - Обновлены примеры с указанием версий

### 2026-01-08
- Добавлен промт [[aigrep-developer_v1.0.0]] v1.0.0:
  - Ассистент для разработки aigrep в Cursor IDE
  - Экспертиза: Python 3.12+, LanceDB, async/await, Protocol интерфейсы
  - Контекст проекта: архитектура v5, схема БД v4, 1026+ тестов
  - Принципы: SOLID, Clean Architecture, DDD, Dependency Injection
  - Roadmap: Extended Query Layer (v6) — FrontmatterAPI, DataviewService, RipgrepService
  - Процесс: анализ → проектирование → реализация → тестирование
- Добавлен промт [[cbt-cognitive-model-extractor_v1.0.0]] v1.0.0:
  - Извлечение компонентов когнитивной модели из транскриптов КПТ-сессий
  - Формат: ситуации → автоматические мысли → эмоции → физиология
  - Выявление паттернов и цикличности
  - Для ситуативного использования в чате

### 2026-01-07
- Обновлён skill [[aigrep/_meta|aigrep]] до v1.1.0:
  - Поддержка aigrep v1.0.0 (Multi-Provider Production Release)
  - Добавлен Core Principle #5: Multi-Provider (Ollama + Yandex)
  - Обновлён `set_provider` — теперь влияет и на enrichment
  - Документированы `enrichment_stats` в `get_job_status`
  - Добавлен раздел Adaptive Rate Limiting
- Обновлён `Naumen CTO/SYSTEM_PROMPT.md` — версия aigrep 1.0.0

### 2026-01-06
- Добавлен skill [[aigrep/_meta|aigrep]] v1.0.0:
  - Универсальный skill для работы с vault'ами через MCP
  - Поддержка aigrep v0.9.1 (50+ инструментов)
  - Документированы все категории: поиск, граф связей, dataview-запросы, timeline, batch-операции
  - Паттерны запросов: ID > Name, фильтры, комбинации
  - Auto-intent detection описан
  - References: tools-reference.md, query-patterns.md, intent-detection.md

### 2026-01-02
- Обновлён системный промт `Naumen CTO/SYSTEM_PROMPT.md` на основе результатов тестирования R6:
  - Добавлена "Краткая справка по поиску" — быстрый доступ к рекомендуемым паттернам
  - Документировано: поиск по ID (100% точность) как основной способ поиска документов и людей
  - Явно указаны ограничения: поиск людей по имени НЕ работает, фильтр дат `created:` работает некорректно
  - Добавлена таблица выбора стратегии поиска
  - Добавлены предупреждения о PROCEDURAL/EXPLORATORY (могут не найти в топ-5)
  - Сокращена избыточная документация

### 2025-01-02
- Обновлён skill [[cbt-session-analyzer/_meta|cbt-session-analyzer]] до v1.1.0:
  - Новый формат отчёта по шаблону МИПЗ
  - Таблицы для техник (техника/контекст/эффективность) и ДЗ (задание/статус/комментарий)
  - Структурированная концептуализация (убеждения/копинг/искажения)
  - Отдельный блок цитат из сессии

### 2025-01-01
- Добавлен промт [[cbt-therapist-assistant_v1.1.0]] v1.1.0:
  - Ассистент для КПТ-психологов и супервизоров
  - Анализ сессий, концептуализация, обратная связь терапевту
  - Интеграция со skill cbt-session-analyzer (делегирование)
- Добавлен skill [[cbt-session-analyzer/_meta|cbt-session-analyzer]] v1.0.0:
  - Анализ транскриптов КПТ-сессий для психологов и супервизоров
  - Формат входных данных: TXT с диаризацией и таймкодами
  - Контекстная коррекция спикеров при ошибках автоматической диаризации
  - Выявление целей сессий, проблем клиента, применённых техник
  - Отслеживание домашних заданий и их статуса
  - Итоги для клиента и для терапевта (качество работы, спорные моменты)
  - Когнитивная концептуализация: биография, глубинные/промежуточные убеждения, копинг, искажения
  - References: cbt-techniques.md (20+ техник), cognitive-distortions.md (15 искажений по Beck/Burns), conceptualization-guide.md

### 2025-12-30
- Добавлен dev-task [[dev-tasks/gramax-sync/TASK|gramax-sync]]:
  - CLI для синхронизации Git-репозиториев проекта РИТМ (Gramax)
  - Команды: clone, pull, status, commit, push, sync
  - MCP server для интеграции с Claude
  - OAuth аутентификация через браузер
  - Python 3.10+, Click, GitPython, Rich, Pydantic
- Добавлена директория `dev-tasks/` для заданий на разработку:
  - Шаблон задания: TASK.md, CONTEXT.md, references/, assets/
  - Оптимизировано для Cursor и Claude Code
  - README с workflow
- Обновлён skill [[meeting-prep/_meta|meeting-prep]] до v1.1.0:
  - **Универсальность:** skill теперь работает с любым vault
  - Параметры (vault_name, пути) получаются из системного промта ассистента
  - Fallback: определение структуры через поиск или вопрос пользователю
  - Обновлён API поиска: `search_vault_smart/simple` → `aigrep:search_vault`
  - Поддержка фильтров: `type:`, `links:`, `created:>`, `tags:`
  - Обновлён `references/data-sources.md` — универсальный, с типичными структурами vault
- Обновлён skill [[meeting-debrief/_meta|meeting-debrief]] до v1.1.0:
  - **Универсальность:** skill теперь работает с любым vault
  - Параметры окружения получаются из системного промта
  - Обновлён API поиска на `aigrep:search_vault`
  - Пути указываются через плейсхолдеры `[people_dir]`, `[projects_dir]`

### 2025-12-23
- Добавлен skill [[public-speaking/_meta|public-speaking]] v1.0.0:
  - Подготовка публичных выступлений на основе методологии Никиты Непряхина
  - 4-этапный workflow: понимание → структурирование → аргументация → подача
  - Degrees of Freedom: экспресс / стандарт / глубокий
  - Формула аргументации: тезис → обоснование → иллюстрация → мини-вывод
  - References: preparation-questions, speech-structure, delivery-techniques
  - Asset: speech-outline-template

### 2025-12-10
- Добавлен skill [[meeting-debrief/_meta|meeting-debrief]] v1.0.0:
  - Постобработка встреч на основе транскриптов, переписки или интервью
  - Извлечение договорённостей, решений, задач
  - Сравнение с повесткой (план vs факт)
  - Уточняющие вопросы при недостатке информации
  - Предложения по обновлению vault с подтверждением
  - Интеграция с meeting-prep и meeting-insights-analyzer
- Добавлен skill [[meeting-prep/_meta|meeting-prep]] v1.0.0:
  - Подготовка к встречам на основе данных vault
  - Поддержка 1-1, проектных встреч, комитетов и произвольных форматов
  - Интеграция с meeting-insights-analyzer (deep-режим)
  - Автоматический сбор договорённостей, целей, блокеров из профилей
  - Валидация качества повестки
  - Адаптивная структура (не жёсткие шаблоны)

### 2025-12-09
- Добавлен skill [[executive-assistant-creator/_meta|executive-assistant-creator]] v1.0.0:
  - Создание персонального AI-ассистента для руководителя
  - Поддержка ролей: CTO, CPO, COO, HR Director, PM
  - Шаблоны системного промта и CLAUDE.md
  - Техническая инструкция по настройке
  - Паттерны эффективной работы
  - На основе материалов Naumen CTO/0_ASSETS/

### 2025-12-05
- Добавлен skill [[meeting-insights-analyzer/_meta|meeting-insights-analyzer]] v1.0.0:
  - Анализ транскриптов из Контур Толк
  - Русскоязычные паттерны коммуникации (references/russian-patterns.md)
  - Адаптация под роль CTO: 1-1, production review, комитеты
  - Интеграция с базой знаний Naumen CTO (шаблон в 04_TEMPLATES/)

### 2025-12-01
- Обновлён [[prompt-engineer-assistant_v2.0.0]] до v2.0.0 — полная переработка:
  - Интеграция с Obsidian MCP (`ai-knowlage-obsidian-mcp`) как основной способ доступа
  - Делегирование работы к специализированным skills
  - Сокращение размера промта с ~2500 до ~800 слов
  - Добавлена маршрутизация по инструментам
  - Старая версия → archive/

### 2025-11-30
- Создан раздел `releases/` для управления релизами skills
- Добавлен `package_skills.py` — утилита упаковки skills в ZIP-архивы
- Добавлено руководство [[releases/RELEASE_GUIDE|RELEASE_GUIDE]]
- Добавлена история релизов [[releases/CHANGELOG|CHANGELOG]]
- Добавлена инструкция по установке [[releases/INSTALLATION|INSTALLATION]]
- Первый публичный релиз всех skills (v1.0.0 / v1.1.0)

### 2025-05-28
- Инициализация репозитория
- Создана структура: system-prompts/, skills/, templates/, archive/
- Добавлен [[prompt-engineer-assistant_v1.0.0]] v1.0.0
- Добавлен [[techniques-reference]] — справочник техник с примерами
- Настроена Obsidian-интеграция с Dataview
- Добавлен skill [[prompt-review/_meta|prompt-review]] v1.0.0
- Добавлен skill [[correspondence-2/_meta|correspondence-2]] v1.0.0 — деловая переписка по методологии Карепиной
- Добавлен skill [[prompt-creator/_meta|prompt-creator]] v1.0.0 — создание промтов через структурированный процесс
- Обновлён skill [[prompt-creator/_meta|prompt-creator]] до v1.1.0 — добавлены Core Principles, Degrees of Freedom, выбор структуры
- Добавлен skill [[nau-skill-creator/_meta|nau-skill-creator]] v1.0.0 — создание skills для Claude Desktop
