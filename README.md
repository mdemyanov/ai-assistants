# AI Assistants

Skills, системные промты и инструменты для Claude Desktop и Claude Code.

## Доступные Skills

| Skill | Описание |
|-------|----------|
| [aigrep](skills/aigrep/) | Работа с базами знаний через aigrep MCP (SQLite + LanceDB) |
| [cbt-session-analyzer](skills/cbt-session-analyzer/) | Анализ КПТ-сессий для психологов |
| [correspondence-2](skills/correspondence-2/) | Деловая переписка по методологии Карепиной |
| [executive-assistant-creator](skills/executive-assistant-creator/) | Создание AI-ассистента для руководителя |
| [meeting-debrief](skills/meeting-debrief/) | Постобработка встреч |
| [meeting-insights-analyzer](skills/meeting-insights-analyzer/) | Анализ транскриптов встреч |
| [meeting-prep](skills/meeting-prep/) | Подготовка к встречам |
| [nau-skill-creator](skills/nau-skill-creator/) | Создание skills для Claude Desktop |
| [prompt-creator](skills/prompt-creator/) | Создание эффективных промтов |
| [prompt-review](skills/prompt-review/) | Анализ и улучшение промтов |
| [public-speaking](skills/public-speaking/) | Подготовка публичных выступлений |

## Установка

### Быстрая установка через curl

**Скачать конкретный skill (актуальная версия):**

```bash
# macOS / Linux
curl -LO https://github.com/mdemyanov/ai-assistants/releases/latest/download/prompt-creator.zip
unzip prompt-creator.zip -d ~/Library/Application\ Support/Claude/skills/
```

**Скачать конкретную версию:**

```bash
curl -LO https://github.com/mdemyanov/ai-assistants/releases/download/v1.0.0/prompt-creator_v1.1.0.zip
```

### Автоматическая установка

```bash
# Установить все skills
curl -sSL https://raw.githubusercontent.com/mdemyanov/ai-assistants/main/scripts/install.sh | bash

# Установить конкретный skill
curl -sSL https://raw.githubusercontent.com/mdemyanov/ai-assistants/main/scripts/install.sh | bash -s -- --skill prompt-creator

# Показать список доступных skills
curl -sSL https://raw.githubusercontent.com/mdemyanov/ai-assistants/main/scripts/install.sh | bash -s -- --list
```

### Ручная установка

1. Скачайте ZIP-архив со [страницы релизов](https://github.com/mdemyanov/ai-assistants/releases)
2. Распакуйте в директорию skills Claude Desktop:
   - **macOS:** `~/Library/Application Support/Claude/skills/`
   - **Windows:** `%APPDATA%\Claude\skills\`
   - **Linux:** `~/.config/claude/skills/`
3. Перезапустите Claude Desktop

## Структура проекта

```
.
├── skills/               # Skills для Claude Desktop (11 шт.)
├── system-prompts/       # Системные промты
├── templates/            # Шаблоны (skill, prompt, subagent, hook)
├── scripts/              # CLI утилиты
├── archive/              # Старые версии
└── CLAUDE.md             # Конфигурация для Claude Code
```

## Для разработчиков

### Валидация

```bash
python3 scripts/validate_all.py skills/
```

### Создание релиза

```bash
git tag v1.0.0
git push --tags
```

GitHub Actions автоматически:
1. Упакует все skills в ZIP-архивы (с версией и без)
2. Создаст GitHub Release с assets

## Лицензия

MIT
