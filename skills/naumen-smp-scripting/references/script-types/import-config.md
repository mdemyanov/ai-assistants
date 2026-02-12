# Скрипт конфигурации импорта

## Назначение

Определяет параметры загрузки данных из внешних источников (файлов CSV, XML, LDAP, внешних систем). XML-конфигурация со встроенными Groovy-скриптами для фильтрации, преобразования и валидации импортируемых данных.

## Место настройки

Администрирование → Импорт → Добавить конфигурацию / Редактировать

## Контекстные переменные

### В script-filter
| Переменная | Тип | Описание |
|------------|-----|----------|
| `item` | Object | Строка импортируемых данных |
| `ctx` | Object | Контекст импорта |
| `parameters` | Map | Параметры конфигурации |

### В script-converter
| Переменная | Тип | Описание |
|------------|-----|----------|
| `value` | Object | Конвертируемое значение |
| `item` | Object | Строка импортируемых данных |
| `subject` | Object | Импортируемый объект |
| `ctx` | Object | Контекст импорта |
| `storage` | Map | Данные между скриптами |
| `parameters` | Map | Параметры конфигурации |

### В script-customizer
| Переменная | Тип | Описание |
|------------|-----|----------|
| `item` | Object | Строка импортируемых данных |
| `subject` | Object | Импортируемый объект |
| `properties` | Map | Свойства для создания/редактирования |
| `ctx` | Object | Контекст импорта |
| `storage` | Map | Данные между скриптами |

## Структура XML-конфигурации

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config save-log="true">
    <!-- Режимы: CREATE, UPDATE, EMPTY -->
    <mode>CREATE</mode>
    <mode>UPDATE</mode>

    <!-- Параметры с формы -->
    <gui-parameter name="file" type="FILE" title="CSV файл"/>

    <!-- Константы -->
    <parameter name="metaclass">ou$import</parameter>

    <class name="ou" threads-number="1">
        <!-- Источник данных -->
        <csv-data-source with-header="true" file-name="$file"
                         delimiter=";" encoding="UTF8">
            <column name="title" src-key="Название"/>
            <column name="code" src-key="Код"/>
        </csv-data-source>

        <!-- Определение типа -->
        <constant-metaclass-resolver metaclass="${metaclass}"/>

        <!-- Поиск существующего -->
        <object-searcher attr="code" metaclass="${metaclass}"/>

        <!-- Маппинг атрибутов -->
        <attr name="title" column="title"/>
        <attr name="code" column="code"/>

        <!-- Кастомизация -->
        <script-customizer>
            <before-process-item>...</before-process-item>
            <after-process>...</after-process>
        </script-customizer>
    </class>
</config>
```

## Этапы выполнения script-customizer

| Этап | Описание | Доступ к subject |
|------|----------|------------------|
| `<before-process-item>` | До формирования свойств | Только чтение |
| `<before-process>` | До создания/редактирования | Только чтение |
| `<after-process>` | После создания/редактирования | Чтение/запись |
| `<after-import>` | После всего импорта | Недоступен |

## Чек-лист проверок

### Корректность
- [ ] В `script-filter` обращение к БД через `api.tx.call({})`
- [ ] В `script-customizer` НЕ использовать `api.tx.call` — уже в транзакции
- [ ] Проверка `threads-number="1"` при использовании storage

### Производительность
- [ ] Минимум потоков для сложной логики
- [ ] Кэширование справочников в storage
- [ ] Батчевая обработка больших файлов

### Валидация
- [ ] Проверка обязательных колонок в источнике
- [ ] Валидация форматов дат и чисел
- [ ] Логирование через `ctx.getLogger()`

## Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| Ошибка транзакции | api.tx.call в customizer | Убрать api.tx.call |
| storage не работает | threads-number > 1 | Установить threads-number="1" |
| Не создаются объекты | Режим только UPDATE | Добавить mode CREATE |
| Нет действий по событиям | Особенность utils.edit в импорте | Использовать отдельный скрипт |

## Примеры

### Фильтр по номерам
```xml
<script-filter><![CDATA[
def NUMBERS = [108, 109, 111, 113, 114, 115]
def num = item.properties.getProperty('number')
try {
    return NUMBERS.contains(num?.toInteger())
} catch (e) {
    ctx.getLogger().error("Некорректный номер: ${num}")
    return false
}
]]></script-filter>
```

### Конвертер ссылки на объект
```xml
<attr name="parent" column="parentCode">
    <script-converter><![CDATA[
        if (!value) return null
        def parent = api.tx.call {
            utils.findFirst('ou', ['code': value])
        }
        if (!parent) {
            ctx.getLogger().warn("Не найден отдел: ${value}")
        }
        return parent
    ]]></script-converter>
</attr>
```

### Дозаполнение после импорта
```xml
<script-customizer>
    <after-process><![CDATA[
        if (subject.state == 'registered') {
            utils.edit(subject, ['processedDate': new Date()])
        }
    ]]></after-process>
</script-customizer>
```
