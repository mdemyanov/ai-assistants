# Скрипт правила обработки входящей почты

## Назначение

Обрабатывает входящие email-сообщения: создает запросы, добавляет комментарии, прикрепляет файлы. Выполняется по расписанию задачи планировщика "Обработка входящей почты".

## Место настройки

Администрирование → Обработка почты → Правила обработки → Добавить

## Контекстные переменные

| Переменная | Тип | Описание |
|------------|-----|----------|
| `message` | Object | Разобранное почтовое сообщение |
| `result` | Object | Результат обработки (можно получить/установить) |
| `incomingServer` | String | Код подключения к серверу входящей почты |
| `api` | Object | API для работы с почтой |
| `utils` | Object | Стандартные утилиты |
| `logger` | Object | Логгер |

### Свойства message

| Свойство | Тип | Описание |
|----------|-----|----------|
| `message.from` | String | Email отправителя |
| `message.subject` | String | Тема письма |
| `message.body` | String | Текст письма (plain text) |
| `message.htmlBody` | String | HTML-содержимое письма |
| `message.sentDate` | Date | Дата отправки |
| `message.attachments` | List | Вложения |

## Коды результата

| Код | Описание |
|-----|----------|
| `NEW_BO` | Зарегистрирован новый запрос |
| `ATTACH` | Письмо прикреплено к существующему запросу |
| `REJECT` | Письмо отклонено |
| `ERROR` | Ошибка обработки |

## Шаблон

```groovy
//ПАРАМЕТРЫ------------------------------------------------------------
def SEARCH_PREFIX = "REQ-"
def DEFAULT_TYPE = "serviceCall$request"
def AGREEMENT_UUID = "agreement$1001"

//ФУНКЦИИ--------------------------------------------------------------
def findScByNumber(number) {
    return utils.findFirst('serviceCall', ['number': number])
}

def extractNumber(subject) {
    def match = subject =~ /${SEARCH_PREFIX}(\d+)/
    return match ? match[0][1] : null
}

//ОСНОВНОЙ БЛОК--------------------------------------------------------
// Проверки
if (!message.subject?.trim()) {
    result.setCode('REJECT')
    result.setMessage("Письмо без темы отклонено")
    return
}

// Поиск запроса по номеру в теме
def number = extractNumber(message.subject)
def sc = number ? findScByNumber(number) : null

if (sc) {
    // Добавить комментарий к существующему запросу
    utils.create('comment', [
        'source': sc.UUID,
        'text': message.body ?: message.htmlBody,
        'author': findEmployeeByEmail(message.from)
    ])

    // Прикрепить вложения
    message.attachments?.each { att ->
        api.utils.attachFile(sc, att)
    }

    result.setCode('ATTACH')
    result.setMessage("Прикреплено к ${sc.number}")
} else {
    // Создать новый запрос
    def newSc = utils.create(DEFAULT_TYPE, [
        'title': message.subject,
        'description': message.body,
        'agreement': AGREEMENT_UUID
    ])

    result.setCode('NEW_BO')
    result.setMessage("Создан запрос ${newSc.number}")
}
```

## Доступные API

### Полностью доступны
- `utils.find`, `utils.findFirst`, `utils.create`, `utils.edit`
- `api.utils.attachFile`
- `api.mail.helper.*` — вспомогательные методы для почты

### Особые методы
- `api.mail.helper.replaceReferencesToAttachments(message)` — замена ссылок на вложения

## Чек-лист проверок

### Валидация
- [ ] Проверка наличия темы письма
- [ ] Проверка наличия тела письма
- [ ] Проверка на уже обработанные письма

### Безопасность
- [ ] Валидация email отправителя
- [ ] Проверка размера вложений
- [ ] Защита от спама/флуда

### Надежность
- [ ] Установка result.setCode для всех веток
- [ ] Логирование ошибок
- [ ] Обработка исключений

## Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| Письма не обрабатываются | Не настроена задача планировщика | Создать задачу "Обработка входящей почты" |
| Потеря вложений | Не включено "Сохранять исходное письмо" | Включить в настройках задачи |
| Дублирование запросов | Нет проверки по message-id | Добавить проверку уникальности |

## Особенности

1. **Модуль обработки**: Рекомендуется использовать `modules.mail.init(binding)` для стандартной логики.

2. **Задача планировщика**: Скрипт вызывается из задачи "Обработка входящей почты" по расписанию.

3. **Сохранение письма**: Включите "Сохранять исходное письмо после обработки" для доступа к вложениям.

## Примеры

### Поиск сотрудника по email
```groovy
def findEmployeeByEmail(email) {
    if (!email) return null
    return utils.findFirst('employee', ['email': email?.toLowerCase()])
}
```

### Создание запроса с вложениями
```groovy
def sc = utils.create('serviceCall$request', [
    'title': message.subject,
    'description': message.body
])

message.attachments?.each { att ->
    api.utils.attachFile(sc, att.inputStream, att.fileName)
}

result.setCode('NEW_BO')
```
