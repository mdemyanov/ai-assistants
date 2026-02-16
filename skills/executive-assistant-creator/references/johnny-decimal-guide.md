# Johnny Decimal Guide для AI-ассистента руководителя

**Версия:** 1.0.0
**Обновлено:** 2026-02-16

---

## Что такое Johnny Decimal?

Johnny Decimal — это система организации информации, где каждая категория получает уникальный номер от 00 до 99. Система создаёт предсказуемую иерархию и упрощает навигацию.

**Ключевой принцип:** Любой файл в системе можно найти по его номеру без поиска.

### Базовая структура

```
00-09 — Метауровень (ядро системы)
10-19 — Категория 1
20-29 — Категория 2
30-39 — Категория 3
...
90-99 — Служебное (шаблоны, архив)
```

---

## Johnny Decimal для C-level руководителя

Для руководителей система адаптирована под **workflow управления**: люди, встречи, проекты, решения, знания, домен.

### Универсальное ядро (00-59)

Эта структура **одинакова для всех ролей** (CTO, CPO, COO, HR, PM):

| Диапазон | Папка | Содержимое | Примеры файлов |
|----------|-------|-----------|----------------|
| **00-09** | `00_CORE/` | Идентичность, стратегия, стейкхолдеры | `identity/role_scope.md`, `strategy/current_priorities.md`, `stakeholders/key_stakeholders.md` |
| **10-19** | `10_PEOPLE/` | Люди, профили, 1-1 встречи | `{id}/profile.md`, `{id}/1-1/{date}.md` |
| **20-29** | `20_MEETINGS/` | Регулярные встречи, комитеты | `committees/{name}/{date}.md`, `standups/{date}.md` |
| **30-39** | `30_PROJECTS/` | Проекты и инициативы | `active/{id}/INDEX.md`, `backlog/{id}.md`, `archive/{id}.md` |
| **40-49** | `40_DECISIONS/` | ADR, политики, decision journal | `adr/{id}.md`, `policies/{name}.md`, `journal/{date}.md` |
| **50-59** | `50_KNOWLEDGE/` | Методологии, процессы, глоссарий | `methodologies/{name}.md`, `processes/{name}.md`, `glossary.md` |

### Доменные модули (60-89)

Эта часть **адаптируется под роль**:

| Роль | Папка | Содержимое |
|------|-------|-----------|
| **CTO** | `60_DOMAIN/technology/` | Платформы, продукты, tech stack, архитектура |
| **CPO** | `60_DOMAIN/product/` | Roadmaps, research, метрики продукта |
| **COO** | `60_DOMAIN/operations/` | Процессы, SLA, вендоры, KPI операций |
| **CFO** | `60_DOMAIN/finance/` | Бюджеты, отчётность, forecasts |
| **HR** | `60_DOMAIN/hr/` | Политики HR, программы развития, компетенции |
| **PM/PMO** | `60_DOMAIN/projects/` | Портфолио проектов, методологии PM, риски |

**Примечание:** Доменных модулей может быть несколько. Например, CTO может иметь как `60_DOMAIN/technology/`, так и `70_DOMAIN/innovation/`.

### Служебные папки (90-99)

| Диапазон | Папка | Содержимое |
|----------|-------|-----------|
| **90-99** | `90_TEMPLATES/` | Шаблоны документов |
| **90-99** | `99_ARCHIVE/` | Архив завершённого |

---

## Преимущества для руководителя

### 1. Предсказуемость

Вы **всегда знаете**, где находится информация:
- Профиль человека → `10_PEOPLE/{id}/profile.md`
- 1-1 встреча → `10_PEOPLE/{id}/1-1/{date}.md`
- Решение → `40_DECISIONS/adr/{id}.md`
- Проект → `30_PROJECTS/active/{id}/INDEX.md`

### 2. Масштабируемость

Система растёт вместе с вами:
- Новый человек → создать папку в `10_PEOPLE/`
- Новый проект → создать папку в `30_PROJECTS/active/`
- Новый домен → добавить `70_DOMAIN/{subdomain}/`

### 3. Кроссфункциональность

Одна система работает для **любой роли** (CTO, CPO, COO, HR, PM). Меняется только доменный модуль (60-89).

### 4. AI-friendly

AI легко понимает структуру:
```
# AI видит pattern
10_PEOPLE/{id}/profile.md → профиль человека
10_PEOPLE/{id}/1-1/{date}.md → записи встреч
```

---

## Примеры адаптации под роли

### CTO (Chief Technology Officer)

```
00_CORE/                # Идентичность: роль CTO, полномочия, ограничения
10_PEOPLE/              # Команда: tech leads, архитекторы, разработчики
20_MEETINGS/            # Комитеты: Tech Council, Architecture Review
30_PROJECTS/            # Проекты: миграции, новые платформы, refactoring
40_DECISIONS/           # ADR: архитектурные решения
50_KNOWLEDGE/           # Методологии: DDD, Arc42, TOGAF
60_DOMAIN/technology/   # Платформы: SMP, integrations, infrastructure
  ├── platforms/
  ├── products/
  ├── architecture/
  └── tech_stack/
90_TEMPLATES/           # Шаблоны: ADR, RFT, Tech Spec
```

