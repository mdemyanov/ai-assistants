# Скрипт пользовательского действия по событию (кнопка-скрипт)

## Назначение

Выполняет произвольное действие по нажатию кнопки пользователем. Используется для массовых операций, интеграций, открытия форм с предзаполненными полями, скачивания файлов и других интерактивных сценариев.

## Место настройки

Администрирование → Действия по событиям → Добавить → Событие: Пользовательское

Кнопка выводится в меню действий карточки или списка.

## Контекстные переменные

| Переменная | Тип | Описание |
|------------|-----|----------|
| `subject` | Object | Произвольный объект из subjects (один из выбранных) |
| `subjects` | List | Все выбранные объекты (из списка или один с карточки) |
| `list` | List | Все объекты списка (макс 1000). `list.limitExceeded()` |
| `params` | Map | Параметры с формы пользовательского действия |
| `source` | String | Откуда вызвано: OBJECT_LIST или OBJECT_CARD |
| `result` | Object | Управление UI после выполнения |
| `cardObject` | Object | Карточка, с которой вызвано (если из карточки) |
| `user` | Object | Текущий пользователь |
| `geo` | Object | Геолокация (для мобильного приложения) |

## Шаблон

```groovy
//ПАРАМЕТРЫ------------------------------------------------------------
def TARGET_STATE = 'inProgress'

//ОСНОВНОЙ БЛОК--------------------------------------------------------
// Обработка всех выбранных объектов
subjects.each { obj ->
    if (obj.state == 'registered') {
        utils.edit(obj, [
            'state': TARGET_STATE,
            'responsibleEmployee': user
        ])
    }
}

// Показать сообщение
result.showMessage("Готово", "Обработано объектов: ${subjects.size()}")
```

## Методы result (веб-приложение)

| Метод | Описание |
|-------|----------|
| `result.showMessage(title, message)` | Показать сообщение |
| `result.setErrorMessage(message)` | Показать ошибку (без прерывания скрипта) |
| `result.goToUrl(url)` | Переход по ссылке |
| `result.goToUrl(url, true)` | Открыть в новой вкладке |
| `result.downloadFile(file)` | Скачать файл |
| `result.downloadFile(file, title)` | Скачать с другим именем |
| `result.reload(true)` | Обновить карточку после действия |
| `result.executeJavaScript(js)` | Выполнить JS на клиенте |

## Методы result (мобильное приложение)

| Метод | Описание |
|-------|----------|
| `result.showMessage(message)` | Toast сообщение |
| `result.showMessage(title, message)` | Диалоговое окно |
| `result.goToMobileAddForm(formCode, attrs)` | Открыть форму добавления |
| `result.goToMobileEditForm(subject, attrs)` | Открыть форму редактирования |
| `result.goToMobileObjectCard(subject)` | Перейти на карточку |
| `result.goToExternal(url, attrs)` | Открыть внешнее приложение |

## Доступные API

### Полностью доступны
- `utils.find`, `utils.findFirst`, `utils.count`, `utils.get`
- `utils.create`, `utils.edit`, `utils.delete`
- `api.http.*`, `api.soap.*`
- `api.web.add`, `api.web.open`, `api.web.list`
- `api.reports.getReportDataSource`

## Чек-лист проверок

### Производительность
- [ ] Батчевая обработка для больших списков subjects
- [ ] Единый utils.edit вместо нескольких
- [ ] Таймаут для внешних запросов

### UI/UX
- [ ] Информативное сообщение по завершении
- [ ] Обработка ошибок с понятным сообщением
- [ ] `result.reload(true)` если данные изменились

### Корректность
- [ ] Проверка прав: subjects содержит только разрешенные объекты
- [ ] Проверка source для разного поведения (карточка vs список)
- [ ] Null-safe доступ к params

## Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| subjects = null | Нет прав на действие | Проверить матрицу прав |
| Форма не обновляется | Не вызван reload | Добавить `result.reload(true)` |
| goToUrl не работает | Некорректный URL | Использовать `api.web.open(...)` |
| list.limitExceeded() | Более 1000 объектов | Обработать частями |

## Особенности

1. **subjects vs list**: `subjects` — выбранные объекты с правами, `list` — все объекты списка (макс 1000).

2. **Синхронность обязательна**: Методы result работают только для синхронных действий.

3. **params зарезервировано**: Используется для параметров формы. Не переопределять!

4. **Веб vs Мобильное**: Разные методы result для разных платформ.

## Примеры

### Подписка на объекты
```groovy
subjects.each { obj ->
    def subs = (obj.subscribers ?: []) + user
    utils.edit(obj, ['subscribers': subs.unique { it.UUID }])
}
result.showMessage("Подписка оформлена на ${subjects.size()} объектов")
result.reload(true)
```

### Открыть форму добавления
```groovy
def attrs = [
    'client': subject.client,
    'service': subject.service,
    'parent': subject.UUID
]
def url = api.web.add(['serviceCall$request'], subject.UUID, attrs)
result.goToUrl("#${api.web.getPlace(url)}", false)
```

### Скачать отчет
```groovy
def source = api.reports.getReportDataSource(
    'reportTemplate',
    subject.UUID,
    [:],
    'pdf'
)
result.downloadFile(source, "Отчет_${subject.number}.pdf")
```

→ См. [examples/event-actions.groovy](../examples/event-actions.groovy) (примеры 5-6)
