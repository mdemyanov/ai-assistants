---
name: skill-manager
description: >-
  Управление внешними skills — скачивание, установка, обновление.
  Используй когда нужно скачать skill с GitHub, установить его локально
  или глобально, проверить обновления, синхронизировать skills из внешних
  репозиториев. Триггеры — install skill, download skill, update skills,
  скачай навык, установи skill, обнови skills.
version: 1.0.0
---

# Skill Manager

Установка и обновление skills из внешних GitHub репозиториев.

## Команды

| Команда | Описание |
|---------|----------|
| `install <url>` | Установить skill из GitHub |
| `update [name]` | Обновить skill(s) из source |
| `list` | Показать установленные skills |
| `check` | Проверить доступные обновления |

## Целевые директории

| Флаг | Директория | Когда использовать |
|------|------------|-------------------|
| `--local` | `./skills/` | Для текущего проекта (по умолчанию) |
| `--global` | `~/.claude/skills/` | Для всех проектов |

## Workflow

### Установка skill

```bash
python skills/skill-manager/scripts/skill_manager.py install <url> [--local|--global]
```

**Форматы URL:**
- `anthropics/skills/skills/docx` — короткий формат
- `https://github.com/owner/repo/blob/main/path/SKILL.md` — полный blob URL
- `https://github.com/owner/repo/tree/main/path` — tree URL
- `https://raw.githubusercontent.com/owner/repo/main/path/SKILL.md` — raw URL

**Примеры:**
```bash
# Установить docx skill локально
python skills/skill-manager/scripts/skill_manager.py install anthropics/skills/skills/docx --local

# Установить глобально
python skills/skill-manager/scripts/skill_manager.py install anthropics/skills/skills/pdf --global

# Перезаписать существующий
python skills/skill-manager/scripts/skill_manager.py install anthropics/skills/skills/xlsx --local --force
```

### Обновление skills

```bash
# Обновить один skill
python skills/skill-manager/scripts/skill_manager.py update docx --local

# Обновить все skills с source
python skills/skill-manager/scripts/skill_manager.py update --all --local

# Принудительно обновить (включая major версии)
python skills/skill-manager/scripts/skill_manager.py update --all --local --force
```

**Версионирование:**
- При minor update (1.0 → 1.1) — обновляет автоматически
- При major update (1.x → 2.x) — предупреждает и требует `--force`
- Версия берётся из frontmatter SKILL.md

### Проверка обновлений

```bash
# Показать доступные обновления без установки
python skills/skill-manager/scripts/skill_manager.py check --local
python skills/skill-manager/scripts/skill_manager.py check --global
```

### Список skills

```bash
python skills/skill-manager/scripts/skill_manager.py list --local
python skills/skill-manager/scripts/skill_manager.py list --global
```

## _meta.md после установки

После установки skill получает `_meta.md` с информацией об источнике:

```yaml
---
source: https://github.com/anthropics/skills
source_path: skills/docx
version: 1.2.0
installed: 2025-01-30
updated: 2025-01-30
---
```

## Зависимости

```bash
pip install pyyaml requests
```

## Переменные окружения

| Переменная | Описание |
|------------|----------|
| `GITHUB_TOKEN` | GitHub Personal Access Token (опционально, увеличивает rate limit) |

## Популярные skills

| Skill | URL | Описание |
|-------|-----|----------|
| docx | `anthropics/skills/skills/docx` | Работа с Word документами |
| pdf | `anthropics/skills/skills/pdf` | Работа с PDF файлами |
| xlsx | `anthropics/skills/skills/xlsx` | Работа с Excel файлами |
| pptx | `anthropics/skills/skills/pptx` | Работа с PowerPoint |
