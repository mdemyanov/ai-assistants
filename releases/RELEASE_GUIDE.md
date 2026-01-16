---
tags: [guide, release, skills]
created: 2025-11-30
updated: 2025-11-30
---

# Руководство по релизам Skills

Процесс подготовки, упаковки и распространения skills для Claude Desktop.

## Структура раздела releases/

```
releases/
├── RELEASE_GUIDE.md      # Это руководство
├── CHANGELOG.md          # История всех релизов
├── dist/                 # Готовые архивы для распространения
│   ├── correspondence-2_v1.0.0.zip
│   ├── prompt-creator_v1.1.0.zip
│   └── ...
└── INSTALLATION.md       # Инструкция для получателей
```

---

## Процесс выпуска новой версии

### 1. Обновление версии в skill

Измени версию в файлах skill:

**SKILL.md** (если есть поле version в frontmatter):
```yaml
---
name: skill-name
version: 1.2.0  # ← Обнови версию
description: ...
---
```

**_meta.md**:
```yaml
---
version: 1.2.0  # ← Обнови версию
updated: 2025-11-30  # ← Обнови дату
---
```

### 2. Обновление REGISTRY.md

Добавь запись в секцию Changelog:

```markdown
### 2025-11-30
- Обновлён skill [[prompt-creator/_meta|prompt-creator]] до v1.2.0 — добавлена поддержка X
```

### 3. Создание архива

```bash
cd ~/Documents/AI\ assistants/skills

# Упаковать конкретный skill
python package_skills.py . ../releases/dist --skill prompt-creator

# Или упаковать все skills
python package_skills.py . ../releases/dist --all
```

### 4. Обновление CHANGELOG.md

Добавь запись о релизе в `releases/CHANGELOG.md`.

### 5. Распространение

Передай получателям:
- Архив(ы) из `releases/dist/`
- Файл `releases/INSTALLATION.md`

---

## Версионирование

Используем [Semantic Versioning](https://semver.org/):

| Изменение | Версия | Пример |
|-----------|--------|--------|
| **MAJOR** — несовместимые изменения | X.0.0 | 2.0.0 |
| **MINOR** — новые функции, обратно совместимые | 0.X.0 | 1.3.0 |
| **PATCH** — исправления, мелкие улучшения | 0.0.X | 1.2.1 |

### Когда повышать версию

**MAJOR (X.0.0):**
- Полная переработка структуры skill
- Изменение workflow, ломающее обратную совместимость
- Удаление ключевых функций

**MINOR (0.X.0):**
- Добавление новых возможностей
- Новые скрипты или референсы
- Существенные улучшения без ломающих изменений

**PATCH (0.0.X):**
- Исправление багов
- Улучшение формулировок
- Обновление примеров
- Мелкие дополнения

---

## Утилита package_skills.py

### Команды

```bash
# Показать список skills с версиями
python package_skills.py . ./dist --list

# Упаковать все skills
python package_skills.py . ./dist --all

# Упаковать один skill
python package_skills.py . ./dist --skill correspondence-2

# Без версии в имени файла
python package_skills.py . ./dist --all --no-version

# Без генерации инструкции
python package_skills.py . ./dist --all --no-guide
```

### Что включается в архив

✅ **Включается:**
- SKILL.md
- scripts/
- references/
- assets/

❌ **Исключается автоматически:**
- _meta.md (Obsidian metadata)
- __pycache__/
- .DS_Store
- .git/
- *.pyc
- package_skills.py

---

## Чеклист релиза

- [ ] Версия обновлена в SKILL.md и/или _meta.md
- [ ] Изменения описаны в REGISTRY.md
- [ ] Skill протестирован локально
- [ ] Создан архив через package_skills.py
- [ ] Добавлена запись в releases/CHANGELOG.md
- [ ] Архив проверен (можно распаковать и структура корректна)

---

## Быстрый релиз (скрипт)

Для автоматизации можно использовать:

```bash
#!/bin/bash
# quick_release.sh — быстрый релиз всех skills

cd ~/Documents/AI\ assistants/skills
python package_skills.py . ../releases/dist --all

echo "✅ Архивы созданы в releases/dist/"
ls -la ../releases/dist/*.zip
```

---

## См. также

- [[REGISTRY]] — центральный реестр всех skills
- [[releases/CHANGELOG]] — история релизов
- [[releases/INSTALLATION]] — инструкция для получателей
