// =============================================================================
// ПРИМЕРЫ: Скрипты интеграций (HTTP, SOAP, внешние системы)
// =============================================================================

// -----------------------------------------------------------------------------
// Пример 1: HTTP GET запрос
// Категория: Действие по событию / Задача планировщика
// Использование: Получение данных из внешней системы
// -----------------------------------------------------------------------------
//ПАРАМЕТРЫ------------------------------------------------------------
def API_URL = 'https://api.example.com/users'
def API_TOKEN = 'Bearer your-token-here'

//ОСНОВНОЙ БЛОК--------------------------------------------------------
try {
    def response = api.http.getJSON(
        API_URL,
        ['Authorization': API_TOKEN]
    )

    if (response) {
        logger.info("Получено записей: ${response.size()}")
        return response
    }
} catch (Exception e) {
    logger.error("Ошибка HTTP GET: ${e.message}")
}

return null

// -----------------------------------------------------------------------------
// Пример 2: HTTP POST запрос с данными
// Категория: Действие по событию
// Использование: Отправка данных во внешнюю систему
// -----------------------------------------------------------------------------
//ПАРАМЕТРЫ------------------------------------------------------------
def API_URL = 'https://api.example.com/tickets'
def API_KEY = 'your-api-key'

//ОСНОВНОЙ БЛОК--------------------------------------------------------
def requestData = [
    'title': subject.title,
    'description': subject.description,
    'priority': subject.urgency?.code ?: 'normal',
    'author': subject.author?.email,
    'createdAt': utils.formatters.dateToStr(new Date(), 'yyyy-MM-dd HH:mm:ss')
]

try {
    def response = api.http.postJSON(
        API_URL,
        requestData,
        [
            'Authorization': "ApiKey ${API_KEY}",
            'Content-Type': 'application/json'
        ]
    )

    if (response?.id) {
        // Сохраняем ID из внешней системы
        utils.edit(subject, ['externalId': response.id.toString()])
        logger.info("Создан тикет во внешней системе: ${response.id}")
    }
} catch (Exception e) {
    logger.error("Ошибка HTTP POST: ${e.message}")
    throw e // Откатить транзакцию при ошибке
}

// -----------------------------------------------------------------------------
// Пример 3: HTTP PUT для обновления данных
// Категория: Действие по событию
// Использование: Синхронизация изменений с внешней системой
// -----------------------------------------------------------------------------
//ПАРАМЕТРЫ------------------------------------------------------------
def API_BASE_URL = 'https://api.example.com/tickets'

//ОСНОВНОЙ БЛОК--------------------------------------------------------
def externalId = subject.externalId
if (!externalId) {
    logger.warn("Нет externalId для синхронизации")
    return
}

def updateData = [
    'status': subject.state,
    'assignee': subject.responsibleEmployee?.email,
    'updatedAt': utils.formatters.dateToStr(new Date(), 'yyyy-MM-dd HH:mm:ss')
]

try {
    def response = api.http.putJSON(
        "${API_BASE_URL}/${externalId}",
        updateData,
        ['Authorization': 'Bearer token']
    )

    logger.info("Обновлен тикет: ${externalId}")
} catch (Exception e) {
    logger.error("Ошибка обновления: ${e.message}")
}

// -----------------------------------------------------------------------------
// Пример 4: Обработка webhook от внешней системы
// Категория: REST API endpoint (требует настройки в SMP)
// Использование: Прием данных от внешних систем
// -----------------------------------------------------------------------------
//ПАРАМЕТРЫ------------------------------------------------------------
def EXTERNAL_ID_ATTR = 'externalId'
def STATUS_MAPPING = [
    'open': 'registered',
    'in_progress': 'inProgress',
    'resolved': 'resolved',
    'closed': 'closed'
]

//ОСНОВНОЙ БЛОК--------------------------------------------------------
// params содержит данные из webhook
def externalId = params.ticketId
def newStatus = params.status

if (!externalId) {
    logger.warn("Webhook без ticketId")
    return [success: false, error: 'Missing ticketId']
}

