---
project: chistova16-site
type: static-site
---

# Технический контекст

## Стек технологий

| Компонент | Технология | Версия |
|-----------|------------|--------|
| Генератор | Hugo | latest (extended) |
| Хостинг | Yandex Object Storage | S3-compatible |
| CI/CD | GitHub Actions | v4 |
| CSS | Vanilla CSS | - |
| Шаблоны | Go templates | - |

## Архитектура Hugo

### Layouts иерархия

```
layouts/
├── _default/           # Базовые шаблоны
│   ├── baseof.html     # Базовый layout (<!DOCTYPE>, <head>, <body>)
│   ├── single.html     # Одиночная страница (по умолчанию)
│   └── list.html       # Список (по умолчанию)
├── index.html          # Главная страница ЖК
├── news/
│   └── list.html       # Агрегатор новостей (собирает из всех корпусов)
├── docs/
│   └── list.html       # Список документов с категориями
├── reports/
│   └── list.html       # Список отчётов по периодам
├── oss/
│   ├── list.html       # Список ОСС
│   └── single.html     # Страница конкретного ОСС
├── faq/
│   └── single.html     # FAQ с аккордеоном
├── partials/           # Переиспользуемые компоненты
└── shortcodes/         # Вставляемые компоненты для контента
```

### Content организация

```
content/
├── _index.md           # Главная (использует layouts/index.html)
├── about.md            # О комплексе (single)
├── news/
│   └── _index.md       # Только индекс, сами новости в корпусах
├── [building]/         # parking, k1, k2
│   ├── _index.md       # Главная корпуса
│   ├── contacts.md     # Контакты
│   ├── faq.md          # FAQ (layout: faq)
│   ├── tariffs.md      # Тарифы
│   ├── news/           # Секция новостей
│   ├── docs/           # Секция документов
│   ├── reports/        # Секция отчётов
│   └── oss/            # Секция ОСС
```

### Data-driven подход

Информация о корпусах и ТСН хранится в `data/`:
- `buildings.yaml` — список корпусов, цвета, ссылки
- `tsn.yaml` — реквизиты организаций

Доступ в шаблонах:
```go
{{ $building := index .Site.Data.buildings "k2" }}
{{ $tsn := index .Site.Data.tsn $building.tsn }}
{{ $tsn.name }}
```

## Паттерны шаблонов

### Агрегация новостей

```go
{{/* layouts/news/list.html */}}
{{ $allNews := slice }}
{{ range .Site.Sections }}
  {{ with .GetPage "news" }}
    {{ range .Pages }}
      {{ $allNews = $allNews | append . }}
    {{ end }}
  {{ end }}
{{ end }}
{{ range sort $allNews "Date" "desc" }}
  {{ partial "news-card.html" . }}
{{ end }}
```

### Определение корпуса из контекста

```go
{{/* В любом шаблоне внутри /parking/, /k1/, /k2/ */}}
{{ $buildingId := index (split .RelPermalink "/") 1 }}
{{ $building := index .Site.Data.buildings $buildingId }}
```

### Badge корпуса

```go
{{/* partials/building-badge.html */}}
{{ $building := index .Site.Data.buildings .Params.building }}
<span class="badge" style="background: {{ $building.color }}">
  {{ $building.name }}
</span>
```

## Yandex Object Storage

### Настройка bucket

1. Создать bucket с именем `chistova16.ru`
2. Включить static website hosting
3. Index document: `index.html`
4. Error document: `404.html`

### DNS настройка

```
chistova16.ru.  CNAME  chistova16.ru.website.yandexcloud.net.
```

### Секреты GitHub

- `YC_ACCESS_KEY` — Access Key сервисного аккаунта
- `YC_SECRET_KEY` — Secret Key сервисного аккаунта

Сервисный аккаунт должен иметь роль `storage.editor` на bucket.

## Соглашения

### Naming

- Файлы новостей: `YYYY-MM-DD-slug.md`
- Файлы отчётов: `YYYY-QN.md` или `YYYY.md` (годовой)
- Папки ОСС: `MM-YYYY` (месяц-год начала)
- ID корпусов: `parking`, `k1`-`k7`

### Frontmatter

Обязательные поля для всех типов контента:
- `title` — заголовок
- `date` — дата создания/публикации
- `building` — ID корпуса (parking, k1, k2)

### CSS классы

```
.card           — карточка с тенью
.badge          — метка корпуса
.btn            — кнопка
.btn-primary    — основная кнопка
.btn-outline    — кнопка с обводкой
.nav            — навигация
.breadcrumbs    — хлебные крошки
.faq-item       — элемент FAQ
.table          — таблица
```

## Ограничения

### Hugo

- Нет серверной логики — только статика
- Поиск потребует внешнего сервиса (или JS-библиотека типа Lunr)
- Формы — только через внешние сервисы

### Yandex Object Storage

- Максимальный размер файла: 5 ГБ
- Нет server-side redirects — только meta refresh или JS
- CORS настраивается отдельно если нужен

### Браузеры

Поддержка:
- Chrome/Edge 90+
- Firefox 90+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

CSS Grid и Flexbox — без fallbacks для IE.
