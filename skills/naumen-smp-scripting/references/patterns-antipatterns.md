# Паттерны и Антипаттерны Naumen SMP

## Паттерны (ИСПОЛЬЗОВАТЬ)

### 1. Единый utils.edit

**Проблема:** Множественные вызовы edit замедляют работу и генерируют лишние события.

```groovy
// ПЛОХО
utils.edit(subject, ['attr1': value1])
utils.edit(subject, ['attr2': value2])
utils.edit(subject, ['attr3': value3])

// ХОРОШО
utils.edit(subject, [
    'attr1': value1,
    'attr2': value2,
    'attr3': value3
])
```

### 2. Null-safe навигация

```groovy
// ПЛОХО - падает на null
def name = subject.responsibleEmployee.parent.title

// ХОРОШО
def name = subject?.responsibleEmployee?.parent?.title ?: 'Не указано'
```

### 3. Кэширование повторных вызовов

```groovy
// ПЛОХО
prop.attr1 = api.metainfo.getMetaClass(subject).getAttribute('attr1')
prop.attr2 = api.metainfo.getMetaClass(subject).getAttribute('attr2')

// ХОРОШО
def mc = api.metainfo.getMetaClass(subject)
prop.attr1 = mc.getAttribute('attr1')
prop.attr2 = mc.getAttribute('attr2')
```

### 4. Лимиты для больших выборок

```groovy
// ПЛОХО - может вернуть 100000 объектов
def all = utils.find('serviceCall', [:])

// ХОРОШО
def batch = utils.find('serviceCall', [:], sp.limit(1000))

// Для подсчета (не загружает объекты)
def count = utils.count('serviceCall', [:])
```

### 5. Батчевая обработка больших коллекций

```groovy
// ПЛОХО - PersistenceContext limit exceeded
def allCalls = utils.find('serviceCall', [:])
allCalls.each { utils.edit(it, ['processed': true]) }

// ХОРОШО
def BATCH_SIZE = 500
def offset = 0
while (true) {
    def batch = utils.find('serviceCall', ['processed': false],
                          sp.limit(BATCH_SIZE).offset(offset))
    if (!batch) break

    batch.each { utils.edit(it, ['processed': true]) }
    offset += BATCH_SIZE
}
```

### 6. Проверка изменений через changedAttributes

```groovy
// ПЛОХО - сравнение объектов может не работать корректно
if (oldSubject.title != subject.title) { ... }

// ХОРОШО
if (changedAttributes.contains('title')) { ... }
```

### 7. Исключение текущего объекта из поиска

```groovy
// Найти всех сотрудников кроме текущего
def others = utils.find('employee', [
    'parent': subject.parent,
    'UUID': op.not(subject.UUID)
])
```

### 8. Передача user в цепочку событий

```groovy
// Сохраняет user для последующих действий по событиям
utils.edit(subject, [
    'title': 'Новое название',
    '@user': user
])
```

### 9. Сравнение объектов

```groovy
// ПЛОХО - может не работать
if (subject == otherObject) { ... }

// ХОРОШО - по UUID
if (subject.UUID == otherObject.UUID) { ... }

// или через utils.equal
if (utils.equal(subject, otherObject)) { ... }
```

### 10. Структура скрипта

```groovy
//ПАРАМЕТРЫ------------------------------------------------------------
def TARGET_STATE = 'resolved'
def ALLOWED_STATES = ['registered', 'inProgress']

//ФУНКЦИИ--------------------------------------------------------------
def isAllowed(state) {
    return ALLOWED_STATES.contains(state)
}

//ОСНОВНОЙ БЛОК--------------------------------------------------------
if (isAllowed(subject.state)) {
    utils.edit(subject, ['state': TARGET_STATE])
}
```

---

## Антипаттерны (ИЗБЕГАТЬ)

### 1. Вычислимый атрибут в поиске

**Ошибка:** `Could not resolve property`

