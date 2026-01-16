---
task: chistova16-site
status: draft
priority: medium
created: 2026-01-11
---

# Hugo-сайт для ЖК «Волжская Life»

## Цель

Создать информационный сайт для жилого комплекса «Волжская Life» (г. Москва, ул. Чистова, д. 16) на Hugo с автодеплоем на Yandex Object Storage.

## Контекст

ЖК состоит из 7 корпусов и подземного паркинга. Разные корпуса управляются разными организациями:

| Объект | Управляющая организация | Контент |
|--------|------------------------|---------|
| Паркинг | ТСН «Гаражный комплекс «Лайф Паркинг»» | Полный (на сайте) |
| Корпус 1 | ТСН «Лайф 1» | Полный (на сайте) |
| Корпус 2 | ТСН «Лайф 2» | Полный (на сайте) |
| Корпус 3 | УК «Волжская 1» | Внешняя ссылка |
| Корпус 4 | ГБУ Жилищник Текстильщики | Внешняя ссылка |
| Корпуса 5-7 | УК «Волжская 1» | Внешняя ссылка |

**Домен:** chistova16.ru

## Требования

### Must have

- [ ] Hugo-проект с нуля (без готовых тем)
- [ ] Главная страница ЖК с карточками всех корпусов
- [ ] Полноценные разделы для паркинга, К1, К2:
  - Новости
  - Документы (с вложенными папками)
  - Отчётность
  - ОСС (общие собрания собственников)
  - FAQ
  - Тарифы
  - Контакты
- [ ] Агрегированная лента новостей всего ЖК
- [ ] Карточки корпусов К3-К7 со ссылками на внешние сайты УК
- [ ] GitHub Actions для деплоя на Yandex Object Storage
- [ ] Mobile-first адаптивный дизайн
- [ ] README с инструкциями по добавлению контента

### Should have

- [ ] RSS-лента для новостей
- [ ] Open Graph мета-теги
- [ ] Breadcrumbs навигация
- [ ] Фильтрация новостей по корпусу
- [ ] Shortcodes для переиспользуемых блоков

### Won't have (в этой итерации)

- Формы обратной связи
- Аутентификация / закрытые разделы
- Мультиязычность
- Комментарии

## URL-структура

```
/                           # Главная ЖК
/news/                      # Все новости (агрегация)
/about/                     # О комплексе

/parking/                   # Паркинг
/parking/news/              # Новости
/parking/docs/              # Документы
/parking/docs/[category]/   # Подпапка документов
/parking/reports/           # Отчётность
/parking/oss/               # Собрания собственников
/parking/oss/[MM-YYYY]/     # Конкретное собрание
/parking/faq/               # Частые вопросы
/parking/tariffs/           # Тарифы
/parking/contacts/          # Контакты

/k1/                        # Корпус 1 (аналогично parking)
/k2/                        # Корпус 2 (аналогично parking)
```

## Структура Hugo-проекта

```
chistova16-site/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── archetypes/
│   ├── default.md
│   ├── news.md
│   ├── report.md
│   ├── document.md
│   ├── oss.md
│   └── faq.md
├── content/
│   ├── _index.md
│   ├── about.md
│   ├── news/
│   │   └── _index.md
│   ├── parking/
│   │   ├── _index.md
│   │   ├── contacts.md
│   │   ├── faq.md
│   │   ├── tariffs.md
│   │   ├── news/
│   │   │   ├── _index.md
│   │   │   └── 2025-01-15-example.md
│   │   ├── docs/
│   │   │   ├── _index.md
│   │   │   ├── ustav.md
│   │   │   └── oss2025/
│   │   │       └── _index.md
│   │   ├── reports/
│   │   │   ├── _index.md
│   │   │   └── 2024-q4.md
│   │   └── oss/
│   │       ├── _index.md
│   │       └── 01-2025/
│   │           ├── _index.md
│   │           ├── agenda.md
│   │           ├── results.md
│   │           └── protocol.md
│   ├── k1/
│   │   └── ... (аналогично parking)
│   └── k2/
│       └── ... (аналогично parking)
├── data/
│   ├── buildings.yaml
│   └── tsn.yaml
├── layouts/
│   ├── _default/
│   │   ├── baseof.html
│   │   ├── single.html
│   │   └── list.html
│   ├── index.html
│   ├── news/
│   │   └── list.html
│   ├── docs/
│   │   └── list.html
│   ├── reports/
│   │   └── list.html
│   ├── oss/
│   │   ├── list.html
│   │   └── single.html
│   ├── faq/
│   │   └── single.html
│   ├── partials/
│   │   ├── header.html
│   │   ├── footer.html
│   │   ├── nav.html
│   │   ├── breadcrumbs.html
│   │   ├── building-card.html
│   │   ├── news-card.html
│   │   ├── oss-card.html
│   │   ├── faq-item.html
│   │   ├── tsn-requisites.html
│   │   └── qr-payment.html
│   └── shortcodes/
│       ├── requisites.html
│       ├── file-link.html
│       └── building-badge.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── images/
│   │   ├── logo.svg
│   │   ├── map-jk.png
│   │   └── qr/
│   │       ├── parking.png
│   │       ├── k1.png
│   │       └── k2.png
│   └── files/
│       ├── parking/
│       ├── k1/
│       └── k2/
├── hugo.toml
├── README.md
└── .gitignore
```

