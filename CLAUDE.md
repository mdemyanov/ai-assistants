# AI Assistants Project

**Репозиторий:** https://github.com/mdemyanov/ai-assistants

Проект для создания промтов, skills, субагентов и хуков для Claude.

## Структура проекта

```
├── .github/workflows/    # CI/CD (release.yml, validate.yml)
├── system-prompts/       # Системные промты для Claude Desktop
├── skills/               # Навыки (11 активных)
├── scripts/              # CLI утилиты
├── templates/            # Шаблоны (subagent, hook)
├── archive/              # Старые версии
└── REGISTRY.md           # Реестр всех компонентов
```

## Задачи и маршрутизация

При получении задачи — читай соответствующий skill:

| Задача | Skill |
|--------|-------|
| Создать промт | `skills/prompt-creator/SKILL.md` |
| Проверить промт | `skills/prompt-review/SKILL.md` |
| Создать skill | `skills/nau-skill-creator/SKILL.md` |
| Создать субагент | `skills/nau-skill-creator/references/subagents.md` |
| Создать хук | `skills/nau-skill-creator/references/hooks.md` |
| Написать письмо | `skills/correspondence-2/SKILL.md` |
| Подготовиться к встрече | `skills/meeting-prep/SKILL.md` |
| Обработать встречу | `skills/meeting-debrief/SKILL.md` |
| Работа с базой знаний (aigrep) | `skills/aigrep/SKILL.md` |

## Команды

| Команда | Действие |
|---------|----------|
| `/new prompt` | Читай `skills/prompt-creator/SKILL.md` → следуй workflow |
| `/new skill` | Читай `skills/nau-skill-creator/SKILL.md` → следуй workflow |
| `/new subagent` | Читай `skills/nau-skill-creator/references/subagents.md` → создай субагент |
| `/new hook` | Читай `skills/nau-skill-creator/references/hooks.md` → создай хук |
| `/review` | Читай `skills/prompt-review/SKILL.md` → анализируй промт |
| `/list` | Покажи содержимое `REGISTRY.md` |
| `/status` | Покажи структуру проекта и доступные skills |
| `/release` | Создай релиз: `git tag v[X.Y.Z] && git push --tags` |

## Версионирование

При сохранении файлов:
- **Промты**: `system-prompts/[name]_v[X.Y.Z].md`
- **Skills**: `skills/[name]/SKILL.md` + обнови `skills/[name]/_meta.md`
- **Архив**: старые версии → `archive/`
- **Реестр**: обнови `REGISTRY.md` changelog
- **Релиз**: создай тег `vX.Y.Z` для автоматической сборки

## CI/CD

При пуше тега `v*` GitHub Actions:
1. Упаковывает все skills в ZIP (с версией и без)
2. Создаёт GitHub Release с assets
3. Генерирует release notes

**Скачивание skills:**
- Актуальная версия: `https://github.com/mdemyanov/ai-assistants/releases/latest/download/{skill-name}.zip`
- Конкретная версия: `https://github.com/mdemyanov/ai-assistants/releases/download/v{X.Y.Z}/{skill-name}_v{X.Y.Z}.zip`

## Валидация

```bash
python3 scripts/validate_all.py skills/
```

## Стандарты

### Skills
- Frontmatter: обязательные поля `name` и `description`
- Name: hyphen-case, ≤64 символа
- Description: ≤1024 символа, без угловых скобок `<>`
- Body SKILL.md: <500 строк (иначе → references/)

### Антипаттерны
- Не создавай README.md, CHANGELOG.md в skills
- Не дублируй информацию между SKILL.md и references/
- Не добавляй "When to Use" в body — это должно быть в description

## Формат ответов

Краткий, структурированный, без избыточных объяснений. При создании артефактов — используй форматы из соответствующих skills.

## Ограничения

- Не создаю промты для вредоносных целей
- Рекомендую тестирование перед production использованием
