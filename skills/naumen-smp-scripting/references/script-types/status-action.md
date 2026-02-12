# Скрипт действия при входе/выходе из статуса

## Назначение

Автоматически выполняет действия при переходе объекта между статусами. Используется для автозаполнения полей, валидации, создания связанных объектов, уведомлений при смене статуса.

## Место настройки

Администрирование → Классы → [Класс] → Жизненный цикл → [Статус] → Действия → Добавить

Выбор: **На вход в статус** или **На выход из статуса**

## Контекстные переменные

| Переменная | Тип | Описание |
|------------|-----|----------|
| `subject` | Object | Текущий объект, статус которого меняется |
| `oldSubject` | Object | Объект **до** смены статуса |
| `initialValues` | Map | Значения с формы смены статуса / формы добавления |
| `comment` | String | Текст комментария с формы смены статуса |
| `isCommentPrivate` | Boolean | Приватность комментария |
| `commentObject` | Object | Созданный объект комментария |
| `cardObject` | Object | Карточка, с которой вызвана смена |
| `user` | Object | Инициатор смены статуса |

## Шаблон

```groovy
//ПАРАМЕТРЫ------------------------------------------------------------
def DATETIME_ATTR = 'resolvedDate'

//ОСНОВНОЙ БЛОК--------------------------------------------------------
// Заполнить дату при входе в статус
utils.edit(subject, [
    (DATETIME_ATTR): new Date(),
    '@user': user
])

// Создать комментарий если есть текст
if (comment) {
    utils.create('comment', [
        'text': comment,
        'source': subject.UUID,
        'author': user,
        'private': isCommentPrivate ?: false
    ])
}
```

## Доступные API

### Полностью доступны
- `utils.find`, `utils.findFirst`, `utils.count`, `utils.get`
- `utils.create`, `utils.edit`, `utils.delete`
- `api.mail.sendMail`
- Все методы API

### Особенности
- `initialValues.getProperty('attrCode')` — получение значения с формы
- `utils.throwReadableException(message)` — прервать смену статуса с ошибкой

## Порядок выполнения

1. **Выход из текущего статуса** — скрипты в порядке настройки
2. **Вход в новый статус** — скрипты в порядке настройки
3. Если любой скрипт упал — смена статуса отменяется

## Чек-лист проверок

### Транзакционность
- [ ] Ошибка в скрипте откатывает всю смену статуса
- [ ] Не вызывать внешние системы без обработки ошибок

### Корректность
- [ ] Передача `@user` в utils.edit
- [ ] Проверка oldSubject.state для условной логики
- [ ] initialValues для значений с формы добавления

### Особые случаи
- [ ] Первый статус "Зарегистрирован" — значения только через initialValues
- [ ] Подчиненные запросы — проверка `subject.masterMassProblem`

## Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| Смена статуса не проходит | Ошибка в скрипте | Проверить логи |
| oldSubject.reverseLinks = null | Обратные ссылки недоступны | Делать отдельный поиск |
| Нет значений с формы | Использование subject вместо initialValues | Использовать initialValues |
| Цикл смен статусов | Скрипт меняет статус, что триггерит скрипт | Проверка oldSubject.state |

## Особенности

1. **initialValues**: На входе в "Зарегистрирован" атрибуты subject могут быть null — используйте initialValues.

2. **Транзакция**: Скрипт выполняется в одной транзакции со сменой статуса. Ошибка = откат.

3. **Обратные ссылки oldSubject**: Всегда null — делайте прямой поиск.

4. **Подчиненные запросы**: Некоторые атрибуты нельзя редактировать. Проверяйте `subject.masterMassProblem`.

## Примеры

### Заполнить дату при входе
```groovy
def ATTR = 'closedDate'
utils.edit(subject, [(ATTR): new Date()])
```

### Сохранить старого ответственного
```groovy
def STATES = ['closed', 'resolved']
if (STATES.contains(oldSubject.state)) {
    utils.edit(subject, [
        'responsibleEmployee': oldSubject.responsibleEmployee,
        'responsibleTeam': oldSubject.responsibleTeam
    ])
}
```

### Скопировать атрибут в комментарий
```groovy
def ATTR = 'resolution'
def text = utils.asRTF(subject, ATTR)
if (text?.trim()) {
    utils.create('comment', [
        'text': "Решение: ${text}",
        'source': subject.UUID,
        'author': user
    ])
} else {
    utils.throwReadableException("Заполните поле '${ATTR}' перед закрытием")
}
```

→ См. [examples/event-actions.groovy](../examples/event-actions.groovy) (примеры 3-4)