## Данные (data/)

### buildings.yaml

```yaml
parking:
  id: parking
  name: Паркинг
  fullName: Подземный паркинг
  tsn: parking
  managed: true
  color: "#6B7280"
  description: Подземный паркинг под корпусами 1-6

k1:
  id: k1
  name: Корпус 1
  fullName: Корпус 1
  tsn: life1
  managed: true
  color: "#3B82F6"

k2:
  id: k2
  name: Корпус 2
  fullName: Корпус 2
  tsn: life2
  managed: true
  color: "#10B981"

k3:
  id: k3
  name: Корпус 3
  fullName: Корпус 3
  managed: false
  externalUrl: https://volgskay-1.ru
  managedBy: УК «Волжская 1»

k4:
  id: k4
  name: Корпус 4
  fullName: Корпус 4
  managed: false
  externalUrl: https://gbutekstilshchiki.mos.ru/contacts/info/
  managedBy: ГБУ Жилищник Текстильщики

k5:
  id: k5
  name: Корпус 5
  fullName: Корпус 5
  managed: false
  externalUrl: https://volgskay-1.ru
  managedBy: УК «Волжская 1»

k6:
  id: k6
  name: Корпус 6
  fullName: Корпус 6
  managed: false
  externalUrl: https://volgskay-1.ru
  managedBy: УК «Волжская 1»

k7:
  id: k7
  name: Корпус 7
  fullName: Корпус 7
  managed: false
  externalUrl: https://volgskay-1.ru
  managedBy: УК «Волжская 1»
```

### tsn.yaml

```yaml
parking:
  name: ТСН «Гаражный комплекс «Лайф Паркинг»»
  shortName: ТСН «Лайф Паркинг»
  inn: ""                     # TODO: заполнить
  bank: ""
  bik: ""
  account: ""
  dispatcher: ""
  lkUrl: ""
  telegram: ""

life1:
  name: ТСН «Лайф 1»
  shortName: ТСН «Лайф 1»
  inn: ""                     # TODO: заполнить
  bank: ""
  bik: ""
  account: ""
  dispatcher: ""
  lkUrl: ""
  telegram: ""

life2:
  name: ТСН «Лайф 2»
  shortName: ТСН «Лайф 2»
  inn: "7723556240"
  bank: АО «Альфа-Банк»
  bik: "044525593"
  account: "40703810802100001274"
  dispatcher: "+7 499 719 16 20"
  lkUrl: https://doma.ai
  telegramNews: https://t.me/life2news
  telegramChat: https://t.me/life2chat
```

## Примеры контента

### Главная (content/_index.md)

```markdown
---
title: ЖК «Волжская Life»
description: Информационный портал жилого комплекса
---

Добро пожаловать на информационный портал жилого комплекса «Волжская Life».

Адрес: г. Москва, ул. Чистова, д. 16

Здесь вы найдёте информацию о работе управляющих организаций, документы, отчётность и новости.
```

### Главная паркинга (content/parking/_index.md)

```markdown
---
title: Паркинг
description: Подземный паркинг ЖК «Волжская Life»
building: parking
---

Подземный паркинг расположен под корпусами 1-6 жилого комплекса.

Управление осуществляет ТСН «Гаражный комплекс «Лайф Паркинг»».
```

### Новость (content/parking/news/2025-01-15-example.md)

