---
tags: [changelog, releases]
created: 2025-11-30
updated: 2025-11-30
---

# Changelog — История релизов Skills

Хронологическая история всех релизов skills для Claude Desktop.

---

## 2025-11-30 — Первый публичный релиз

### Выпущены skills

| Skill | Версия | Описание |
|-------|--------|----------|
| correspondence-2 | 1.0.0 | Деловая переписка по методологии Карепиной |
| prompt-creator | 1.1.0 | Создание системных промтов |
| prompt-review | 1.1.0 | Анализ и улучшение промтов |
| nau-skill-creator | 1.0.0 | Создание skills для Claude Desktop |

### Инфраструктура

- Создан `package_skills.py` — утилита упаковки skills в ZIP-архивы
- Создана структура `releases/` для управления релизами
- Добавлена документация по установке и обновлению

### Файлы релиза

```
releases/dist/
├── correspondence-2_v1.0.0.zip  (17 KB)
├── prompt-creator_v1.1.0.zip    (9 KB)
├── prompt-review_v1.1.0.zip     (3 KB)
└── nau-skill-creator_v1.0.0.zip (14 KB)
```

---

## Шаблон для будущих релизов

```markdown
## YYYY-MM-DD — Название релиза

### Обновлённые skills

| Skill | Версия | Изменения |
|-------|--------|-----------|
| skill-name | X.Y.Z | Описание изменений |

### Новые skills

- **new-skill** v1.0.0 — описание

### Исправления

- skill-name: описание исправления

### Файлы релиза

- skill-name_vX.Y.Z.zip
```
