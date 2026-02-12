# Скрипт задачи планировщика

## Назначение

Выполняет автоматические действия по расписанию без участия пользователя. Используется для регулярных отчетов, синхронизации данных, очистки устаревших объектов, массовых обновлений, интеграций.

## Место настройки

Администрирование → Планировщик → Добавить задачу → Тип: Скрипт

## Контекстные переменные

| Переменная | Тип | Описание |
|------------|-----|----------|
| `currentTaskInfo` | Object | Информация о текущей задаче планировщика |
| `user` | Object | null (системное выполнение) |
| `api`, `utils` | Object | Доступ к API |
| `modules` | Object | Доступ к модулям |
| `logger` | Object | Логирование |

### Методы currentTaskInfo

| Метод | Описание |
|-------|----------|
| `getCode()` | UUID задачи |
| `getTitle()` | Название задачи |
| `getDescription()` | Описание задачи |
| `getLastExecutionDate()` | Дата последнего выполнения |
| `getPlanDate()` | Дата следующего запуска |
| `getTrigger()` | Правила выполнения |

## Шаблон

```groovy
//ПАРАМЕТРЫ------------------------------------------------------------
def BATCH_SIZE = 500
def DAYS_TO_ARCHIVE = 90
def LOG_PREFIX = "[ArchiveTask]"

//ФУНКЦИИ--------------------------------------------------------------
def log(message) {
    logger.info("${LOG_PREFIX} ${message}")
}

//ОСНОВНОЙ БЛОК--------------------------------------------------------
log("Запуск задачи: ${currentTaskInfo.getTitle()}")
def startTime = System.currentTimeMillis()

def archiveDate = api.date.addDays(new Date(), -DAYS_TO_ARCHIVE)
def processed = 0
def offset = 0

while (true) {
    def batch = utils.find('serviceCall', [
        'state': 'closed',
        'closedDate': op.lt(archiveDate)
    ], sp.limit(BATCH_SIZE).offset(offset))

    if (!batch) break

    batch.each { sc ->
        try {
            utils.edit(sc, ['archived': true])
            processed++
        } catch (Exception e) {
            log("Ошибка обработки ${sc.number}: ${e.message}")
        }
    }

    offset += BATCH_SIZE
    log("Обработано: ${processed}")
}

def duration = (System.currentTimeMillis() - startTime) / 1000
log("Завершено. Обработано: ${processed}, время: ${duration}с")
```

## Доступные API

### Полностью доступны
- `utils.find`, `utils.findFirst`, `utils.count`, `utils.get`
- `utils.create`, `utils.edit`, `utils.delete`
- `api.http.*`, `api.soap.*`
- `api.mail.sendMail`, `api.mail.sender`
- `api.reports.getReportDataSource`
- `api.db.query` (HQL)

## Чек-лист проверок

### Производительность
- [ ] Батчевая обработка больших объемов данных
- [ ] Лимиты `sp.limit()` для всех utils.find
- [ ] Планирование на ночное время / выходные

### Надежность
- [ ] try-catch для каждой итерации (ошибка одного не ломает все)
- [ ] Логирование начала, прогресса и завершения
- [ ] Логирование ошибок с идентификаторами объектов

### Мониторинг
- [ ] Подсчет обработанных/ошибочных записей
- [ ] Замер времени выполнения
- [ ] Алерты при критических ошибках (email)

## Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `PersistenceContext limit exceeded` | >50000 объектов без батчинга | Батчевая обработка |
| Таймаут задачи | Слишком долгое выполнение | Разбить на подзадачи |
| user = null | Системный контекст | Не полагаться на user |
| Повторное выполнение | Задача не учитывает уже обработанные | Добавить флаг/дату обработки |

## Особенности

1. **user = null**: Задачи выполняются в системном контексте. Нет текущего пользователя.

2. **Тяжелые операции**: Планируйте на ночь/выходные. Используйте батчинг.

3. **Идемпотентность**: Задача может запуститься повторно — учитывайте в логике.

4. **Логирование**: Обязательно логируйте — единственный способ понять что происходит.

## Примеры

### Ежедневный отчет по email
```groovy
def TEMPLATE_CODE = 'dailyReport'
def REPORT_PARAMS = ['DateFrom': new Date()-1, 'DateTo': new Date()]
def SUBJECT_UUID = 'root$101'
def RECIPIENTS = [
    ['name': 'Администратор', 'email': 'admin@example.com']
]

def message = api.mail.sender.createMail()
RECIPIENTS.each { r ->
    message.addTo(r.name, r.email)
}
message.contentType = 'text/html'
message.setSubject("Ежедневный отчет за ${new Date().format('dd.MM.yyyy')}")
message.setText("Отчет во вложении")

def source = api.reports.getReportDataSource(TEMPLATE_CODE, SUBJECT_UUID, REPORT_PARAMS, 'pdf')
message.attachFile(source, "report_${new Date().format('yyyyMMdd')}.pdf")

api.mail.sender.sendMail(message)
logger.info("Отчет отправлен")
```

### Синхронизация с внешней системой
```groovy
def SYNC_URL = 'https://api.external.com/updates'
def LAST_SYNC_CONFIG = 'lastSyncTimestamp'

def config = utils.findFirst('systemConfig', ['code': LAST_SYNC_CONFIG])
def lastSync = config?.value ?: '1970-01-01T00:00:00Z'
def currentTime = new Date().format("yyyy-MM-dd'T'HH:mm:ss'Z'")

try {
    def response = api.http.getJSON("${SYNC_URL}?since=${lastSync}", null)

    response?.items?.each { item ->
        def existing = utils.findFirst('serviceCall', ['externalId': item.id])
        if (existing) {
            utils.edit(existing, ['title': item.title, 'state': item.status])
        }
    }

    if (config) {
        utils.edit(config, ['value': currentTime])
    }

    logger.info("Синхронизация завершена. Обновлено: ${response?.items?.size() ?: 0}")
} catch (Exception e) {
    logger.error("Ошибка синхронизации: ${e.message}")
}
```

→ См. [examples/integrations.groovy](../examples/integrations.groovy) (пример 5)