```markdown
---
title: Пример новости паркинга
date: 2025-01-15
building: parking
pinned: false
tags: [объявление]
---

Текст новости...
```

### Документ (content/parking/docs/ustav.md)

```markdown
---
title: Устав ТСН
date: 2020-01-01
file: /files/parking/ustav.pdf
fileSize: "1.2 MB"
category: учредительные
building: parking
---

Устав Товарищества собственников недвижимости «Гаражный комплекс «Лайф Паркинг»».
```

### Отчёт (content/parking/reports/2024-q4.md)

```markdown
---
title: Отчёт за 4 квартал 2024
date: 2025-01-10
period: 2024-Q4
building: parking
---

## Доходы

| Статья | Сумма, ₽ |
|--------|----------|
| Взносы | 500 000 |

## Расходы

| Статья | Сумма, ₽ |
|--------|----------|
| Электричество | 150 000 |
| Охрана | 100 000 |
```

### ОСС — список (content/parking/oss/_index.md)

```markdown
---
title: Общие собрания собственников
description: Информация о проведённых и запланированных ОСС
building: parking
---

На этой странице размещается информация о проведённых и запланированных общих собраниях собственников помещений паркинга.
```

### ОСС — конкретное собрание (content/parking/oss/01-2025/_index.md)

```markdown
---
title: ОСС Январь 2025
date: 2025-01-20
building: parking
status: planned  # planned | voting | completed
votingStart: 2025-01-20
votingEnd: 2025-02-20
---

Общее собрание собственников помещений паркинга, январь 2025 года.

Форма голосования: очно-заочная.
```

### ОСС — повестка (content/parking/oss/01-2025/agenda.md)

```markdown
---
title: Повестка собрания
date: 2025-01-15
building: parking
ossId: 01-2025
type: agenda
---

## Вопросы повестки

1. Избрание председателя и секретаря собрания
2. Утверждение сметы на 2025 год
3. Выбор способа управления общим имуществом
4. Разное
```

### ОСС — результаты (content/parking/oss/01-2025/results.md)

```markdown
---
title: Результаты голосования
date: 2025-02-21
building: parking
ossId: 01-2025
type: results
---

## Итоги голосования

| Вопрос | За | Против | Воздержались | Решение |
|--------|-----|--------|--------------|---------|
| Вопрос 1 | 75% | 10% | 15% | Принято |
| Вопрос 2 | 82% | 8% | 10% | Принято |
```

### ОСС — протокол (content/parking/oss/01-2025/protocol.md)

```markdown
---
title: Протокол собрания
date: 2025-02-25
building: parking
ossId: 01-2025
type: protocol
file: /files/parking/oss/01-2025/protocol.pdf
fileSize: "2.1 MB"
---

Протокол общего собрания собственников помещений паркинга от 20.01.2025 — 20.02.2025.
```

### FAQ (content/parking/faq.md)

```markdown
---
title: Частые вопросы
description: Ответы на часто задаваемые вопросы по паркингу
building: parking
layout: faq
---

## Оплата

### Как оплатить парковочное место?

Оплату можно произвести:
- Через личный кабинет DOMA.AI
- По реквизитам банковским переводом
- По QR-коду

### Когда нужно вносить оплату?

Оплата вносится ежемесячно до 10 числа текущего месяца.

## Доступ

### Как получить пульт от ворот?

Обратитесь в правление ТСН. Стоимость пульта — 2000 ₽.

### Что делать если пульт не работает?

Позвоните диспетчеру или напишите в Telegram-чат.

## Правила

### Можно ли мыть машину на паркинге?

Мойка автомобилей на территории паркинга запрещена.
```

### Тарифы (content/parking/tariffs.md)

```markdown
---
title: Тарифы
description: Действующие тарифы и взносы
building: parking
---

## Действующие тарифы

*С 1 января 2025 года*

| Услуга | Тариф | Единица |
|--------|-------|---------|
| Содержание машино-места | 3 500 ₽ | мес. |
| Капитальный ремонт | 500 ₽ | мес. |
| Дополнительный пульт | 2 000 ₽ | шт. |

## История изменений

### 2024
- С 01.01.2024: содержание — 3 200 ₽/мес.

### 2023
- С 01.01.2023: содержание — 3 000 ₽/мес.
```

### Контакты (content/parking/contacts.md)

