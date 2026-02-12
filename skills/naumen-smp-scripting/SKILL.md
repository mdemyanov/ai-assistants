---
name: naumen-smp-scripting
description: >
  Разработка Groovy-скриптов для Naumen SMP. Используй когда пользователь:
  просит написать скрипт SMP, спрашивает про API методы (utils.find, api.http,
  api.db.query), нужна помощь с действиями по событиям, вычислимыми атрибутами,
  фильтрацией, интеграциями, отладкой скриптов, рефакторингом устаревших методов.
  Триггеры: "напиши скрипт", "метод API", "действие по событию", "HQL запрос",
  "utils.", "api.", "subject", "oldSubject", "Groovy SMP", "Naumen скрипт".
---

# Naumen SMP Scripting

Помощь в разработке Groovy-скриптов для Naumen SMP: генерация, отладка, рефакторинг, подбор API.

## Workflow

### 1. Определи тип задачи

| Запрос | Действие |
|--------|----------|
| Написать скрипт | Генерация |
| Найти метод API | Подбор API |
| Объяснить код | Анализ |
| Улучшить скрипт | Рефакторинг |
| Исправить ошибку | Отладка |
| Проверить код | Валидация |

### 2. Генерация скрипта

1. **Определи тип скрипта** → загрузи спецификацию из `references/script-types/`:
   - Фильтрация → `filter-script.md`
   - Вычислимый атрибут → `computed-attribute.md`
   - Значение по умолчанию → `default-value.md`
   - Действие по событию (системное) → `event-action-system.md`
   - Действие по событию (пользовательское) → `event-action-user.md`
   - Действие при входе/выходе из статуса → `status-action.md`
   - Скрипт условия → `condition-script.md`
   - Задача планировщика → `scheduler-task.md`
   - Конфигурация импорта → `import-config.md`
   - Обработка почты → `mail-processing.md`
   - Шаблон отчёта → `report-template.md`
   - Скриптовой модуль → `script-module.md`
   - Определение прав доступа → `access-rights.md`

2. **Уточни контекст:**
   - Синхронный/асинхронный
   - Какие данные на входе (subject, params, form...)

3. **Выбери паттерн** из `references/patterns-antipatterns.md`

4. **Собери методы API:**
   - Сначала проверь Quick Reference ниже
   - Если не нашел — `references/api-quick-ref.md`
   - Для редких методов — поиск в полной документации

5. **Напиши код** по структуре:
```groovy
//ПАРАМЕТРЫ------------------------------------------------------------
def PARAM_NAME = 'value' // Комментарий параметра

//ФУНКЦИИ--------------------------------------------------------------
def myFunction(arg) {
    // логика
}

//ОСНОВНОЙ БЛОК--------------------------------------------------------
// Основная логика здесь
```

6. **Добавь обработку ошибок** (null-safety, try-catch)

7. **Проверь по чек-листу** `references/validation-checklist.md`

### 3. Подбор методов API (Quick Reference)

| Задача | Метод |
|--------|-------|
| Найти один объект | `utils.get('fqn', [:])` или `utils.load('uuid')` |
| Найти несколько | `utils.find('fqn', attrs)` + `sp.limit()` |
| Найти первый | `utils.findFirst('fqn', attrs)` |
| Подсчитать | `utils.count('fqn', attrs)` |
| Создать объект | `utils.create('fqn', attrs)` |
| Редактировать | `utils.edit(obj, attrs)` |
| Удалить | `utils.delete(obj)` |
| HTTP GET | `api.http.getJSON(url, headers)` |
| HTTP POST | `api.http.postJSON(url, data, headers)` |
| HQL запрос | `api.db.query('from Class').list()` |
| Дата + N дней | `api.date.addDays(date, n)` |
| Форматировать дату | `utils.formatters.dateToStr(date, 'dd.MM.yyyy')` |
| Парсить дату | `utils.formatters.strToDate(str, 'yyyy-MM-dd')` |

**Детали:** `references/api-quick-ref.md`

### 4. Условные операции (op.*)