```groovy
// ОШИБКА: isEmployeeActive - вычислимый атрибут
utils.find('employee', ['isEmployeeActive': true])

// РЕШЕНИЕ: использовать системные атрибуты или HQL
utils.find('employee', ['removed': false])
```

### 2. Строка вместо UUID для ссылки

**Ошибка:** `Could not execute query`

```groovy
// ОШИБКА
utils.find('catalogs$bu', ['item': 'Телефон'])

// РЕШЕНИЕ
utils.find('catalogs$bu', ['item': 'item$2353453'])
```

### 3. Пустой список в HQL IN

**Ошибка:** `Could not extract ResultSet`

```groovy
// ОШИБКА
def list = []
api.db.query('SELECT id FROM T WHERE id in (:list)')
   .set('list', list).list()

// РЕШЕНИЕ
if (list) {
    api.db.query('SELECT id FROM T WHERE id in (:list)')
       .set('list', list).list()
} else {
    return []
}
```

### 4. sp.ignoreCase с числовыми атрибутами

**Ошибка:** `Could not extract ResultSet`

```groovy
// ОШИБКА
utils.find('serviceCall', ['number': '1'], sp.ignoreCase())

// РЕШЕНИЕ - без ignoreCase для чисел
utils.find('serviceCall', ['number': 1])
```

### 5. utils.get без фильтра

**Ошибка:** `Many objects in result`

```groovy
// ОШИБКА
utils.get('ou', [:])

// РЕШЕНИЕ
utils.findFirst('ou', [:])
// или
utils.get('ou$12345')
```

### 6. Обращение к UUID на null

**Ошибка:** `Cannot get property 'UUID' on null object`

```groovy
// ОШИБКА
def uuid = subject.responsibleEmployee.UUID

// РЕШЕНИЕ
def uuid = subject?.responsibleEmployee?.UUID
if (uuid) { ... }
```

### 7. Циклическая ссылка в JSON

**Ошибка:** `There is a cycle in the hierarchy`

```groovy
// ОШИБКА - передача объекта с ссылками в JSON
def data = [
    'employee': subject.responsibleEmployee // объект!
]
api.http.postJSON(url, data)

// РЕШЕНИЕ - передавать только примитивы
def data = [
    'employeeUUID': subject.responsibleEmployee?.UUID,
    'employeeName': subject.responsibleEmployee?.title
]
```

### 8. Обратная ссылка в oldSubject

```groovy
// ОШИБКА - всегда null
def oldLinks = oldSubject.reverseLinks

// РЕШЕНИЕ - обратные ссылки в oldSubject недоступны
// Используй прямой поиск
def links = utils.find('linkedClass', ['target': subject.UUID])
```

### 9. Использование params для других целей

```groovy
// ОШИБКА - params зарезервировано для параметров формы
def params = [:]

// РЕШЕНИЕ
def myParams = [:]
```

### 10. Статические поля без класса

**Ошибка:** Компиляция

```groovy
// ОШИБКА
static def MY_CONSTANT = 'value'

// РЕШЕНИЕ
class Constants {
    static def MY_CONSTANT = 'value'
}
```

---

## Типичные ошибки и решения

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `No signature of method` | Неверные параметры метода | Проверить типы аргументов |
| `NullPointerException` | Обращение к null объекту | Добавить `?.` или проверку |
| `Many objects in result` | utils.get нашел несколько | Использовать findFirst |
| `Could not resolve property` | Вычислимый атрибут в поиске | Не использовать в find |
| `Could not extract ResultSet` | Пустой список в IN / ignoreCase с числом | Проверка на пустоту / убрать ignoreCase |
| `Loader not found for prefix` | Строка вместо объекта | Передавать UUID |
| `ConnectException` | Проблемы подключения | Проверить настройки сети |
| `PersistenceContext limit exceeded` | >50000 объектов | Батчевая обработка |
| `There is a cycle in the hierarchy` | Объект со ссылками в JSON | Передавать только примитивы |
| `Wait for modules to be initialized` | Конфликт имен классов в модулях | Режим компиляции OneByOne |