### CPO (Chief Product Officer)

```
00_CORE/                # Идентичность: роль CPO, product vision
10_PEOPLE/              # Команда: PM, designers, researchers
20_MEETINGS/            # Комитеты: Product Council, Roadmap Review
30_PROJECTS/            # Проекты: новые features, улучшения UX
40_DECISIONS/           # Решения: product decisions, trade-offs
50_KNOWLEDGE/           # Методологии: Jobs to Be Done, OKR, RICE
60_DOMAIN/product/      # Продукты: roadmaps, metrics, research
  ├── roadmaps/
  ├── research/
  ├── metrics/
  └── customer_feedback/
90_TEMPLATES/           # Шаблоны: PRD, User Story, Research Brief
```

### COO (Chief Operating Officer)

```
00_CORE/                # Идентичность: роль COO, operational scope
10_PEOPLE/              # Команда: операционные менеджеры, процессоры
20_MEETINGS/            # Комитеты: Ops Review, Process Improvement
30_PROJECTS/            # Проекты: оптимизация процессов, автоматизация
40_DECISIONS/           # Решения: SLA changes, vendor selection
50_KNOWLEDGE/           # Методологии: Lean, Six Sigma, ITIL
60_DOMAIN/operations/   # Операции: процессы, metrics, vendors
  ├── processes/
  ├── sla/
  ├── vendors/
  └── kpi/
90_TEMPLATES/           # Шаблоны: SOP, Процесс, Метрика
```

### HR Director

```
00_CORE/                # Идентичность: роль HR Director, HR strategy
10_PEOPLE/              # Расширенное использование: все сотрудники компании
20_MEETINGS/            # Комитеты: HR Council, Talent Review
30_PROJECTS/            # Проекты: программы развития, изменения в HR
40_DECISIONS/           # Решения: политики, компенсации
50_KNOWLEDGE/           # Методологии: Competency Framework, OKR
60_DOMAIN/hr/           # HR: политики, программы, компетенции
  ├── policies/
  ├── programs/
  ├── competencies/
  └── compensation/
90_TEMPLATES/           # Шаблоны: Job Description, Performance Review
```

### PM/PMO (Project Manager / PMO Lead)

```
00_CORE/                # Идентичность: роль PM, scope управления проектами
10_PEOPLE/              # Команда: project managers, stakeholders
20_MEETINGS/            # Комитеты: PMO Council, Portfolio Review
30_PROJECTS/            # Расширенное использование: портфолио проектов
40_DECISIONS/           # Решения: project approvals, scope changes
50_KNOWLEDGE/           # Методологии: PMBOK, Agile, Critical Chain
60_DOMAIN/projects/     # Портфолио: методологии PM, риски, lessons learned
  ├── portfolio/
  ├── methodologies/
  ├── risks/
  └── lessons_learned/
90_TEMPLATES/           # Шаблоны: Project Charter, Risk Register, Status Report
```

---

## Миграция со старой структуры (01-07)

Если вы используете структуру **v1.1.0** (01-07), вот план миграции:

### Mapping старой структуры на новую

| Старая (v1.1.0) | Новая (v2.0.0) | Примечания |
|-----------------|----------------|------------|
| `01_CONTEXT/` | `00_CORE/` | Переименовать + реструктурировать |
| `02_DOMAIN/` | `60_DOMAIN/{subdomain}/` | Добавить subdomain |
| `03_METHODOLOGY/` | `50_KNOWLEDGE/methodologies/` | Переместить |
| `04_TEMPLATES/` | `90_TEMPLATES/` | Переименовать |
| `05_DECISIONS/` | `40_DECISIONS/` | Переименовать |
| `06_CURRENT/` | `00_CORE/strategy/` | Интегрировать в CORE |
| `07_PEOPLE/` | `10_PEOPLE/` | Переименовать |
| *Нет* | `20_MEETINGS/` | **НОВОЕ** — создать |
| *Нет* | `30_PROJECTS/` | **НОВОЕ** — создать |

### Пошаговая миграция

**Шаг 1: Backup**
```bash
cp -r /path/to/vault /path/to/vault_backup_$(date +%Y%m%d)
```

**Шаг 2: Создать новую структуру**
```bash
cd /path/to/vault
mkdir -p 00_CORE/{identity,stakeholders,strategy}
mkdir -p 10_PEOPLE
mkdir -p 20_MEETINGS/{committees,standups}
mkdir -p 30_PROJECTS/{active,backlog,archive}
mkdir -p 40_DECISIONS/{adr,policies,journal}
mkdir -p 50_KNOWLEDGE/{methodologies,processes}
mkdir -p 60_DOMAIN/{subdomain}  # Замените {subdomain} на ваш домен
mkdir -p 90_TEMPLATES
mkdir -p 99_ARCHIVE
```

