---
tags: [guide, installation]
created: 2025-11-30
updated: 2025-11-30
---

# Установка Skills для Claude Desktop

Инструкция для получателей skills.

---

## Требования

- Claude Desktop с поддержкой custom skills
- Python 3.7+ (для скриптов внутри некоторых skills)
- PyYAML: `pip install pyyaml`

---

## Быстрая установка

### Шаг 1: Определите директорию skills

| ОС | Путь |
|----|------|
| **macOS** | `~/Library/Application Support/Claude/skills/` |
| **Windows** | `%APPDATA%\Claude\skills\` |
| **Linux** | `~/.config/Claude/skills/` |

Если директория не существует, создайте её:

```bash
# macOS
mkdir -p ~/Library/Application\ Support/Claude/skills

# Linux
mkdir -p ~/.config/Claude/skills
```

### Шаг 2: Распакуйте архивы

**macOS / Linux:**
```bash
cd ~/Library/Application\ Support/Claude/skills  # ваш путь

# Распакуйте нужные skills
unzip correspondence-2_v1.0.0.zip
unzip prompt-creator_v1.1.0.zip
unzip prompt-review_v1.1.0.zip
unzip skill-creator_v1.0.0.zip
```

**Windows:**
Распакуйте архивы через проводник или:
```powershell
Expand-Archive -Path .\correspondence-2_v1.0.0.zip -DestinationPath $env:APPDATA\Claude\skills\
```

### Шаг 3: Перезапустите Claude Desktop

---

## Проверка установки

После установки структура должна выглядеть так:

```
skills/
├── correspondence-2/
│   ├── SKILL.md           # ← Обязательный файл
│   ├── assets/
│   ├── references/
│   └── scripts/
├── prompt-creator/
│   ├── SKILL.md
│   ├── assets/
│   └── references/
├── prompt-review/
│   ├── SKILL.md
│   └── assets/
└── skill-creator/
    ├── SKILL.md
    ├── assets/
    ├── references/
    └── scripts/
```

---

## Доступные Skills

### correspondence-2 (v1.0.0)

**Назначение:** Деловая переписка по методологии "Переписка 2.0" Саши Карепиной.

**Триггеры:**
- "Напиши письмо..."
- "Составь email..."
- "Сообщение в телеграм/слак..."
- "Ответь на переписку..."

**Примеры использования:**
- "Напиши письмо клиенту о переносе сроков проекта"
- "Составь сообщение в слак команде о результатах спринта"
- "Помоги ответить на это письмо с жалобой"

---

### prompt-creator (v1.1.0)

**Назначение:** Создание эффективных системных промтов через структурированный процесс.

**Триггеры:**
- "Создай промт для..."
- "Напиши системные инструкции..."
- "Сделай ассистента для..."

**Примеры использования:**
- "Создай промт для код-ревью ассистента"
- "Сделай системные инструкции для чат-бота поддержки"
- "Напиши промт для ассистента по финансовому анализу"

---

### prompt-review (v1.1.0)

**Назначение:** Анализ и улучшение существующих промтов.

**Триггеры:**
- "Проверь промт..."
- "Проанализируй инструкции..."
- "Сделай ревью промта..."
- "Как улучшить этот промт?"

**Примеры использования:**
- "Проверь этот промт на ошибки: [промт]"
- "Как улучшить эти системные инструкции?"
- "Оцени качество этого промта"

---

### skill-creator (v1.0.0)

**Назначение:** Создание skills для Claude Desktop.

**Триггеры:**
- "Создай skill для..."
- "Сделай навык для Claude..."
- "Автоматизируй задачу..."

**Примеры использования:**
- "Создай skill для генерации SQL запросов"
- "Сделай навык для работы с нашим API"
- "Автоматизируй создание отчётов"

---

## Обновление Skills

### Вариант 1: Полная замена

1. Удалите старую директорию skill
2. Распакуйте новый архив
3. Перезапустите Claude Desktop

```bash
rm -rf ~/Library/Application\ Support/Claude/skills/prompt-creator
unzip prompt-creator_v1.2.0.zip -d ~/Library/Application\ Support/Claude/skills/
```

### Вариант 2: Перезапись

```bash
unzip -o prompt-creator_v1.2.0.zip -d ~/Library/Application\ Support/Claude/skills/
```

Флаг `-o` перезапишет существующие файлы.

---

## Устранение проблем

### Skill не активируется

1. Проверьте наличие SKILL.md в корне директории skill:
   ```bash
   ls ~/Library/Application\ Support/Claude/skills/skill-name/SKILL.md
   ```

2. Убедитесь, что SKILL.md содержит корректный YAML frontmatter:
   ```yaml
   ---
   name: skill-name
   description: ...
   ---
   ```

3. Перезапустите Claude Desktop

### Ошибки Python-скриптов

```bash
# Проверьте версию Python
python3 --version  # Требуется 3.7+

# Установите зависимости
pip install pyyaml
```

### Архив не распаковывается

```bash
# Проверьте целостность
unzip -t archive.zip

# Принудительная распаковка
unzip -o archive.zip -d ./destination/
```

---

## Удаление Skill

```bash
rm -rf ~/Library/Application\ Support/Claude/skills/skill-name
```

После удаления перезапустите Claude Desktop.

---

## Контакты

При возникновении вопросов обращайтесь к автору skills.
