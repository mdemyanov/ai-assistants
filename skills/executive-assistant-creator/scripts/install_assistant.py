#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0"]
# ///

"""
install_assistant.py - главный оркестратор установки executive-assistant-creator.

Интерактивная установка с созданием структуры vault, системного промта и конфигурации.
"""

import os
import sys
import json
import subprocess
import logging
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str) -> None:
    """Вывести заголовок."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}\n")

def print_info(text: str) -> None:
    """Вывести информационное сообщение."""
    print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")

def print_success(text: str) -> None:
    """Вывести сообщение об успехе."""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text: str) -> None:
    """Вывести сообщение об ошибке."""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_warning(text: str) -> None:
    """Вывести предупреждение."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def setup_logging(log_file: Path) -> logging.Logger:
    """Настроить логирование."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def validate_role(role: str) -> bool:
    """Проверить валидность роли."""
    valid_roles = ['CTO', 'CPO', 'COO', 'CFO', 'HR', 'PM']
    return role.upper() in valid_roles

def validate_vault_path(path_str: str) -> bool:
    """Проверить валидность пути к vault."""
    path = Path(path_str).expanduser()
    return path.exists() and path.is_dir()

def input_with_validation(prompt: str, validator=None, retry_count: int = 3) -> Optional[str]:
    """Получить ввод пользователя с валидацией."""
    for attempt in range(retry_count):
        value = input(f"{Colors.BLUE}➜ {prompt}{Colors.ENDC} ").strip()

        if not value:
            print_warning(f"Пожалуйста, введите значение (попыток осталось: {retry_count - attempt - 1})")
            continue

        if validator is None or validator(value):
            return value
        else:
            print_warning(f"Невалидное значение. Попыток осталось: {retry_count - attempt - 1}")

    return None

def collect_user_input() -> Dict[str, str]:
    """Собрать интерактивный ввод от пользователя."""
    print_header("⚙️  Настройка AI-ассистента Executive")

    # Роль пользователя
    print_info("Выберите роль: CTO, CPO, COO, CFO, HR, PM")
    role = input_with_validation("Роль:", lambda x: validate_role(x))
    if not role:
        print_error("Не удалось получить роль. Прерывание.")
        sys.exit(1)

    # Название vault
    vault_name = input_with_validation("Название vault (например, CTO_Vault):")
    if not vault_name:
        print_error("Не удалось получить название vault. Прерывание.")
        sys.exit(1)

    # Путь к vault
    vault_path = input_with_validation(
        "Путь к vault (например, ~/Documents/vault):",
        lambda x: validate_vault_path(x)
    )
    if not vault_path:
        print_error("Путь к vault не существует или невалиден. Прерывание.")
        sys.exit(1)

    # Owner name
    owner_name = input_with_validation("Ваше имя (для кастомизации):")
    if not owner_name:
        print_error("Не удалось получить имя. Прерывание.")
        sys.exit(1)

    # Owner ID
    owner_id = input_with_validation("Ваш ID (опционально, например, user@company.com):")
    if not owner_id:
        owner_id = "user"

    return {
        "role": role.upper(),
        "vault_name": vault_name,
        "vault_path": Path(vault_path).expanduser().as_posix(),
        "owner_name": owner_name,
        "owner_id": owner_id,
    }

def create_vault_structure(vault_path: Path, role: str, logger: logging.Logger) -> bool:
    """Создать структуру vault с Johnny Decimal (00-99)."""
    print_info("Создаю структуру vault...")

    # Базовая структура
    directories = [
        "00_CORE/identity",
        "00_CORE/stakeholders",
        "00_CORE/strategy",
        "10_PEOPLE",
        "20_MEETINGS/committees",
        "20_MEETINGS/standups",
        "30_PROJECTS/active",
        "30_PROJECTS/backlog",
        "30_PROJECTS/archive",
        "40_DECISIONS/adr",
        "40_DECISIONS/policies",
        "40_DECISIONS/journal",
        "50_KNOWLEDGE/methodologies",
        "50_KNOWLEDGE/processes",
        "60_DOMAIN",
        "90_TEMPLATES",
        "99_ARCHIVE",
    ]

    # Добавить subdomain для 60_DOMAIN в зависимости от роли
    subdomain_map = {
        'CTO': 'technology',
        'CPO': 'product',
        'COO': 'operations',
        'CFO': 'finance',
        'HR': 'hr',
        'PM': 'projects',
    }
    subdomain = subdomain_map.get(role, 'domain')
    directories.append(f"60_DOMAIN/{subdomain}")

    try:
        for directory in directories:
            dir_path = vault_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Создана директория: {dir_path}")

        print_success(f"Структура vault создана в {vault_path}")
        return True
    except Exception as e:
        print_error(f"Ошибка при создании структуры: {e}")
        logger.error(f"Ошибка при создании структуры: {e}")
        return False

def generate_system_prompt(role: str, vault_name: str, vault_path: str, owner_name: str) -> str:
    """Генерировать SYSTEM_PROMPT.md на основе роли."""

    methodologies_map = {
        'CTO': 'DDD, Arc42, TOGAF, ITIL',
        'CPO': 'Jobs to Be Done, OKR, RICE, Kano Model',
        'COO': 'Lean, Six Sigma, ITIL, Process Mining',
        'CFO': 'GAAP, IFRS, Zero-Based Budgeting',
        'HR': 'Competency Framework, OKR, Talent Review',
        'PM': 'PMBOK, Agile, Critical Chain, Risk Management',
    }

    limitations_map = {
        'CTO': '- Не принимай архитектурные решения без анализа рисков\n- Не изменяй production системы без планов отката\n- Учитывай legacy системы и техдолг',
        'CPO': '- Не путай feature requests с customer problems\n- Не делай решения на основе single customer feedback\n- Учитывай тремоли и компромиссы с другими подразделениями',
        'COO': '- Не оптимизируй процессы без анализа impact на людей\n- Учитывай compliance и regulatory требования\n- Не жертвуй качеством ради скорости',
        'CFO': '- Всегда учитывай tax implications\n- Анализируй cash flow, а не только прибыль\n- Помни про compliance и аудиторские требования',
        'HR': '- Соблюдай законодательство по трудоустройству\n- Учитывай культуру компании\n- Защищай конфиденциальность сотрудников',
        'PM': '- Не запускай project без clear scope и requirements\n- Анализируй риски и dependencies\n- Помни про resource constraints',
    }

    methodologies = methodologies_map.get(role, 'Standard best practices')
    limitations = limitations_map.get(role, '- Standard limitations')

    prompt = f"""# Системный промт для AI-ассистента {role}

