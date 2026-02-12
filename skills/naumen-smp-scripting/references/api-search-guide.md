# Поиск в документации API

Полная документация: `/Users/mdemyanov/Devel/naumen-ecosystem/naumen-smp/script/metody-api.md` (575KB)

## Структура документации

Документация организована по namespaces:

| Namespace | Файл | Описание |
|-----------|------|----------|
| api.utils | api-utils-*.md (9 файлов) | Работа с объектами |
| api.db | api-db-ispolzovanie-zaprosov-k-baze-dannykh.md | HQL запросы |
| api.http | api-http-formirovanie-zaprosov-k-json-servisam.md | REST интеграции |
| api.soap | api-soap-*.md | SOAP интеграции |
| api.mail | api-mail-*.md (5 файлов) | Работа с почтой |
| api.ldap | api-ldap-*.md | LDAP интеграция |
| api.date | В metody-api.md | Операции с датами |
| api.timing | api-timing-*.md | Счетчики времени |
| api.security | api-security-*.md | Права доступа |
| api.web | api-web-*.md | Формирование ссылок |
| api.wf | api-wf-*.md | Workflow, статусы |
| api.reports | api-reports-*.md | Отчеты и печатные формы |
| api.metainfo | В metody-api.md | Метаинформация |

## Детальные файлы api.utils

| Файл | Содержание |
|------|------------|
| api-utils-poisk-obektov.md | find, get, load, findFirst, count, условные операции |
| api-utils-rabota-s-obektami.md | create, edit, delete, editWithoutEventActions |
| api-utils-rabota-s-roditelskimi-i-dochernimi-obektami.md | parent, children |
| api-utils-rabota-s-atributami-obekta.md | getAttribute, setAttribute |
| api-utils-rabota-s-kommentariyami.md | comments |
| api-utils-rabota-s-faylami.md | attachFile, getFiles |
| api-utils-rabota-s-shablonami-groovy.md | processTemplate |
| api-utils-redaktirovanie-tablitsy-sootvetstviy.md | correspondence |
| api-utils-formatirovanie-dannykh.md | formatters |

## Паттерны поиска

### По названию метода

```bash
# В терминале
grep "api.http.postJSON" /path/to/metody-api.md

# Через Grep tool
Grep pattern="api\.http\.postJSON" path="/Users/mdemyanov/Devel/naumen-ecosystem/naumen-smp/script/"
```

### По описанию функции

```bash
grep -i "отправка почты" /path/to/metody-api.md
grep -i "создание объекта" /path/to/metody-api.md
```

### По namespace

```bash
grep "^## api.utils" metody-api.md
grep "api\.utils\." metody-api.md
```

## Часто искомые методы

### Работа с объектами
- `utils.get` → api-utils-poisk-obektov.md
- `utils.find` → api-utils-poisk-obektov.md
- `utils.create` → api-utils-rabota-s-obektami.md
- `utils.edit` → api-utils-rabota-s-obektami.md
- `utils.editWithoutEventActions` → api-utils-rabota-s-obektami.md

### Интеграции
- `api.http.*` → api-http-formirovanie-zaprosov-k-json-servisam.md
- `api.soap.*` → api-soap-*.md
- `api.ldap.*` → api-ldap-*.md

### Файлы и комментарии
- `attachFile` → api-utils-rabota-s-faylami.md
- `getFiles` → api-utils-rabota-s-faylami.md
- Комментарии → api-utils-rabota-s-kommentariyami.md

### Отчеты
- `api.reports.*` → api-reports-api-parameters-rabota-s-otchetami-i-pechatnymi-formami.md

### Даты
- `api.date.*` → metody-api.md (поиск по "api.date")
- `utils.formatters.*` → api-utils-formatirovanie-dannykh.md

## Структура файла metody-api.md

```
# Методы API (заголовок)
## api.utils (секция namespace)
### utils.get (метод)
   - Описание
   - Параметры
   - Возвращаемое значение
   - Примеры
### utils.find
   ...
## api.db
### api.db.query
   ...
```

## Рекомендации по поиску

1. **Сначала проверь quick-ref** — 80% задач покрываются ТОП-20 методами
2. **Затем отдельный файл namespace** — для детальной информации
3. **metody-api.md как fallback** — для редких методов через grep
4. **Читай секциями** — используй Read с offset/limit для больших файлов

## Путь к документации

```
/Users/mdemyanov/Devel/naumen-ecosystem/naumen-smp/script/
├── metody-api.md                    # Полный справочник (575KB)
├── kategorii-skriptov.md            # Категории скриптов
├── tipovye-oshibki-i-sposoby-ikh-ispravleniya.md  # Ошибки
├── api-utils-*.md                   # Детали api.utils
├── api-db-*.md                      # Детали api.db
├── api-http-*.md                    # Детали api.http
├── api-mail-*.md                    # Детали api.mail
├── skript-*.md                      # Типы скриптов
└── ...
```