**Шаг 3: Переместить файлы**
```bash
# 01_CONTEXT → 00_CORE
mv 01_CONTEXT/role_scope.md 00_CORE/identity/
mv 01_CONTEXT/constraints.md 00_CORE/identity/
mv 01_CONTEXT/stakeholders.md 00_CORE/stakeholders/key_stakeholders.md

# 02_DOMAIN → 60_DOMAIN
mv 02_DOMAIN 60_DOMAIN/technology  # Для CTO

# 03_METHODOLOGY → 50_KNOWLEDGE
mv 03_METHODOLOGY 50_KNOWLEDGE/methodologies

# 04_TEMPLATES → 90_TEMPLATES
mv 04_TEMPLATES 90_TEMPLATES

# 05_DECISIONS → 40_DECISIONS
mv 05_DECISIONS 40_DECISIONS

# 06_CURRENT → 00_CORE/strategy
mv 06_CURRENT/priorities.md 00_CORE/strategy/current_priorities.md

# 07_PEOPLE → 10_PEOPLE
mv 07_PEOPLE 10_PEOPLE
```

**Шаг 4: Обновить ссылки**

Найти и заменить внутренние ссылки в markdown файлах:
```bash
# Найти все ссылки на старую структуру
grep -r "\[\[01_CONTEXT" .
grep -r "\[\[02_DOMAIN" .
# ... и т.д.

# Заменить (вручную или через sed)
# Пример для sed (macOS):
find . -type f -name "*.md" -exec sed -i '' 's/01_CONTEXT/00_CORE/g' {} +
find . -type f -name "*.md" -exec sed -i '' 's/07_PEOPLE/10_PEOPLE/g' {} +
```

**Шаг 5: Обновить CLAUDE.md**

Обновить секцию "Структура базы знаний" в CLAUDE.md на новую (00-99).

**Шаг 6: Переиндексировать aigrep**
```bash
# Если используете aigrep
aigrep reindex --vault "Your_Vault_Name"
```

**Шаг 7: Проверка**
```bash
# Убедиться что все файлы перемещены
ls -la 00_CORE/
ls -la 10_PEOPLE/
ls -la 20_MEETINGS/
ls -la 30_PROJECTS/
ls -la 40_DECISIONS/
ls -la 50_KNOWLEDGE/
ls -la 60_DOMAIN/
ls -la 90_TEMPLATES/

# Удалить старые папки (ОСТОРОЖНО!)
# rm -rf 01_CONTEXT 02_DOMAIN 03_METHODOLOGY 04_TEMPLATES 05_DECISIONS 06_CURRENT 07_PEOPLE
```

---

## Path Patterns для новой структуры

Для автоматизации и AI-контекста используйте эти паттерны:

```yaml
# Vault
vault_name: "{Role}_Vault"  # Например: CTO_Vault, CPO_Vault

# Директории
people_dir: "10_PEOPLE"
meetings_dir: "20_MEETINGS"
projects_dir: "30_PROJECTS"
decisions_dir: "40_DECISIONS"
knowledge_dir: "50_KNOWLEDGE"
domain_dir: "60_DOMAIN"
templates_dir: "90_TEMPLATES"
archive_dir: "99_ARCHIVE"

# Path patterns
profile: "{people_dir}/{id}/profile.md"
one_on_one: "{people_dir}/{id}/1-1/{date}.md"
one_on_one_agenda: "{people_dir}/{id}/1-1/{date}_agenda.md"
project: "{projects_dir}/active/{id}/INDEX.md"
adr: "{decisions_dir}/adr/{id}.md"
policy: "{decisions_dir}/policies/{name}.md"
committee_meeting: "{meetings_dir}/committees/{name}/{date}.md"
```

---

## FAQ

### Можно ли использовать другую нумерацию?

Да, но **не рекомендуется**. Johnny Decimal — это стандарт, который:
- Узнаваем другими людьми
- Имеет community и ресурсы
- Хорошо документирован

### Что если у меня несколько доменов?

Используйте несколько папок в диапазоне 60-89:
```
60_DOMAIN/technology/
70_DOMAIN/innovation/
80_DOMAIN/research/
```

### Можно ли добавить свои категории?

Да, но **только в служебные диапазоны** (90-99) или доменные (60-89). Универсальное ядро (00-59) менять **не рекомендуется** — это стандарт для всех ролей.

### Как организовать файлы внутри папок?

Внутри папок (например, `10_PEOPLE/{id}/`) используйте свободную структуру без номеров:
```
10_PEOPLE/vshadrin/
├── profile.md
├── 1-1/
│   ├── 2026-01-15.md
│   └── 2026-01-22.md
├── feedback/
│   └── 2026_q1.md
└── notes.md
```

### Нужно ли мигрировать существующий vault?

Зависит от размера:
- **<100 файлов** → да, миграция займёт ~1-2 часа
- **100-500 файлов** → опционально, можно делать постепенно
- **>500 файлов** → не обязательно, используйте новую структуру только для новых файлов

---

## Дополнительные ресурсы

- [Johnny.Decimal official site](https://johnnydecimal.com/)
- [CLAUDE.md template](../templates/claude-md-template.md) — шаблон с интеграцией Johnny Decimal
- [System Prompt template](../templates/system-prompt-template.md) — шаблон системного промта

---

*Версия 1.0.0 — Создан 16.02.2026*
