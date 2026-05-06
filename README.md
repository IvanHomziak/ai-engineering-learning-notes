# AI Engineering Learning Notes

Персональний навчальний репозиторій для переходу з **Backend / Java Engineering** у напрям **AI Platform Engineering / LLM Infrastructure / AI Systems Engineering**.

Цей репозиторій зберігає навчальні нотатки, flashcards, weekly reviews, шаблони й матеріали для щоденного повторення. Формат — звичайні Markdown-файли, які зручно відкривати в **Obsidian**, версіонувати через Git і пізніше автоматизувати Python-скриптами.

## Основні цілі

- Побудувати довгострокову інженерну базу знань з AI Engineering.
- Зберігати матеріали у Markdown, сумісному з Obsidian.
- Версіонувати навчання через Git.
- Генерувати flashcards для Anki або іншої spaced-repetition системи.
- Відстежувати слабкі місця, повторення й weekly consolidation.
- Поступово перетворити навчальний процес у portfolio-friendly AI automation project.

## Структура репозиторію

```text
00_Index/                  Головні індекси, roadmap і dashboard повторення
01_LangChain/              Нотатки по LangChain, LCEL, chains, tools, agents
02_Python/                 Python fundamentals, async, backend/AI tooling
03_RAG/                    Retrieval-Augmented Generation
04_Agents/                 AI agents, tools, LangGraph, orchestration
05_LLM_Gateway/            Архітектура LLM Gateway
06_Spring_AI/              Spring AI для Java/Spring екосистеми
07_AI_Platform/            AI Platform Engineering topics
08_Production_LLM/         Observability, evaluation, cost, security, reliability
09_Interview_Preparation/  Interview Q&A, system design, role preparation
Weekly_Reviews/            Weekly summaries і knowledge gap analysis
Flashcards/                CSV-файли для Anki / repetition tools
templates/                 Повторно використовувані шаблони нотаток
scripts/                   Допоміжні скрипти для автоматизації
```

## Щоденний workflow

1. Після уроку або практики створи одну atomic note для конкретної теми.
2. Використовуй шаблон `templates/daily-review-note-template.md`.
3. Поклади файл у правильну папку, наприклад `01_LangChain/`.
4. Додай metadata: topic, tags, status, review dates.
5. Додай flashcards у `Flashcards/`, якщо тема містить важливі терміни.
6. Раз на тиждень створи weekly review у `Weekly_Reviews/`.

## Рекомендований Obsidian setup

Відкрий кореневу папку цього репозиторію як Obsidian Vault:

```text
Obsidian → Open folder as vault → ai-engineering-learning-notes
```

## Правило якості нотаток

Кожна навчальна нотатка має відповідати на питання:

- що це таке;
- навіщо існує;
- як працює;
- як це повʼязано з backend / distributed systems / AI platform;
- які production-ризики;
- які типові помилки;
- як пояснити це на interview;
- яку маленьку практичну задачу можна зробити.

## Принцип

```text
Не накопичувати хаотичні конспекти.
Будувати інженерну систему повторення знань.
```
