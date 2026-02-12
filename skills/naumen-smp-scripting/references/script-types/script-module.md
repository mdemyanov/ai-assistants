# Скрипт текста модуля (скриптовый модуль)

## Назначение

Универсальный переиспользуемый код — библиотека функций, вызываемых из любого скрипта SMP. Позволяет избежать дублирования, централизовать бизнес-логику, организовать код в модули.

## Место настройки

Администрирование → Скриптовые модули → Добавить / Редактировать

**Важно**: Код модуля используется для вызова: `modules.{код_модуля}.{метод}()`

## Контекстные переменные

| Переменная | Тип | Описание |
|------------|-----|----------|
| `user` | Object | Текущий пользователь (из вызывающего контекста) |
| `api` | Object | Доступ к API |
| `utils` | Object | Синоним api.utils |
| `modules` | Object | Доступ к другим модулям |
| `logger` | Object | Логирование |

**Важно**: `user` передается из вызывающего скрипта. Из действий по событию нужно передавать явно.

## Структура модуля

```groovy
// Модуль с кодом "myUtils"

//ПАРАМЕТРЫ------------------------------------------------------------
def DEFAULT_STATE = 'registered'

//ФУНКЦИИ--------------------------------------------------------------
/**
 * Находит запросы пользователя в указанном статусе
 * @param employee Сотрудник
 * @param state Код статуса (опционально)
 * @return Список запросов
 */
def findUserRequests(employee, state = DEFAULT_STATE) {
    if (!employee) return []

    return utils.find('serviceCall', [
        'clientEmployee': employee.UUID,
        'state': state
    ], sp.limit(100))
}

/**
 * Проверяет, является ли сотрудник VIP
 * @param employee Сотрудник
 * @return true если VIP
 */
def isVipEmployee(employee) {
    if (!employee) return false
    return employee.vipStatus == true
}

/**
 * Создает стандартный комментарий
 * @param sc Запрос
 * @param text Текст
 * @param author Автор (опционально)
 */
def addComment(sc, text, author = null) {
    utils.create('comment', [
        'source': sc.UUID,
        'text': text,
        'author': author?.UUID
    ])
}
```

## Вызов из других скриптов

```groovy
// Из действия по событию
def requests = modules.myUtils.findUserRequests(subject.clientEmployee)

// Проверка VIP
if (modules.myUtils.isVipEmployee(subject.clientEmployee)) {
    // Особая обработка
}

// Добавление комментария с передачей user
modules.myUtils.addComment(subject, "Обработано автоматически", user)
```

## Класс-модуль (для режима компиляции All)

```groovy
// Модуль с кодом "Bar"
class Bar extends Script {

    Bar() {
        this(new Binding([:]))
    }

    Bar(Binding binding) {
        super(binding)
    }

    Object run() {
        return null
    }

    def sum(a, b) {
        return a + b
    }

    def multiply(a, b) {
        return a * b
    }
}
```

## Чек-лист проверок

### Структура
- [ ] Код модуля = имя класса (для режима All)
- [ ] Класс extends Script (для режима All)
- [ ] Документация методов (JSDoc)

### Безопасность
- [ ] Явная передача user из действий по событию
- [ ] Проверка входных параметров
- [ ] Обработка null значений

### Производительность
- [ ] Нет @Field с вызовами API
- [ ] Кэширование тяжелых операций
- [ ] Параметры по умолчанию

## Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| Модуль не найден | Код модуля ≠ имени класса | Синхронизировать имена |
| user = null | Не передан из действия по событию | Передавать явно как параметр |
| Ошибка компиляции | @Field с utils.get | Убрать обращения к API из @Field |
| Зацикливание | Взаимные вызовы модулей | Проверить зависимости |

## Особенности

1. **Режимы компиляции**: OneByOne (независимо) или All (вместе). Настройка в dbaccess.properties.

2. **Передача user**: Из действий по событию user не передается автоматически — нужно передавать явно.

3. **Вызов между модулями**: Можно вызывать методы одного модуля из другого.

4. **@Field запрещен с API**: `@Field String x = utils.get(...)` вызывает ошибку.

## Примеры

### Модуль для работы с SLA
```groovy
// Модуль: slaHelper

def calculateDeadline(sc) {
    def service = sc.service
    if (!service?.slaHours) return null

    def hours = service.slaHours
    return api.timing.serviceTime(
        service.calendar,
        sc.clientEmployee?.city?.timeZone,
        sc.creationDate,
        hours * 60 * 60 * 1000  // часы в мс
    )
}

def isOverdue(sc) {
    def deadline = sc.deadline ?: calculateDeadline(sc)
    return deadline && deadline < new Date()
}
```

### Модуль интеграции
```groovy
// Модуль: externalApi

def API_URL = 'https://api.external.com'

def sendToExternal(sc, usr) {
    def data = [
        'id': sc.number,
        'title': sc.title,
        'user': usr?.login
    ]

    try {
        return api.http.postJSON("${API_URL}/tickets", data, [
            'Authorization': getToken()
        ])
    } catch (e) {
        logger.error("External API error: ${e.message}")
        return null
    }
}

private def getToken() {
    // Логика получения токена
    return 'Bearer xxx'
}
```