```groovy
op.like('%value%')     // Поиск по вхождению
op.eq(value)           // Равно
op.not(value)          // Не равно (включая null!)
op.in(v1, v2, v3)      // Входит в список
op.orEq(v1, v2)        // Равно одному из (минимум 2)
op.gt(value)           // Больше
op.lt(value)           // Меньше
op.between(v1, v2)     // Диапазон (включительно)
op.isNull()            // Пустое значение
op.isNotNull()         // Не пустое
```

### 5. Контекстные переменные

**Глобальные (все скрипты):**
- `user` — пользователь, инициировавший событие (employee, может быть null)
- `ip` — IP-адрес пользователя
- `api` — доступ к методам API
- `utils` — синоним api.utils
- `modules` — доступ к скриптовым модулям
- `logger` — логирование (info/debug/warn/error)

**Действия по событию (системные):**
- `subject` — текущий объект (может быть null при удалении)
- `oldSubject` — объект до изменения (null при добавлении)
- `currentSubject` — актуальное состояние после предыдущих действий
- `changedAttributes` — список кодов измененных атрибутов
- `sourceObject` — добавленный файл/комментарий
- `cardObject` — объект карточки (null если не из карточки)

**Действия по событию (пользовательские):**
- `subjects` — выбранные объекты
- `subject` — произвольный из subjects
- `params` — параметры с формы
- `result` — управление результатом (showMessage, goToUrl...)
- `source` — откуда вызвано (OBJECT_LIST/OBJECT_CARD)

**Вычисление атрибутов:**
- `subject` — редактируемый объект
- `form` — значения на форме
- `origin` — тип формы (readForm/addForm/editForm)

**Полный список:** `references/script-categories.md`

### 6. Отладка

**Типичные ошибки:**

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `No signature of method` | Неверные параметры | Проверь типы аргументов |
| `NullPointerException` | Обращение к null | Добавь `?.` или проверку |
| `Many objects in result` | `utils.get` нашел несколько | Используй `utils.findFirst` |
| `Could not resolve property` | Вычислимый атрибут в поиске | Не использовать в utils.find |
| `Could not extract ResultSet` | Пустой список в HQL IN | Проверка `if (list)` |
| `PersistenceContext limit exceeded` | >50000 объектов | Делить на части, sp.limit() |

**Логирование:**
```groovy
logger.info("Debug: value=${variable}")
logger.error("Error: ${e.message}")
logger.debug("Detailed: ${obj.dump()}")
```

**Детали:** `references/patterns-antipatterns.md`

## Антипаттерны (ИЗБЕГАТЬ)

1. **Множественные edit** — объединяй в один вызов
```groovy
// ПЛОХО
utils.edit(subject, ['attr1': v1])
utils.edit(subject, ['attr2': v2])

// ХОРОШО
utils.edit(subject, ['attr1': v1, 'attr2': v2])
```

2. **utils.find без limit** при большом количестве — добавь `sp.limit()`

3. **Вычислимый атрибут в utils.find** — не работает, используй HQL или системные атрибуты

4. **subject.UUID на null** — проверяй `subject?.UUID`

5. **Строка вместо UUID для ссылки:**
```groovy
// ОШИБКА
utils.find('catalogs$bu', ['item': 'Телефон'])

// РЕШЕНИЕ
utils.find('catalogs$bu', ['item': 'item$2353453'])
```

6. **Пустой список в HQL IN:**
```groovy
// ОШИБКА
api.db.query('...WHERE id in (:list)').set('list', []).list()

// РЕШЕНИЕ
if (list) { api.db.query('...').set('list', list).list() }
```

## Ресурсы

- `references/script-types/` — **спецификации по типам скриптов** (13 типов)
- `references/validation-checklist.md` — **чек-лист проверок** (производительность, безопасность, корректность)
- `references/api-quick-ref.md` — ТОП-20 методов с примерами
- `references/script-categories.md` — категории скриптов и переменные
- `references/patterns-antipatterns.md` — паттерны и типовые ошибки
- `references/api-search-guide.md` — поиск в полной документации API
- `references/examples/` — готовые примеры по категориям

**Полная документация API:**
`/Users/mdemyanov/Devel/naumen-ecosystem/naumen-smp/script/metody-api.md` (575KB)

**Категории скриптов:**
`/Users/mdemyanov/Devel/naumen-ecosystem/naumen-smp/script/kategorii-skriptov.md`
