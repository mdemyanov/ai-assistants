# Скрипт шаблона отчета / печатной формы

## Назначение

Формирует данные для отчетов и печатных форм. Определяет параметры отчета, извлекает данные (включая вычислимые атрибуты), преобразует их для вывода. Работает совместно с Pentaho Report Designer (PRD).

## Место настройки

Администрирование → Отчеты → Добавить шаблон / Редактировать

## Контекстные переменные

### Общие переменные
| Переменная | Тип | Описание |
|------------|-----|----------|
| `user` | Object | Текущий пользователь |
| `table` | Object | Таблица данных отчета |

### В getParameters()
| Переменная | Тип | Описание |
|------------|-----|----------|
| `user` | Object | Текущий пользователь |
| `subject` | Object | Объект, с карточки которого строится отчет |

### В setFiltrationScript()
| Переменная | Тип | Описание |
|------------|-----|----------|
| `params` | Map | Уже выбранные параметры отчета |
| `subject` | Object | null при получении зависимых атрибутов |

## Структура скрипта

```groovy
//ПАРАМЕТРЫ------------------------------------------------------------
def DATE_FORMAT = 'dd.MM.yyyy'

//ФУНКЦИИ--------------------------------------------------------------
def getParameters() {
    return [
        api.parameters.getDate('dateFrom', 'Дата с'),
        api.parameters.getDate('dateTo', 'Дата по'),
        api.parameters.getObject('service', 'Услуга', 'slmService')
    ]
}

//ОСНОВНОЙ БЛОК--------------------------------------------------------
// Обработка данных из SQL-запроса
table.rows.each { row ->
    // Вычисление процентов
    row.percent = row.count * 100.0 / total
    // Форматирование
    row.dateStr = row.date?.format(DATE_FORMAT)
}

return table
```

## Методы api.parameters

| Метод | Описание |
|-------|----------|
| `getString(code, title, default)` | Строковый параметр |
| `getInteger(code, title, default)` | Целое число |
| `getDouble(code, title, default)` | Дробное число |
| `getBoolean(code, title, default)` | Логический |
| `getDate(code, title, default)` | Дата |
| `getDateTime(code, title, default)` | Дата/время |
| `getObject(code, title, metaclass, default)` | Ссылка на объект |
| `getObjects(code, title, metaclass, defaults)` | Набор объектов |
| `getCatalogItem(code, title, catalog, default)` | Элемент справочника |
| `getCatalogItems(code, title, catalog, defaults)` | Набор элементов |
| `getState(code, title, metaclass, default)` | Статус |
| `getStates(code, title, metaclass, defaults)` | Набор статусов |

## Режимы работы

| Режим | Описание | Когда использовать |
|-------|----------|-------------------|
| **Обычный** | Данные в памяти | Небольшие отчеты <10000 строк |
| **Потоковый** | Данные на диске | Большие отчеты, добавить `/*&streamMode*/` |

## Чек-лист проверок

### Производительность
- [ ] Потоковый режим для больших отчетов
- [ ] Лимиты в SQL-запросах
- [ ] Кэширование справочников

### Корректность
- [ ] Обработка null в вычислениях
- [ ] Форматирование дат и чисел
- [ ] Возврат table в конце скрипта

### Параметры
- [ ] Значения по умолчанию для всех параметров
- [ ] Фильтрация зависимых параметров

## Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| Пустой отчет | Не возвращается table | Добавить `return table` |
| Ошибка в PRD | Регистр переменных не совпадает | Использовать lowercase или кавычки в SQL |
| Параметры недоступны | Вызов через api.reports | user/subject = null при API вызове |

## Особенности

1. **Потоковый режим**: В начале скрипта `/*&streamMode*/`. Алиасы SQL становятся lowercase.

2. **PRD интеграция**: Имена переменных в PRD должны совпадать с алиасами SQL.

3. **api.reports вызов**: При программном вызове user и subject в getParameters() = null.

## Примеры

### Параметры с фильтрацией
```groovy
def getParameters() {
    return [
        api.parameters.getObject('service', 'Услуга', 'slmService'),
        api.parameters.getObjects('requests', 'Запросы', 'serviceCall')
            .setFiltrationScript({
                def DEPS = ['service']
                if (subject == null) return DEPS
                return utils.find('serviceCall', ['service': params.service])
            })
    ]
}
```

### Вычисление процентов
```groovy
def total = table.rows.collect { it.count }.sum() ?: 1

table.rows.each { row ->
    row.percent = String.format("%.2f%%", row.count * 100.0 / total)
}

return table
```

### Кастомная функция
```groovy
def getFunctions() {
    return [
        api.reports.totalFunction('currentUser', { rows ->
            api.tx.call { user?.title }
        })
    ]
}
```
