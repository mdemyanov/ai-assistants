// =============================================================================
// ПРИМЕРЫ: Скрипты фильтрации
// =============================================================================

// -----------------------------------------------------------------------------
// Пример 1: Базовая фильтрация по связанному объекту
// Категория: Скрипт фильтрации значений атрибута при редактировании
// Место: Администрирование → Атрибуты → Скрипт фильтрации
// -----------------------------------------------------------------------------
// Часть 1: Определение зависимых атрибутов (выполняется в админке)
def DEPENDENT_ATTRS = ['clientEmployee', 'clientOU']
if (subject == null) {
    return DEPENDENT_ATTRS
}

// Часть 2: Фильтрация услуг по клиенту
def client = form?.clientEmployee?.parent ?: form?.clientOU
if (!client) {
    return api.filtration.disableFiltration()
}

return utils.find('service', ['clients': op.in(client)])

// -----------------------------------------------------------------------------
// Пример 2: Фильтрация с несколькими условиями
// Категория: Скрипт фильтрации значений атрибута
// Использование: Фильтрация ответственных по услуге и отделу
// -----------------------------------------------------------------------------
// Часть 1: Зависимые атрибуты
def DEPENDENT_ATTRS = ['service', 'clientOU']
if (subject == null) {
    return DEPENDENT_ATTRS
}

// Часть 2: Фильтрация
def service = form?.service ?: subject?.service
def clientOU = form?.clientOU ?: subject?.clientOU

if (!service) {
    return api.filtration.disableFiltration()
}

// Находим сотрудников, которые могут быть ответственными по услуге
def serviceTeams = service.responsibleTeams ?: []
def serviceEmployees = service.responsibleEmployees ?: []

def employees = []

// Добавляем сотрудников из команд
serviceTeams.each { team ->
    employees.addAll(utils.find('employee', ['teams': op.in(team.UUID)]))
}

// Добавляем прямо указанных сотрудников
employees.addAll(serviceEmployees)

if (!employees) {
    return api.filtration.disableFiltration()
}

return employees.unique { it.UUID }

// -----------------------------------------------------------------------------
// Пример 3: Фильтрация статусов
// Категория: Скрипт фильтрации статусов
// Место: Администрирование → Атрибуты (state) → Скрипт фильтрации
// -----------------------------------------------------------------------------
//ПАРАМЕТРЫ------------------------------------------------------------
// Статусы, доступные для выбора из каждого текущего статуса
def ALLOWED_TRANSITIONS = [
    'registered': ['assigned', 'inProgress', 'cancelled'],
    'assigned': ['inProgress', 'registered', 'cancelled'],
    'inProgress': ['pending', 'resolved', 'assigned'],
    'pending': ['inProgress', 'resolved'],
    'resolved': ['closed', 'inProgress'],
    'closed': [] // Закрытый нельзя переоткрыть
]

//ОСНОВНОЙ БЛОК--------------------------------------------------------
def currentState = subject?.state

if (!currentState) {
    // Для нового объекта - только начальные статусы
    return utils.find('status', ['code': op.in('registered', 'assigned')])
}

def allowedCodes = ALLOWED_TRANSITIONS[currentState] ?: []

if (!allowedCodes) {
    return []
}

return utils.find('status', ['code': op.in(allowedCodes)])

// -----------------------------------------------------------------------------
// Пример 4: Фильтрация с проверкой прав
// Категория: Скрипт фильтрации значений атрибута
// Использование: Показывать только объекты, на которые есть права
// -----------------------------------------------------------------------------
// Часть 1
if (subject == null) {
    return ['parentOU']
}

// Часть 2: Фильтрация отделов, доступных пользователю
def userOU = user?.parent
if (!userOU) {
    return api.filtration.disableFiltration()
}

// Находим все дочерние отделы пользователя
def childOUs = utils.find('ou', ['parent': userOU.UUID])
def result = [userOU] + childOUs

return result

// -----------------------------------------------------------------------------
// Пример 5: Динамическая фильтрация по типу объекта
// Категория: Скрипт фильтрации значений атрибута
// Использование: Разные списки для разных типов объектов
// -----------------------------------------------------------------------------
// Часть 1
if (subject == null) {
    return []
}

// Часть 2
def metaClass = form?.metaClass?.toString() ?: subject?.getMetainfo()?.toString()

switch (metaClass) {
    case 'serviceCall$incident':
        // Для инцидентов - только технические услуги
        return utils.find('service', ['category': 'technical'])

    case 'serviceCall$request':
        // Для запросов - все услуги
        return api.filtration.disableFiltration()

    case 'serviceCall$change':
        // Для изменений - только бизнес-услуги
        return utils.find('service', ['category': 'business'])

    default:
        return api.filtration.disableFiltration()
}

// -----------------------------------------------------------------------------
// Пример 6: Фильтрация элементов справочника
// Категория: Скрипт фильтрации значений атрибута
// Использование: Каскадная фильтрация справочников
// -----------------------------------------------------------------------------
// Часть 1: Зависимость от родительского справочника
if (subject == null) {
    return ['parentCategory']
}

// Часть 2: Фильтрация подкатегорий по выбранной категории
def parentCategory = form?.parentCategory
if (!parentCategory) {
    // Если родитель не выбран - показать корневые элементы
    return utils.find('category', ['parent': op.isNull()])
}

// Показать только дочерние элементы выбранной категории
return utils.find('category', ['parent': parentCategory.UUID])

// -----------------------------------------------------------------------------
// Пример 7: Фильтрация с учетом даты
// Категория: Скрипт фильтрации значений атрибута
// Использование: Показывать только актуальные элементы
// -----------------------------------------------------------------------------
// Часть 1
if (subject == null) {
    return []
}

// Часть 2: Только активные соглашения на текущую дату
def today = new Date().clearTime()

return utils.find('agreement', [
    'startDate': op.lt(today),
    'endDate': op.gt(today),
    'status': 'active'
])

// -----------------------------------------------------------------------------
// Пример 8: Ограничение дат (минимум/максимум)
// Категория: Скрипт ограничения значений атрибутов типа "Дата"
// Место: Администрирование → Атрибуты → Ограничение значений
// -----------------------------------------------------------------------------
//ПАРАМЕТРЫ------------------------------------------------------------
def MIN_DAYS = 0    // Не раньше сегодня
def MAX_DAYS = 90   // Не позже 90 дней вперед

//ОСНОВНОЙ БЛОК--------------------------------------------------------
def today = new Date().clearTime()

return [
    'min': api.date.addDays(today, MIN_DAYS),
    'max': api.date.addDays(today, MAX_DAYS)
]

// -----------------------------------------------------------------------------
// Пример 9: Фильтрация с поиском по иерархии
// Категория: Скрипт фильтрации значений атрибута
// Использование: Показывать объект и всех его потомков
// -----------------------------------------------------------------------------
// Часть 1
if (subject == null) {
    return ['rootOU']
}

// Часть 2: Рекурсивный поиск всех дочерних отделов
def rootOU = form?.rootOU ?: subject?.rootOU
if (!rootOU) {
    return api.filtration.disableFiltration()
}

def getAllChildren(ou) {
    def result = [ou]
    def children = utils.find('ou', ['parent': ou.UUID])
    children.each { child ->
        result.addAll(getAllChildren(child))
    }
    return result
}

return getAllChildren(rootOU)