```markdown
---
title: Контакты
description: Контактная информация ТСН
building: parking
---

## ТСН «Гаражный комплекс «Лайф Паркинг»»

**Адрес:** г. Москва, ул. Чистова, д. 16

**Диспетчерская:** [будет заполнено]

**Личный кабинет:** [будет заполнено]

## Реквизиты для оплаты

[Будут добавлены после заполнения data/tsn.yaml]

## Связь

- Telegram-канал: [будет заполнено]
- Чат жителей: [будет заполнено]
```

## Дизайн (style.css)

### Концепция дизайна

**Стиль: Apple Design Language + doma.ai**

Сайт должен выглядеть как современный продукт Apple:
- Чистый, минималистичный интерфейс
- Много "воздуха" (white space)
- Плавные микро-анимации
- Акцент на типографике
- Ощущение премиальности и надёжности

**Референсы:**
- apple.com — общий подход к layout, типографика, анимации
- doma.ai — цветовая схема, стиль карточек, подача информации для ЖКХ

### Цветовая схема (по аналогии с doma.ai)

```css
:root {
  /* === Основные цвета (doma.ai style) === */
  --color-primary: #10B981;           /* Зелёный — основной акцент */
  --color-primary-hover: #059669;     /* Зелёный при наведении */
  --color-primary-light: #D1FAE5;     /* Светло-зелёный фон */
  --color-primary-gradient: linear-gradient(135deg, #10B981 0%, #059669 100%);
  
  /* === Нейтральные цвета === */
  --color-bg: #FFFFFF;                /* Чисто белый фон (как Apple) */
  --color-bg-secondary: #F9FAFB;      /* Светло-серый для секций */
  --color-bg-tertiary: #F3F4F6;       /* Ещё светлее для карточек */
  --color-surface: #FFFFFF;           /* Поверхность карточек */
  
  /* === Текст === */
  --color-text: #1F2937;              /* Основной текст (почти чёрный) */
  --color-text-secondary: #6B7280;    /* Вторичный текст */
  --color-text-tertiary: #9CA3AF;     /* Подписи, мета-информация */
  --color-text-inverse: #FFFFFF;      /* Белый текст на тёмном фоне */
  
  /* === Границы и разделители === */
  --color-border: #E5E7EB;            /* Основная граница */
  --color-border-light: #F3F4F6;      /* Лёгкая граница */
  
  /* === Цвета корпусов (для badge) === */
  --color-parking: #6B7280;           /* Серый — паркинг */
  --color-k1: #3B82F6;                /* Синий — корпус 1 */
  --color-k2: #10B981;                /* Зелёный — корпус 2 */
  --color-external: #9CA3AF;          /* Серый — внешние УК */
  
  /* === Семантические цвета === */
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;
  
  /* === Геометрия (Apple-style) === */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;              /* Пилюли, badge */
  
  /* === Тени (мягкие, как у Apple) === */
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --shadow-card: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-card-hover: 0 8px 24px rgba(0, 0, 0, 0.12);
  
  /* === Типографика (Apple San Francisco stack) === */
  --font-sans: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', 'Segoe UI', system-ui, sans-serif;
  
  /* === Размеры шрифтов (Apple-style scale) === */
  --text-xs: 0.75rem;     /* 12px */
  --text-sm: 0.875rem;    /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  --text-4xl: 2.25rem;    /* 36px */
  --text-5xl: 3rem;       /* 48px */
  --text-6xl: 3.75rem;    /* 60px — hero заголовки */
  
  /* === Отступы (8px grid) === */
  --space-1: 0.25rem;     /* 4px */
  --space-2: 0.5rem;      /* 8px */
  --space-3: 0.75rem;     /* 12px */
  --space-4: 1rem;        /* 16px */
  --space-6: 1.5rem;      /* 24px */
  --space-8: 2rem;        /* 32px */
  --space-12: 3rem;       /* 48px */
  --space-16: 4rem;       /* 64px */
  --space-20: 5rem;       /* 80px */
  --space-24: 6rem;       /* 96px */
  
  /* === Анимации (плавные, как у Apple) === */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  
  /* === Контейнер === */
  --container-max: 1280px;
}
```

### Ключевые принципы дизайна

#### 1. Типографика (Apple-style)

