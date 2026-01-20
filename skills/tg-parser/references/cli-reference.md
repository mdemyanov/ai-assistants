# CLI Reference — tg-parser

Полный справочник команд CLI. Версия: 1.2.0

## Установка

```bash
# PyPI
pip install tg-parser

# С полными зависимостями
pip install "tg-parser[all]"

# UV (рекомендуется)
uv tool install tg-parser
```

## Команды

### parse — Парсинг с фильтрами

Основная команда для извлечения и фильтрации сообщений.

```bash
tg-parser parse <input> [options]
```

**Аргументы:**
- `<input>` — путь к JSON-файлу экспорта

**Опции фильтрации:**
| Опция | Описание |
|-------|----------|
| `--date-from DATE` | Начало периода (YYYY-MM-DD) |
| `--date-to DATE` | Конец периода (YYYY-MM-DD) |
| `--last-days N` | Последние N дней |
| `--last-hours N` | Последние N часов |
| `--senders LIST` | Включить отправителей |
| `--exclude-senders LIST` | Исключить отправителей |
| `--topics LIST` | Включить топики |
| `--exclude-topics LIST` | Исключить топики |
| `--contains REGEX` | Поиск по содержимому |
| `--mentions USER` | Сообщения с упоминанием |
| `--min-length N` | Минимальная длина |
| `--has-attachment` | Только с вложениями |
| `--has-reactions` | Только с реакциями |
| `--exclude-forwards` | Без пересланных |
| `--include-service` | Включить сервисные |

**Опции вывода:**
| Опция | Описание |
|-------|----------|
| `-f, --format` | markdown / json / csv / kb |
| `-o, --output` | Директория для вывода |
| `--split-topics` | Разделить по топикам |
| `--streaming` | Потоковая обработка (>50MB) |

**Примеры:**
```bash
# Дайджест за неделю
tg-parser parse ./export.json --last-days 7 -f markdown -o ./output/

# Решения за январь
tg-parser parse ./export.json \
  --date-from 2026-01-01 --date-to 2026-01-31 \
  --contains "решили|утвердили" \
  -f markdown
```

### chunk — Разбивка для LLM

Разбивает экспорт на части для обработки LLM.

```bash
tg-parser chunk <input> [options]
```

**Опции:**
| Опция | Описание |
|-------|----------|
| `-s, --strategy` | fixed / conversation / topic / daily |
| `--max-tokens N` | Макс. токенов в чанке (default: 4000) |
| `--time-gap N` | Пауза между диалогами в минутах (для conversation) |
| `-o, --output` | Директория для чанков |
| `--streaming` | Потоковая обработка |

**Примеры:**
```bash
# По диалогам
tg-parser chunk ./export.json -s conversation --max-tokens 4000 -o ./chunks/

# По топикам форума
tg-parser chunk ./export.json -s topic -o ./topics/

# По дням
tg-parser chunk ./export.json -s daily -o ./daily/
```

### stats — Статистика чата

Показывает метрики чата.

```bash
tg-parser stats <input> [options]
```

**Опции:**
| Опция | Описание |
|-------|----------|
| `--format` | table / json |
| `--top-senders N` | Топ-N отправителей |
| `--by-day` | Группировка по дням |
| `--by-topic` | Группировка по топикам |

**Примеры:**
```bash
# Общая статистика
tg-parser stats ./export.json

# JSON для обработки
tg-parser stats ./export.json --format json --top-senders 20
```

### mentions — Анализ упоминаний

Показывает частоту упоминаний участников.

```bash
tg-parser mentions <input> [options]
```

**Опции:**
| Опция | Описание |
|-------|----------|
| `--format` | table / json |
| `--top N` | Топ-N упоминаемых |

### split-topics — Разделение форума

Разделяет форум на отдельные файлы по топикам.

```bash
tg-parser split-topics <input> [options]
```

**Опции:**
| Опция | Описание |
|-------|----------|
| `-o, --output` | Директория для файлов |
| `--list` | Только показать список топиков |
| `-f, --format` | markdown / json |

**Примеры:**
```bash
# Список топиков
tg-parser split-topics ./export.json --list

# Разделить на файлы
tg-parser split-topics ./export.json -o ./topics/
```

### config — Управление конфигурацией

```bash
tg-parser config <subcommand>
```

**Подкоманды:**
| Команда | Описание |
|---------|----------|
| `init` | Создать пример конфигурации |
| `show` | Показать текущую конфигурацию |
| `path` | Показать пути поиска конфигов |

### mcp-config — Настройка MCP

Настраивает интеграцию с Claude Desktop/Code.

```bash
tg-parser mcp-config [options]
```

**Опции:**
| Опция | Описание |
|-------|----------|
| `--apply` | Применить конфигурацию |
| `--target` | desktop / code |
| `--show` | Показать текущую конфигурацию |

**Примеры:**
```bash
# Настроить Claude Desktop
tg-parser mcp-config --apply

# Настроить Claude Code
tg-parser mcp-config --apply --target code
```

## Глобальные опции

| Опция | Описание |
|-------|----------|
| `--config PATH` | Использовать конфигурационный файл |
| `--verbose` | Подробный вывод |
| `--version` | Показать версию |
| `--help` | Справка |

## Переменные окружения

| Переменная | Описание |
|------------|----------|
| `TG_PARSER_CONFIG` | Путь к конфигурационному файлу |

## Коды выхода

| Код | Описание |
|-----|----------|
| 0 | Успех |
| 1 | Ошибка парсинга или валидации |
| 2 | Файл не найден |
