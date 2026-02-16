# Installation Scripts for executive-assistant-creator

Набор автоматизированных Python скриптов для установки и настройки executive-assistant-creator.

## Требования

- Python 3.10+
- `uv` для управления зависимостями
- Git (для клонирования репозиториев)

## Скрипты

### 1. `install_skills.py`

**Назначение:** Установка 7 требуемых skills

**Использование:**
```bash
python3 install_skills.py
# или
uv run install_skills.py
```

**Что делает:**
- Загружает skills из GitHub репозиториев:
  - aigrep, correspondence-2, meeting-prep, meeting-debrief (из `mdemyanov/ai-assistants`)
  - xlsx, docx (из `anthropics/skills`)
  - tg-parser (установка через `uv tool install`)
- Сохраняет skills в `~/.claude/skills/`
- Логирует успех/ошибки установки

**Зависимости:** `requests>=2.28`

---

### 2. `setup_mcp.py`

**Назначение:** Настройка MCP серверов в Claude Desktop

**Использование:**
```bash
python3 setup_mcp.py
# или
uv run setup_mcp.py
```

**Что делает:**
- Находит `claude_desktop_config.json` (в зависимости от ОС)
- Создаёт бэкап исходного конфига
- Добавляет конфигурацию aigrep MCP сервера
- Валидирует JSON перед сохранением

**Поддержка ОС:**
- macOS: `~/Library/Application Support/Claude/`
- Linux: `~/.config/Claude/`
- Windows: `%APPDATA%\Claude\`

**Зависимости:** нет (встроенные модули)

---

### 3. `copy_aigrep_config.py`

**Назначение:** Копирование и обновление конфигурации aigrep

**Использование:**
```bash
python3 copy_aigrep_config.py
# или
uv run copy_aigrep_config.py
```

**Интерактивный ввод:**
- Имя vault
- Путь к vault директории (по умолчанию: `~/.claude/vault`)

**Что делает:**
- Ищет существующую конфигурацию aigrep
- Позволяет использовать её как шаблон
- Создаёт структуру vault (папки 00-99)
- Инициализирует индексный файл
- Сохраняет конфиг в `~/.claude/aigrep/config.yaml`

**Зависимости:** `pyyaml>=6.0`

---

### 4. `verify_installation.py`

**Назначение:** Проверка успешности установки всех компонентов

**Использование:**
```bash
python3 verify_installation.py
# или
uv run verify_installation.py
```

**Проверяемые компоненты:**
- ✓ Структура vault (100 папок 00-99)
- ✓ Необходимые файлы (SYSTEM_PROMPT.md, CLAUDE.md)
- ✓ Все 7 skills установлены
- ✓ Структура каждого skill (наличие SKILL.md)
- ✓ MCP конфигурация в Claude Desktop
- ✓ Конфиг aigrep
- ✓ Установлен ли `uv`

**Зависимости:** нет (встроенные модули)

---

## Быстрый старт

### Полная автоматизированная установка

```bash
# 1. Установить skills
python3 install_skills.py

# 2. Настроить MCP
python3 setup_mcp.py

# 3. Настроить aigrep
python3 copy_aigrep_config.py

# 4. Проверить установку
python3 verify_installation.py

# 5. Перезагрузить Claude Desktop
```

### Или использовать uv для запуска

```bash
uv run install_skills.py && \
uv run setup_mcp.py && \
uv run copy_aigrep_config.py && \
uv run verify_installation.py
```

---

## Цветной вывод

Все скрипты используют цветной вывод:
- **✓** (зелёный) — успешная операция
- **✗** (красный) — ошибка
- **⚠** (жёлтый) — предупреждение
- **→** (жирный) — информационное сообщение

---

## PEP 723

Все скрипты следуют стандарту PEP 723 для управления зависимостями. Каждый скрипт содержит блок:

```python
# /// script
# requires-python = ">=3.10"
# dependencies = [...]
# ///
```

Это позволяет запускать их с помощью `uv run` без предварительной установки зависимостей.

---

## Обработка ошибок

Все скрипты имеют:
- Обработку исключений с информативными сообщениями об ошибках
- Проверку существования файлов и директорий
- Валидацию JSON/YAML файлов
- Таймауты для сетевых операций

---

## Логирование

Каждый скрипт выводит:
- Текущий прогресс выполнения
- Пути к обрабатываемым файлам
- Статус успеха/ошибки для каждой операции
- Итоговый отчёт

---

## Совместимость

- ✓ macOS (Darwin)
- ✓ Linux
- ⚠ Windows (поддерживается, но тестировалось только на Unix)

---

## Помощь и отладка

Если возникают проблемы:

1. Проверьте версию Python: `python3 --version` (требуется 3.10+)
2. Проверьте установку `uv`: `uv --version`
3. Проверьте доступ в интернет для загрузки skills
4. Выполните `verify_installation.py` для диагностики
5. Проверьте права доступа на созданные файлы и директории
