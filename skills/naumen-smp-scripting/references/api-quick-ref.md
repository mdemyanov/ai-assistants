# API Quick Reference

ТОП-20 методов Naumen SMP API с примерами.

## 1. Поиск объектов

### utils.get(fqn, attributes)

Поиск **ОДНОГО** объекта. Ошибка если найдено несколько.

```groovy
// По UUID
def obj = utils.get('employee$12345')

// По атрибутам (должен вернуть ровно один)
def urg = utils.get('urgency', ['code': 'low'])
```

### utils.load(uuid)

Поиск по UUID. Возвращает **null** если не найден (не ошибку).

```groovy
def obj = utils.load('serviceCall$12345')
if (obj) { /* работа с объектом */ }
```

### utils.find(fqn, attributes)

Поиск **НЕСКОЛЬКИХ** объектов. Возвращает коллекцию (может быть пустой).

```groovy
// Все сотрудники отдела
def employees = utils.find('employee', ['parent': 'ou$123'])

// С пагинацией
def first10 = utils.find('ou', [:], sp.limit(10))
def page2 = utils.find('ou', [:], sp.limit(10).offset(10))

// С условиями
def active = utils.find('employee', ['lastName': op.like('Иван%')])

// Поиск по ссылке на объект
def author = utils.get('employee$12345')
def calls = utils.find('serviceCall', ['author': author])
// или по UUID напрямую
def calls = utils.find('serviceCall', ['author': 'employee$12345'])
```

### utils.findFirst(fqn, attributes)

Первый из найденных. Безопаснее чем get.

```groovy
def item = utils.findFirst('urgency', [:])
```

### utils.count(fqn, attributes)

Подсчет количества объектов.

```groovy
def total = utils.count('serviceCall', ['state': 'registered'])
```

## 2. Создание и редактирование

### utils.create(fqn, attributes)

```groovy
def newSC = utils.create('serviceCall$request', [
    'title': 'Новый запрос',
    'clientEmployee': user,
    'service': 'service$123'
])

// С комментарием
utils.create('comment', [
    'text': 'Текст комментария',
    'source': subject.UUID
])
```

### utils.edit(object, attributes)

```groovy
// Одним вызовом (ПРАВИЛЬНО)
utils.edit(subject, [
    'title': 'Новое название',
    'state': 'resolved',
    '@comment': 'Комментарий к изменению'
])

// С передачей user в цепочку событий
utils.edit(subject, ['title': 'Новое', '@user': user])
```

### utils.delete(object)

```groovy
def obj = utils.load('serviceCall$12345')
if (obj) {
    utils.delete(obj)
}
```

## 3. HTTP запросы

### api.http.getJSON(url, headers)

```groovy
// Простой GET
def data = api.http.getJSON('https://api.example.com/data')

// С заголовками
def data = api.http.getJSON(
    'https://api.example.com/data',
    ['Authorization': 'Bearer token']
)
```

### api.http.postJSON(url, data, headers)

```groovy
def result = api.http.postJSON(
    'https://api.example.com/create',
    ['key': 'value', 'name': 'test'],
    ['Authorization': 'Bearer token']
)
```

### api.http.putJSON / patchJSON / deleteJSON

```groovy
api.http.putJSON(url, data, headers)
api.http.patchJSON(url, data, headers)
api.http.deleteJSON(url, headers)
```

**Важно:** Timeout 5 сек, кодировка UTF-8.

## 4. HQL запросы (api.db.query)

```groovy
// Простой запрос
def query = api.db.query('from serviceCall sc WHERE sc.state = :state')
query.set('state', 'registered')
query.setMaxResults(100)
def results = query.list()

// Запрос с несколькими параметрами
def query = api.db.query('''
    SELECT sc.id FROM serviceCall sc
    WHERE sc.state = :state AND sc.urgency.code = :urg
''')
query.set([state: 'registered', urg: 'high'])
def ids = query.list()

// Подсчет
def count = api.db.query('SELECT count(sc.id) FROM serviceCall sc').list()[0]

// Поиск по типу в рамках класса (metaCaseId)
def query = api.db.query('''
    SELECT count(sc.id) FROM serviceCall sc
    WHERE sc.metaCaseId = 'INC'
''')
```

**Важно:**
- Только SELECT (INSERT/UPDATE/DELETE запрещены)
- Используй utils.create/edit/delete для изменений
- Для ссылок используй `.id` в WHERE

## 5. Работа с датами

### api.date

```groovy
// Добавить дни
def tomorrow = api.date.addDays(new Date(), 1)
def lastWeek = api.date.addDays(new Date(), -7)

// Форматирование
def formatted = utils.formatters.dateToStr(new Date(), 'dd.MM.yyyy')
def formatted2 = utils.formatters.dateToStr(new Date(), 'yyyy-MM-dd HH:mm:ss')

// Парсинг
def parsed = utils.formatters.strToDate('2024-01-15', 'yyyy-MM-dd')
def parsed2 = utils.formatters.strToDate('15.01.2024 10:30', 'dd.MM.yyyy HH:mm')
```

## 6. Работа с файлами

```groovy
// Получить файлы объекта
def files = subject.getFiles()

// Прикрепить файл
def file = api.utils.attachFile(subject, bytes, 'filename.pdf', 'description')

// Получить содержимое файла
def content = file.getBytes()
```

## 7. Веб-ссылки

### api.web

```groovy
// Ссылка на карточку объекта
def url = api.web.open(subject)

// Ссылка на форму добавления
def url = api.web.add(['serviceCall$request'], null, ['title': 'Заголовок'])

// Ссылка на список объектов
def url = api.web.list(subject, 'contentCode')

// Скачать файл
def url = api.web.download(file)
```

## 8. Метаинформация

```groovy
// Получить метакласс объекта
def mc = api.metainfo.getMetaClass(subject)

// Получить атрибут
def attr = mc.getAttribute('attrCode')

// Проверить тип объекта
def fqn = subject.getMetainfo().toString() // 'serviceCall$request'
```

## 9. Условные операции (op.*)

```groovy
// Поиск по вхождению
utils.find('employee', ['lastName': op.like('Иван%')])
utils.find('employee', ['lastName': op.like('%ванов%')])

// Входит в список
utils.find('employee', ['parent': op.in('ou$1', 'ou$2', 'ou$3')])
utils.find('employee', ['parent': op.in(ouList)]) // коллекция

// Не равно (включая объекты с null!)
utils.find('employee', ['parent': op.not('ou$123')])
// Не равно (исключая null)
utils.find('employee', ['ouAttr': op.not(null, 'ou$123')])

// Диапазоны
utils.find('serviceCall', ['registeredDate': op.gt(startDate)])
utils.find('serviceCall', ['registeredDate': op.lt(endDate)])
utils.find('serviceCall', ['registeredDate': op.between(startDate, endDate)])

// Null проверки
utils.find('serviceCall', ['responsibleEmployee': op.isNull()])
utils.find('serviceCall', ['responsibleEmployee': op.isNotNull()])
```

## 10. Параметры поиска (sp.*)

```groovy
// Лимит
utils.find('ou', [:], sp.limit(10))

// Пагинация (offset требует limit!)
utils.find('ou', [:], sp.limit(10).offset(20))

// Игнорировать регистр (только для строк!)
utils.find('ou', ['title': 'Отдел'], sp.ignoreCase())

// Комбинирование
utils.find('ou', ['title': 'Отдел'], sp.limit(10).offset(5).ignoreCase())
```