```css
/* Заголовки — жирные, с плотным межстрочным интервалом */
h1 {
  font-size: var(--text-5xl);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.025em;  /* Плотнее для крупных заголовков */
}

/* Основной текст — комфортный для чтения */
body {
  font-size: var(--text-base);
  line-height: 1.6;
  letter-spacing: -0.01em;
  -webkit-font-smoothing: antialiased;
}
```

#### 2. Карточки (Apple-style с hover)

```css
.card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow-card);
  transition: transform var(--transition-base) var(--ease-out-expo),
              box-shadow var(--transition-base) var(--ease-out-expo);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card-hover);
}
```

#### 3. Навигация (прозрачная с blur, как у Apple)

```css
.nav {
  position: sticky;
  top: 0;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid var(--color-border-light);
  z-index: 100;
}
```

#### 4. Кнопки (doma.ai style)

```css
/* Основная кнопка — зелёная */
.btn-primary {
  background: var(--color-primary);
  color: white;
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-full);
  font-weight: 500;
  transition: all var(--transition-fast);
}

.btn-primary:hover {
  background: var(--color-primary-hover);
  transform: scale(1.02);
}
```

#### 5. Hero-секция

```css
.hero {
  padding: var(--space-24) 0;
  text-align: center;
  background: linear-gradient(180deg, var(--color-bg) 0%, var(--color-bg-secondary) 100%);
}

.hero__title {
  font-size: var(--text-6xl);
  font-weight: 700;
  background: var(--color-primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

#### 6. Badge для корпусов

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: 500;
  color: white;
}

.badge--parking { background: var(--color-parking); }
.badge--k1 { background: var(--color-k1); }
.badge--k2 { background: var(--color-k2); }
```

#### 7. Анимации появления

```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.6s var(--ease-out-expo) forwards;
}
```

### Чек-лист дизайна

- [ ] Навигация с blur-эффектом (sticky)
- [ ] Hero-секция с градиентным текстом
- [ ] Карточки корпусов с hover-эффектом подъёма
- [ ] Цветовые badge для маркировки корпусов
- [ ] Плавные переходы на всех интерактивных элементах
- [ ] Много белого пространства между секциями (80-96px)
- [ ] Скруглённые углы (16-24px для карточек)
- [ ] Мягкие тени без резких границ
- [ ] Типографика с отрицательным letter-spacing для заголовков
- [ ] Консистентная 8px сетка для отступов
- [ ] Mobile-first responsive (1 колонка → 2 → 3-4)

## GitHub (работа через CLI)

### Требования

**Вся работа с GitHub ведётся через GitHub CLI (`gh`)**, а не через веб-интерфейс или git remote commands.

### Первичная настройка репозитория

```bash
# Создать репозиторий на GitHub
gh repo create chistova16-site --public --source=. --remote=origin

# Или если репозиторий уже существует — клонировать
gh repo clone <username>/chistova16-site
```

### Настройка секретов для деплоя

```bash
# Добавить секреты для Yandex Object Storage
gh secret set YC_ACCESS_KEY --body "<your-access-key>"
gh secret set YC_SECRET_KEY --body "<your-secret-key>"

# Проверить список секретов
gh secret list
```

### Работа с репозиторием

```bash
# Посмотреть статус workflow
gh run list

# Посмотреть логи последнего деплоя
gh run view --log

# Запустить деплой вручную
gh workflow run deploy.yml

# Создать Pull Request
gh pr create --title "feat: add FAQ section" --body "Добавлен раздел FAQ"

# Посмотреть issues
gh issue list
```

### GitHub (работа через CLI)

### Требования

**Вся работа с GitHub ведётся через GitHub CLI (`gh`)**, а не через веб-интерфейс или git remote commands.

### Первичная настройка репозитория

```bash
# Создать репозиторий на GitHub
gh repo create chistova16-site --public --source=. --remote=origin

# Или если репозиторий уже существует — клонировать
gh repo clone <username>/chistova16-site
```

### Настройка секретов для деплоя

```bash
# Добавить секреты для Yandex Object Storage
gh secret set YC_ACCESS_KEY --body "<your-access-key>"
gh secret set YC_SECRET_KEY --body "<your-secret-key>"

# Проверить список секретов
gh secret list
```

### Работа с репозиторием

```bash
# Посмотреть статус workflow
gh run list

# Посмотреть логи последнего деплоя
gh run view --log

# Запустить деплой вручную
gh workflow run deploy.yml

# Создать Pull Request
gh pr create --title "feat: add FAQ section" --body "Добавлен раздел FAQ"

# Посмотреть issues
gh issue list
```