Создано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Vault: {vault_name}
Owner: {owner_name}

## 1. Роль

Ты — персональный AI-ассистент {role} в компании. Твоя задача — помогать думать лучше, а не думать вместо меня.

**Ключевой принцип:** Ты должен **оспаривать**, а не **подтверждать**. Если ты всегда соглашаешься — ты бесполезен.

## 2. Принципы работы

1. **Критическое мышление > согласие** — Видишь ошибку — говоришь прямо
2. **Факты > предположения** — Не знаешь — так и скажи
3. **Контекст > шаблоны** — Учитывай специфику компании
4. **Конкретика > общие слова** — Примеры с указанием источника
5. **Альтернативы > один вариант** — Всегда предлагай варианты

## 3. Ограничения

{limitations}

## 4. Методологии

Фреймворки для работы:
- {methodologies.replace(', ', chr(10) + '- ')}

## 5. Протокол работы

Для каждой задачи:
1. Загрузи контекст из базы знаний
2. Проверь ограничения
3. Проанализируй ситуацию критически
4. Предложи 2-3 варианта с обоснованием
5. Укажи риски и компромиссы
6. Дай конкретные следующие шаги

## 6. База знаний

Структура vault (Johnny Decimal):
- **00_CORE/** — Идентичность, стейкхолдеры, стратегия
- **10_PEOPLE/** — Информация о команде
- **20_MEETINGS/** — Committees, standups, meeting notes
- **30_PROJECTS/** — Active, backlog, archive projects
- **40_DECISIONS/** — ADR, policies, decision journal
- **50_KNOWLEDGE/** — Методологии, процессы, best practices
- **60_DOMAIN/** — Специфичные для роли знания ({role.lower()})
- **90_TEMPLATES/** — Шаблоны и примеры
- **99_ARCHIVE/** — Архивные материалы

Путь: {vault_path}

## 7. Инструменты

- **Filesystem** — чтение/создание/редактирование файлов
- **aigrep** — семантический поиск по vault
- **Slack/Email** — получение контекста из коммуникаций

## 8. Самопроверка

Перед ответом спроси себя:
- [ ] Прочитал контекст из базы?
- [ ] Не нарушаю ограничения?
- [ ] Даю конкретику, а не общие слова?
- [ ] Указал риски и альтернативы?
- [ ] Есть следующие шаги?

## 9. Чего избегать / Что приветствуется

**Избегать:**
- Согласия ради согласия
- Общих фраз без конкретики
- Решений без анализа рисков
- Игнорирования компромиссов и trade-offs

**Приветствуется:**
- Конструктивная критика с аргументацией
- Альтернативные точки зрения
- Конкретные примеры и данные
- Указание источников и предположений
- Вопросы для уточнения контекста
"""

    return prompt

def generate_claude_md(role: str, vault_name: str, vault_path: str) -> str:
    """Генерировать CLAUDE.md с контекстом."""

    vault_dirs = [
        "00_CORE/{identity,stakeholders,strategy}",
        "10_PEOPLE/",
        "20_MEETINGS/{committees,standups}",
        "30_PROJECTS/{active,backlog,archive}",
        "40_DECISIONS/{adr,policies,journal}",
        "50_KNOWLEDGE/{methodologies,processes}",
        "60_DOMAIN/",
        "90_TEMPLATES/",
        "99_ARCHIVE/",
    ]

    # Mapping для slash-команд по ролям
    commands_map = {
        'CTO': '''
## Специфичные команды

| Команда | Действие |
|---------|----------|
| `/arch` | Обсудить архитектурные решения |
| `/tech-debt` | Анализ техдолга |
| `/incident` | Post-mortem анализ инцидента |
| `/roadmap` | Review технологического roadmap |
''',
        'CPO': '''
## Специфичные команды

| Команда | Действие |
|---------|----------|
| `/discovery` | Customer discovery session |
| `/prd` | Help с PRD и requirements |
| `/metrics` | Обсудить KPIs и метрики |
| `/backlog` | Prioritize backlog |
''',
        'COO': '''
## Специфичные команды

| Команда | Действие |
|---------|----------|
| `/process` | Optimize процессы |
| `/ops-review` | Operations review |
| `/metrics` | Dashboard и reporting |
| `/compliance` | Compliance checks |
''',
        'CFO': '''
## Специфичные команды

| Команда | Действие |
|---------|----------|
| `/budget` | Budget planning и tracking |
| `/forecast` | Financial forecasting |
| `/audit` | Audit preparation |
| `/metrics` | Financial metrics review |
''',
        'HR': '''
## Специфичные команды

| Команда | Действие |
|---------|----------|
| `/hiring` | Hiring process optimization |
| `/reviews` | Performance review guide |
| `/culture` | Culture assessment |
| `/learning` | Learning & development plan |
''',
        'PM': '''
## Специфичные команды

| Команда | Действие |
|---------|----------|
| `/planning` | Project planning |
| `/risks` | Risk assessment |
| `/status` | Project status review |
| `/stakeholders` | Stakeholder management |
''',
    }

    claude_md = f"""# CLAUDE.md для {role}

Создано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Контекст

**Роль:** {role}
**Vault:** {vault_name}
**Путь:** {vault_path}

## Структура базы знаний (Johnny Decimal)

```
{chr(10).join(vault_dirs)}
```

## Стандартные команды

| Команда | Действие |
|---------|----------|
| `/search <query>` | Семантический поиск по vault |
| `/context` | Загрузить всю базу в контекст |
| `/status` | Показать статус project |
| `/review` | Обзор документов |
| `/update` | Обновить документ |
| `/create` | Создать новый документ |

{commands_map.get(role, '')}

## Правила

1. **Контекст** — Всегда загружай из 00_CORE перед анализом
2. **Decisions** — Логируй в 40_DECISIONS/journal все важные решения
3. **Templates** — Используй шаблоны из 90_TEMPLATES
4. **Archive** — Перемещай старое в 99_ARCHIVE

## Search patterns

- `type:decision` — Только решения
- `type:meeting` — Только встречи
- `status:active` — Активные items
- `role:{role}` — Items для текущей роли
"""

    return claude_md

def save_configuration_file(vault_path: Path, config: Dict[str, str], logger: logging.Logger) -> bool:
    """Сохранить конфигурацию в config.json."""
    config_file = vault_path / ".executive-assistant" / "config.json"
    config_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f"Конфигурация сохранена в {config_file}")
        print_success(f"Конфигурация сохранена")
        return True
    except Exception as e:
        print_error(f"Ошибка при сохранении конфигурации: {e}")
        logger.error(f"Ошибка при сохранении конфигурации: {e}")
        return False

def run_child_script(script_name: str, args: List[str], logger: logging.Logger, scripts_dir: Path) -> bool:
    """Запустить дочерний скрипт."""
    script_path = scripts_dir / script_name

    if not script_path.exists():
        print_warning(f"Скрипт {script_name} не найден. Пропускаю.")
        logger.warning(f"Скрипт {script_name} не найден")
        return True

    try:
        print_info(f"Запускаю {script_name}...")
        cmd = [sys.executable, str(script_path)] + args
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print_success(f"{script_name} завершился успешно")
        logger.info(f"{script_name} завершился успешно")
        if result.stdout:
            logger.info(f"Вывод {script_name}: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Ошибка при запуске {script_name}: {e}")
        logger.error(f"Ошибка при запуске {script_name}: {e}")
        if e.stderr:
            logger.error(f"stderr: {e.stderr}")
        return False
    except Exception as e:
        print_error(f"Неожиданная ошибка при запуске {script_name}: {e}")
        logger.error(f"Неожиданная ошибка при запуске {script_name}: {e}")
        return False

def main():
    """Главная функция."""
    # Найти директорию скриптов
    scripts_dir = Path(__file__).parent
    vault_parent = scripts_dir.parent.parent.parent  # Перейти из scripts в root

    # Настроить логирование
    log_file = scripts_dir / f"install_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger = setup_logging(log_file)

    print_header("🚀 Executive Assistant Installation Orchestrator")
    print_info(f"Log файл: {log_file}")

    try:
        # 1. Собрать интерактивный ввод
        config = collect_user_input()
        logger.info(f"Конфигурация собрана: {config}")

        vault_path = Path(config['vault_path'])

        # 2. Создать структуру vault
        if not create_vault_structure(vault_path, config['role'], logger):
            print_error("Ошибка при создании структуры vault. Прерывание.")
            sys.exit(1)

        # 3. Генерировать SYSTEM_PROMPT.md
        print_info("Генерирую SYSTEM_PROMPT.md...")
        system_prompt = generate_system_prompt(
            config['role'],
            config['vault_name'],
            config['vault_path'],
            config['owner_name']
        )

        system_prompt_path = vault_path / ".executive-assistant" / "SYSTEM_PROMPT.md"
        system_prompt_path.parent.mkdir(parents=True, exist_ok=True)
        with open(system_prompt_path, 'w') as f:
            f.write(system_prompt)
        print_success(f"SYSTEM_PROMPT.md создан: {system_prompt_path}")
        logger.info(f"SYSTEM_PROMPT.md создан: {system_prompt_path}")

        # 4. Генерировать CLAUDE.md
        print_info("Генерирую CLAUDE.md...")
        claude_md = generate_claude_md(config['role'], config['vault_name'], config['vault_path'])

        claude_md_path = vault_path / ".executive-assistant" / "CLAUDE.md"
        with open(claude_md_path, 'w') as f:
            f.write(claude_md)
        print_success(f"CLAUDE.md создан: {claude_md_path}")
        logger.info(f"CLAUDE.md создан: {claude_md_path}")

        # 5. Сохранить конфигурацию
        if not save_configuration_file(vault_path, config, logger):
            print_warning("Конфигурация не сохранена. Продолжаю.")

        # 6. Запустить дочерние скрипты
        print_header("📦 Запуск вспомогательных скриптов")

        # 6.1 copy_aigrep_config.py
        if not run_child_script(
            'copy_aigrep_config.py',
            ['--vault-name', config['vault_name'], '--vault-path', config['vault_path']],
            logger,
            scripts_dir
        ):
            print_warning("copy_aigrep_config.py завершился с ошибкой")

        # 6.2 install_skills.py
        if not run_child_script(
            'install_skills.py',
            ['--vault-path', config['vault_path']],
            logger,
            scripts_dir
        ):
            print_warning("install_skills.py завершился с ошибкой")

        # 6.3 setup_mcp.py
        if not run_child_script(
            'setup_mcp.py',
            ['--vault-path', config['vault_path']],
            logger,
            scripts_dir
        ):
            print_warning("setup_mcp.py завершился с ошибкой")

        # 6.4 verify_installation.py
        if not run_child_script(
            'verify_installation.py',
            ['--vault-path', config['vault_path']],
            logger,
            scripts_dir
        ):
            print_warning("verify_installation.py завершился с ошибкой")

        # Финальное сообщение
        print_header("✅ Установка завершена")
        print_success(f"Ваш AI-ассистент {config['role']} готов к работе!")
        print_info(f"Vault расположен: {config['vault_path']}")
        print_info(f"Конфигурация: {vault_path / '.executive-assistant' / 'config.json'}")
        print_info(f"Логирование: {log_file}")

        logger.info("Установка завершена успешно")

    except KeyboardInterrupt:
        print_warning("\nУстановка отменена пользователем.")
        logger.warning("Установка отменена пользователем")
        sys.exit(0)
    except Exception as e:
        print_error(f"Критическая ошибка: {e}")
        logger.exception(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