def ticket = utils.findFirst('serviceCall', ["${EXTERNAL_ID_ATTR}": externalId])
if (!ticket) {
    logger.warn("Не найден объект с externalId: ${externalId}")
    return [success: false, error: 'Ticket not found']
}

def mappedStatus = STATUS_MAPPING[newStatus]
if (mappedStatus && ticket.state != mappedStatus) {
    utils.edit(ticket, ['state': mappedStatus])
    logger.info("Обновлен статус ${ticket.number}: ${mappedStatus}")
}

return [success: true, ticketNumber: ticket.number]

// -----------------------------------------------------------------------------
// Пример 5: Периодическая синхронизация (планировщик)
// Категория: Скрипт задачи планировщика
// Использование: Регулярная синхронизация данных
// -----------------------------------------------------------------------------
//ПАРАМЕТРЫ------------------------------------------------------------
def SYNC_URL = 'https://api.example.com/updates'
def LAST_SYNC_CONFIG = 'lastSyncTimestamp'
def BATCH_SIZE = 100

//ФУНКЦИИ--------------------------------------------------------------
def getLastSyncTime() {
    // Получить из конфигурации или использовать дефолт
    def config = utils.findFirst('systemConfig', ['code': LAST_SYNC_CONFIG])
    return config?.value ?: '1970-01-01T00:00:00Z'
}

def saveLastSyncTime(timestamp) {
    def config = utils.findFirst('systemConfig', ['code': LAST_SYNC_CONFIG])
    if (config) {
        utils.edit(config, ['value': timestamp])
    }
}

//ОСНОВНОЙ БЛОК--------------------------------------------------------
def lastSync = getLastSyncTime()
def currentTime = utils.formatters.dateToStr(new Date(), "yyyy-MM-dd'T'HH:mm:ss'Z'")

try {
    def response = api.http.getJSON(
        "${SYNC_URL}?since=${lastSync}&limit=${BATCH_SIZE}",
        ['Authorization': 'Bearer token']
    )

    def processed = 0
    response?.items?.each { item ->
        // Обработка каждого элемента
        def existing = utils.findFirst('serviceCall', ['externalId': item.id])
        if (existing) {
            utils.edit(existing, ['title': item.title, 'state': item.status])
        }
        processed++
    }

    saveLastSyncTime(currentTime)
    logger.info("Синхронизация завершена. Обработано: ${processed}")

} catch (Exception e) {
    logger.error("Ошибка синхронизации: ${e.message}")
}

// -----------------------------------------------------------------------------
// Пример 6: Multipart form-data (загрузка файлов)
// Категория: Действие по событию
// Использование: Отправка файлов во внешнюю систему
// -----------------------------------------------------------------------------
//ПАРАМЕТРЫ------------------------------------------------------------
def UPLOAD_URL = 'https://api.example.com/upload'

//ОСНОВНОЙ БЛОК--------------------------------------------------------
def files = subject.getFiles()
if (!files) {
    logger.info("Нет файлов для загрузки")
    return
}

files.each { file ->
    try {
        def publisher = api.http.getBodyPublishers().ofFormData()
        publisher.addText('ticketId', subject.externalId)
        publisher.addText('fileName', file.title)
        publisher.addStream('file', file.title, { -> new ByteArrayInputStream(file.getBytes()) })

        // Примечание: для отправки multipart требуется java.net.http.HttpClient
        // Этот пример показывает подготовку данных

        logger.info("Подготовлен файл для загрузки: ${file.title}")
    } catch (Exception e) {
        logger.error("Ошибка подготовки файла ${file.title}: ${e.message}")
    }
}

// -----------------------------------------------------------------------------
// Пример 7: Проверка доступности внешней системы
// Категория: Скрипт условия действия
// Использование: Проверка перед интеграцией
// -----------------------------------------------------------------------------
//ПАРАМЕТРЫ------------------------------------------------------------
def HEALTH_CHECK_URL = 'https://api.example.com/health'
def TIMEOUT_MS = 3000

//ОСНОВНОЙ БЛОК--------------------------------------------------------
try {
    def response = api.http.getJSON(HEALTH_CHECK_URL, null)
    return response?.status == 'ok'
} catch (Exception e) {
    logger.warn("Внешняя система недоступна: ${e.message}")
    return false
}
