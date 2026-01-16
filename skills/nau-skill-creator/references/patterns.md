# Паттерны Skills

Проверенные паттерны структуры и вывода для эффективных skills.

## Паттерны структуры SKILL.md

### 1. Workflow-Based

**Когда:** Последовательные процессы с чёткими шагами.

```markdown
# PDF Form Filler

## Overview
[1-2 sentences]

## Workflow

1. Analyze form → run `analyze_form.py`
2. Create field mapping → edit `fields.json`
3. Validate mapping → run `validate_fields.py`
4. Fill form → run `fill_form.py`
5. Verify output → run `verify_output.py`

## Step Details
[Details per step as needed]
```

**Примеры:** DOCX skill, PDF processing, data pipelines.

### 2. Task-Based

**Когда:** Коллекция независимых операций.

```markdown
# Image Editor

## Quick Start
[Basic usage]

## Tasks

### Resize Image
[Instructions]

### Convert Format
[Instructions]

### Apply Filters
[Instructions]
```

**Примеры:** Image tools, file converters, utilities.

### 3. Reference-Based

**Когда:** Стандарты, гайдлайны, спецификации.

```markdown
# Brand Guidelines

## Overview
[What this covers]

## Colors
[Color specifications]

## Typography
[Font rules]

## Logo Usage
[Guidelines]
```

**Примеры:** Brand guidelines, coding standards, policies.

### 4. Capabilities-Based

**Когда:** Интегрированная система с связанными фичами.

```markdown
# Product Management

## Core Capabilities

### 1. Context Building
[Description and process]

### 2. Communication
[Description and process]

### 3. Planning
[Description and process]
```

**Примеры:** PM tools, integrated systems.

## Паттерны Progressive Disclosure

### High-level guide + references

```markdown
# PDF Processing

## Quick start
[Basic example]

## Advanced features
- **Form filling**: See `references/forms.md`
- **API reference**: See `references/api.md`
- **Examples**: See `references/examples.md`
```

### Domain-specific organization

```markdown
# Finance Skill

## Common queries
[Basic patterns]

## Domain-specific
- **Accounting**: See `references/accounting.md`
- **Reporting**: See `references/reporting.md`
```

## Паттерны вывода

### Template Pattern (строгий)

Для API responses, data formats, строгих требований:

```markdown
## Report structure

ALWAYS use this exact template:

# [Analysis Title]

## Executive summary
[One-paragraph overview]

## Key findings
- Finding 1 with data
- Finding 2 with data

## Recommendations
1. Actionable recommendation
2. Actionable recommendation
```

### Template Pattern (гибкий)

Для адаптивного вывода:

```markdown
## Report structure

Sensible default, use judgment:

# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt based on what you discover]

## Recommendations
[Tailor to context]

Adjust sections as needed.
```

### Examples Pattern

Когда качество зависит от примеров:

```markdown
## Commit message format

**Example 1:**
Input: Added user authentication with JWT
Output:
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware

**Example 2:**
Input: Fixed date display bug in reports
Output:
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently

Follow this style: type(scope): brief, then detailed explanation.
```

## Паттерны Conditional Workflows

```markdown
## Processing workflow

1. Determine modification type:
   - **Creating new?** → Follow "Creation workflow"
   - **Editing existing?** → Follow "Editing workflow"

### Creation workflow
[steps]

### Editing workflow  
[steps]
```

## Комбинирование паттернов

Большинство skills комбинируют паттерны:

| Комбинация | Применение |
|------------|------------|
| Task-Based + Workflow | Утилиты со сложными операциями |
| Reference + Examples | Стандарты с примерами применения |
| Capabilities + Progressive Disclosure | Большие системы с детальной документацией |