### GitHub Actions (deploy.yml)

```yaml
name: Deploy to Yandex Object Storage

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'
          extended: true
      
      - name: Build
        run: hugo --minify
      
      - name: Configure AWS CLI
        run: |
          aws configure set aws_access_key_id ${{ secrets.YC_ACCESS_KEY }}
          aws configure set aws_secret_access_key ${{ secrets.YC_SECRET_KEY }}
          aws configure set default.region ru-central1
      
      - name: Deploy to S3
        run: |
          aws s3 sync public/ s3://chistova16.ru \
            --endpoint-url=https://storage.yandexcloud.net \
            --delete \
            --cache-control "max-age=3600"
```

## hugo.toml

```toml
baseURL = 'https://chistova16.ru/'
languageCode = 'ru-ru'
title = 'ЖК «Волжская Life»'

[params]
  description = 'Информационный портал ЖК «Волжская Life»'
  address = 'г. Москва, ул. Чистова, д. 16'

[menu]
  [[menu.main]]
    name = 'Новости'
    url = '/news/'
    weight = 1
  [[menu.main]]
    name = 'Паркинг'
    url = '/parking/'
    weight = 2
  [[menu.main]]
    name = 'Корпус 1'
    url = '/k1/'
    weight = 3
  [[menu.main]]
    name = 'Корпус 2'
    url = '/k2/'
    weight = 4
  [[menu.main]]
    name = 'О комплексе'
    url = '/about/'
    weight = 5

[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true

[outputs]
  home = ['HTML', 'RSS']
  section = ['HTML', 'RSS']

[taxonomies]
  tag = 'tags'
  building = 'buildings'
```

## README.md

Включи разделы:

### Локальный запуск
```bash
hugo server -D
# Откроется http://localhost:1313
```

### Добавление новости
```bash
hugo new parking/news/YYYY-MM-DD-название.md
# Отредактировать файл
git add . && git commit -m "news: новая новость" && git push

# Посмотреть статус деплоя
gh run watch
```

### Добавление документа
1. Положить PDF в `static/files/parking/`
2. Создать `content/parking/docs/название.md`
3. Указать путь к файлу в frontmatter

### Добавление отчёта
```bash
hugo new parking/reports/YYYY-QN.md
```

### Создание нового ОСС
```bash
# Создать директорию
mkdir -p content/parking/oss/MM-YYYY

# Создать файлы
hugo new parking/oss/MM-YYYY/_index.md
hugo new parking/oss/MM-YYYY/agenda.md
hugo new parking/oss/MM-YYYY/results.md
hugo new parking/oss/MM-YYYY/protocol.md
```

### Деплой (через GitHub CLI)

```bash
# Пуш в main запускает деплой автоматически
git push origin main

# Следить за деплоем в реальном времени
gh run watch

# Запустить деплой вручную
gh workflow run deploy.yml

# Посмотреть логи последнего запуска
gh run view --log-failed
```

### Структура frontmatter

Для каждого типа контента описать обязательные и опциональные поля.

## Acceptance Criteria

```
GIVEN пустой репозиторий
WHEN выполнен промт в Claude Code
THEN создан Hugo-проект со всеми файлами

GIVEN локальный запуск `hugo server`
WHEN открыта главная страница
THEN отображаются карточки всех корпусов с правильной маркировкой

GIVEN карточка корпуса 3-7
WHEN клик по карточке
THEN открывается внешний сайт УК в новой вкладке

GIVEN страница /news/
WHEN загрузка страницы
THEN отображаются новости из всех корпусов с badge

GIVEN страница /parking/oss/
WHEN загрузка страницы
THEN отображается список собраний с датами и статусами

GIVEN страница /parking/faq/
WHEN загрузка страницы
THEN отображаются вопросы сгруппированные по категориям

GIVEN push в main
WHEN GitHub Actions завершён
THEN сайт опубликован на chistova16.ru
```

## Примечания

- QR-коды для оплаты — placeholder изображения, заменить позже
- Реквизиты ТСН «Лайф Паркинг» и «Лайф 1» — TODO в data/tsn.yaml
- Favicon — создать placeholder
- Схема ЖК (map-jk.png) — placeholder, заменить позже
