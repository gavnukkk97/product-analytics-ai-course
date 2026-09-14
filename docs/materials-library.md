# Публичная библиотека материалов (внутренняя библиотека курса)

**Роль:** самодостаточность курса. Студент закрывает базу **внутри** уроков + `docs/uploads/`; уход на Medium/LinkedIn — опция, не обязательный шаг.  
Кураторский слой поверх инвентарей. Для писателей уроков и блока «Дальше читать» (= углубление в библиотеке курса).  
Проверка / discovery: **13–14 сентября 2026**. Язык предпочтения: **RU first**. Paywall не обходим.

| Связанные доки | Роль |
|---|---|
| [`uploads/README.md`](./uploads/README.md) | **внутренняя библиотека** md (kir, 2026-09-14) — читать из курса |
| [`lessons/`](./lessons/) | тела уроков: концепции уже вшиты; uploads — углубление |
| [`../internal/article-weave-map.md`](../internal/article-weave-map.md) | карта upload → модуль → статус weave |
| [`../internal/stats-ab-weave.md`](../internal/stats-ab-weave.md) | карта stats-ab-course → М2.4/М2.5 |
| [`medium-linkedin-sources.md`](./medium-linkedin-sources.md) | оценка семёрки kir + discovery |
| [`medium-download-wishlist.md`](./medium-download-wishlist.md) | wishlist (закрыт выгрузкой) |
| [`ux-sources.md`](./ux-sources.md) | М4.* детально |
| [`sql-python-sources.md`](./sql-python-sources.md) | М3.* канон SQL/Python |
| [`sources-inventory.md`](./sources-inventory.md) | полный корпус (Красинский, TG, GoPractice, …) |
| [`course-structure.md`](./course-structure.md) | модули и вехи P1–P4 |
| [`full-course-gap-plan.md`](./full-course-gap-plan.md) | дыры полного 8-нед. календаря vs файлы |

**Легенда решения:** `keep` — можно цитировать/класть в библиотеку урока; `adapt` — взять кусок (чеклист, таблицу, рамку), не целиком; `skip` — не тащить в обязательный трек; `mirror` — Medium 403 → открытое зеркало; **`local`** — есть md в [`uploads/`](./uploads/); **`woven`** — концепт уже в теле урока (см. weave-map).

**Доступ из облака:** Medium часто **Cloudflare 403**; LinkedIn Pulse иногда открыт без логина, **посты** и часть Pulse — только с сессии. Поэтому **локальные копии в `uploads/` — основной способ самодостаточности**. Habr / vc.ru / GoPractice / Surf / Kariernik — обычно открыты (доп. якоря).

---

## 1. Топ-10 уже открытых — можно цитировать сразу

| # | Источник | Модули | Почему |
|---|---|---|---|
| 1 | [Surf — аналитика моб. приложений / tracking plan](https://surf.ru/analitika-mobilnyh-prilozhenij/) | **М4.3**, М3.1 | Таблица-контракт события: триггер, параметры, payload — каркас практики Ритма |
| 2 | [Habr — ИИ-аналитика, которая не галлюцинирует](https://habr.com/ru/articles/1066650/) | **М3.6**, М0.2 | Цифры в детерминированном коде; LLM только объясняет — канон AI-линии |
| 3 | [Habr — text-to-SQL ломается](https://habr.com/ru/articles/944010/) | **М3.6**, М3.5 | Таксономия ошибок схемы/JOIN/агрегаций — фон «поймай ложь» |
| 4 | [Beskov CustDev — зеркало vc.ru](https://vc.ru/marketing/53090-vvedenie-v-customer-development) | М1.1, М4.4 | Medium оригинал 403; зеркало стабильно |
| 5 | [GoPractice — юнит-экономика](https://gopractice.ru/product/unit-economics/) | **М1.3** | Когортный LTV vs CPA; рядом с Красинским |
| 6 | [GoPractice — дизайн A/B](https://gopractice.ru/data/design-ab-test/) + [гайд A/B](https://gopractice.ru/data/ab-tests-guide/) | **М2.5** | Гипотеза, MDE, sample size; literacy без Medium |
| 7 | [Habr — A/B: дизайн до старта](https://habr.com/ru/articles/996860/) | М2.5, М2.4 | Primary / guardrail / не «на недельку» |
| 8 | [Habr — события Яндекс Лавка](https://habr.com/ru/companies/yandex/articles/940728/) | М4.3, М5.5 | Процесс разметки, доверие к событиям, мониторинг |
| 9 | [Habr — продуктовый дашборд](https://habr.com/ru/articles/929770/) + [IBS — дашборд для руководителя](https://ibs.ru/media/kak-sdelat-dashbord-ponyatnym-dlya-rukovoditelya-bazovye-printsipy/) | **М5.2**, М5.1 | Структура health/funnels + 5–7 KPI для решения |
| 10 | [GoPractice — дашборд «здоровья»](https://gopractice.ru/insights/product-health-dashboard/) | М5.2, М5.1 | Acquisition / product / growth блоки без vendor-шума |

Дополнительно открыты и уже в каноне SQL: [Kariernik 15 запросов](https://kariernik.ru/blog/sql-zaprosy-dlya-produktovyh-analitikov), [Habr метрики на SQL](https://habr.com/ru/articles/1010980/), [Habr план самообразования ПА](https://habr.com/ru/articles/791300/), [Habr User flow](https://habr.com/ru/articles/1081360/), [vc.ru юнит-экономика привлечения](https://vc.ru/marketing/3052938-unit-ekonomika-privlecheniya-ltv-cac), [Kustov JTBD — ScrumTrek-зеркало](https://scrumtrek.ru/blog/product-management/2492/gajd-po-tehnike-jobs-to-be-done-jtbd/).

---

## 2. Внутренняя библиотека uploads (самодостаточность курса)

Wishlist закрыт: локальные md лежат в [`uploads/`](./uploads/). Инвентарь и атрибуция — [`uploads/README.md`](./uploads/README.md). Карта вшивания в уроки — [`../internal/article-weave-map.md`](../internal/article-weave-map.md).

**Как студент использует:**

1. Читает **тело урока** — там уже пересказ нужных концептов голосом Ритма / спирали.
2. При необходимости углубляется в 1–3 файла из `uploads/` по ссылкам «Дальше читать» (относительные пути `../uploads/…`).
3. Внешние URL (Medium и т.п.) — **опционально**; курс не требует выходить за paywall/403.

Тела статей в уроки не копируем; пиратские дампы курсов не используем. Атрибуция идей — в имени файла uploads и в weave-map.

### Карта: модуль → офлайн-копии

| Модуль | Локальные файлы (курс-пакет) | Урок |
|---|---|---|
| **М0.1** | [`uploads/medium-geoghegan-end-to-end-product-analytics-strategy.md`](./uploads/medium-geoghegan-end-to-end-product-analytics-strategy.md) | [`lessons/m0-1-contour.md`](./lessons/m0-1-contour.md) · **woven** |
| **М1.3** | [`uploads/bonus-gopractice-unit-economics.md`](./uploads/bonus-gopractice-unit-economics.md) · [`uploads/bonus-vcru-ltv-cac-unit-economics.md`](./uploads/bonus-vcru-ltv-cac-unit-economics.md) · [`uploads/medium-ki-unit-economics-one-day.md`](./uploads/medium-ki-unit-economics-one-day.md) · [`uploads/linkedin-min-finance-operators-guide-ltvcac.md`](./uploads/linkedin-min-finance-operators-guide-ltvcac.md) · (дубль Pulse) [`uploads/linkedin-ki-unit-economics-one-day.md`](./uploads/linkedin-ki-unit-economics-one-day.md) | [`lessons/m1-3-unit-economics.md`](./lessons/m1-3-unit-economics.md) · **woven** |
| **М1.5** | [`uploads/medium-seregina-metrics-hierarchy-vs-pyramid.md`](./uploads/medium-seregina-metrics-hierarchy-vs-pyramid.md) · [`uploads/linkedin-zaleuska-north-star-product-metrics.md`](./uploads/linkedin-zaleuska-north-star-product-metrics.md) · [`uploads/linkedin-swartz-hierarchy-product-metrics.md`](./uploads/linkedin-swartz-hierarchy-product-metrics.md) · [`uploads/medium-seregina-metrics-frameworks.md`](./uploads/medium-seregina-metrics-frameworks.md) | [`lessons/m1-5-strategy-nsm.md`](./lessons/m1-5-strategy-nsm.md) · **woven** |
| **М1.8** | [`uploads/linkedin-tyler-rice-excerpt.md`](./uploads/linkedin-tyler-rice-excerpt.md) | [`lessons/m1-8-product-diagnosis.md`](./lessons/m1-8-product-diagnosis.md) · **woven** |
| **М2.3** | [`uploads/linkedin-swartz-hierarchy-product-metrics.md`](./uploads/linkedin-swartz-hierarchy-product-metrics.md) · [`uploads/medium-duckweave-duckdb-retention-cohorts.md`](./uploads/medium-duckweave-duckdb-retention-cohorts.md) · [`uploads/bonus-habr-product-metrics-sql.md`](./uploads/bonus-habr-product-metrics-sql.md) · [`uploads/medium-hashblock-duckdb-window-cohorts.md`](./uploads/medium-hashblock-duckdb-window-cohorts.md) | [`lessons/m2-3-conversion-cohorts.md`](./lessons/m2-3-conversion-cohorts.md) · **woven** |
| **М2.4** | — (мало в uploads; якоря §3.4 + stats-ab) | [`lessons/m2-4-confidence-intervals.md`](./lessons/m2-4-confidence-intervals.md) · **углублён** (stats-ab) |
| **М2.5** | [`uploads/medium-geoghegan-end-to-end-product-analytics-strategy.md`](./uploads/medium-geoghegan-end-to-end-product-analytics-strategy.md) (эксперимент как мышца) | [`lessons/m2-5-ab-design-read.md`](./lessons/m2-5-ab-design-read.md) · **углублён** (stats-ab + GoPractice/Habr §3.4) |
| **М3.2** | [`uploads/medium-hashblock-duckdb-window-cohorts.md`](./uploads/medium-hashblock-duckdb-window-cohorts.md) · [`uploads/medium-mohitdaxini-monthly-cohort-retention-sql.md`](./uploads/medium-mohitdaxini-monthly-cohort-retention-sql.md) · [`uploads/medium-shaunmia-sql-window-cohort-analysis.md`](./uploads/medium-shaunmia-sql-window-cohort-analysis.md) · [`uploads/medium-snehagupta-10-sql-queries-data-analyst.md`](./uploads/medium-snehagupta-10-sql-queries-data-analyst.md) · [`uploads/bonus-kariernik-sql-product-analyst.md`](./uploads/bonus-kariernik-sql-product-analyst.md) · [`uploads/bonus-habr-product-metrics-sql.md`](./uploads/bonus-habr-product-metrics-sql.md) · [`uploads/medium-duckweave-duckdb-retention-cohorts.md`](./uploads/medium-duckweave-duckdb-retention-cohorts.md) | [`lessons/m3-2-sql-zero-to-windows.md`](./lessons/m3-2-sql-zero-to-windows.md) · **woven** |
| **М3.4** | [`uploads/medium-nickpatel-pandas-to-duckdb.md`](./uploads/medium-nickpatel-pandas-to-duckdb.md) | [`lessons/m3-4-pandas-polars.md`](./lessons/m3-4-pandas-polars.md) · **woven** |
| **М3.5** | — (якоря Habr / zasqlpython §3.1) | [`lessons/m3-5-ai-copilot-sql-python.md`](./lessons/m3-5-ai-copilot-sql-python.md) · **написан** |
| **М3.3** | — (HireHi / Postgres docs в sql-python-sources) | [`lessons/m3-3-query-under-the-hood.md`](./lessons/m3-3-query-under-the-hood.md) · **написан** |
| **М2.1** | — | [`lessons/m2-1-noise-variability.md`](./lessons/m2-1-noise-variability.md) · **написан** |
| **М2.2** | — | [`lessons/m2-2-descriptive-stats.md`](./lessons/m2-2-descriptive-stats.md) · **написан** |
| **М4.1** | — (UX: NN/g / Surf в ux-sources) | [`lessons/m4-1-screen-as-hypothesis.md`](./lessons/m4-1-screen-as-hypothesis.md) · **написан** |
| **М4.2** | — (Habr user flow) | [`lessons/m4-2-flow-friction.md`](./lessons/m4-2-flow-friction.md) · **написан** |
| **М1.2** | — (GoPractice JTBD / Kustov) | [`lessons/m1-2-jtbd.md`](./lessons/m1-2-jtbd.md) · **написан** |
| **М1.4** | GoPractice + vc.ru + Min LTV/CAC uploads | [`lessons/m1-4-product-finance.md`](./lessons/m1-4-product-finance.md) · **написан** |
| **М1.6** | — (Бюро UI / Habr friction) | [`lessons/m1-6-benefit-tax.md`](./lessons/m1-6-benefit-tax.md) · **написан** |
| **М2.6** | — (Statsig / DoorDash switchback) | [`lessons/m2-6-when-ab-impossible.md`](./lessons/m2-6-when-ab-impossible.md) · **написан** |
| **М5.3** | storytellingwithdata / IBS — §1 топ + §3 BI | [`lessons/m5-3-chart-choice.md`](./lessons/m5-3-chart-choice.md) · **написан** |
| **М5.5** | Metabase Learn organization | [`lessons/m5-5-analytics-in-team.md`](./lessons/m5-5-analytics-in-team.md) · **написан** |
| **М5.1** | [`uploads/medium-seregina-metrics-frameworks.md`](./uploads/medium-seregina-metrics-frameworks.md) · [`uploads/medium-seregina-metrics-hierarchy-vs-pyramid.md`](./uploads/medium-seregina-metrics-hierarchy-vs-pyramid.md) · [`uploads/linkedin-zaleuska-north-star-product-metrics.md`](./uploads/linkedin-zaleuska-north-star-product-metrics.md) · [`uploads/bonus-gopractice-product-health-dashboard.md`](./uploads/bonus-gopractice-product-health-dashboard.md) | [`lessons/m5-1-metrics-layer.md`](./lessons/m5-1-metrics-layer.md) · **woven** |
| **М5.2** | [`uploads/bonus-gopractice-product-health-dashboard.md`](./uploads/bonus-gopractice-product-health-dashboard.md) · [`uploads/bonus-habr-product-dashboard.md`](./uploads/bonus-habr-product-dashboard.md) | [`lessons/m5-2-dashboard-decision.md`](./lessons/m5-2-dashboard-decision.md) · **woven** |
| **М5** (обзор) | + Geoghegan end-to-end | см. М0.1 / М5.2 |

История wishlist и URL: [`medium-download-wishlist.md`](./medium-download-wishlist.md). Политика копий: [`uploads/README.md`](./uploads/README.md).

---

## 3. Библиотека по пробелам / модулям

### 3.1. AI-verify SQL (М0.2, М3.5–М3.6)

| Источник | Яз. | Доступ | Решение | Заметка |
|---|---|---|---|---|
| [Habr 1066650 — не галлюцинирует](https://habr.com/ru/articles/1066650/) | ru | открыто | **keep** | Опорный кейс границы LLM vs код |
| [Habr 944010 — text-to-SQL ломается](https://habr.com/ru/articles/944010/) | ru | открыто | **keep** | Каркас правдоподобных ошибок |
| [Habr Bothub — RAG/CoT text-to-SQL](https://habr.com/ru/companies/bothub/articles/925632/) | ru | открыто | adapt | Фон промптинга; не методика приёмки студента |
| [Habr X5 — Text2SQL в аналитике](https://habr.com/ru/companies/X5Tech/articles/949694/) | ru | открыто | adapt | Прод-кейс галлюцинаций колонок; сильным |
| [zasqlpython — YandexGPT/ChatGPT для SQL](https://zasqlpython.ru/blog/yandexgpt-chatgpt-dlya-analitika-sql-generaciya-2026) | ru | открыто | **keep** | Практика «пишет быстро — проверяй» |
| HireHi ChatGPT для аналитика | ru | см. sql-python | keep | Уже в sql-python-sources |

### 3.2. Tracking plan / разметка (М4.3, стык М3.1)

| Источник | Яз. | Доступ | Решение | Заметка |
|---|---|---|---|---|
| [Surf tracking plan](https://surf.ru/analitika-mobilnyh-prilozhenij/) | ru | открыто | **keep** | Лучший RU-каркас таблицы событий |
| [Habr Яндекс Лавка — события](https://habr.com/ru/companies/yandex/articles/940728/) | ru | открыто | **keep** | Процесс, YAML-спека, мониторинг доверия |
| [Зеркало Лавки на blog Yandex Go](https://dev.go.yandex/blog/new-lavka-layout-2025-09-16) | ru | открыто | adapt | Тот же кейс короче |
| [Habr OTUS — система событий / продажи](https://habr.com/ru/companies/otus/articles/1037016/) | ru | открыто | **keep** | Один этап = одно событие; чеклист полей |
| [Habr Ситидрайв — разметка](https://habr.com/ru/companies/citydrive/articles/780576/) | ru | открыто | adapt | Масштаб событий; процесс |
| [AppMetrica — офферные события / Product Flow](https://appmetrica.yandex.com/docs/ru/data-collection/offers.md) | ru | открыто | adapt | `offerShown` → `flowResult` как схема сценария |
| Habr AGIMA / имена событий (ux-sources) | ru | открыто | keep | Уже в ux-sources |

### 3.3. Юнит-экономика / когорты денег (М1.3, М2.3)

| Источник | Яз. | Доступ | Решение | Заметка |
|---|---|---|---|---|
| [GoPractice unit-economics](https://gopractice.ru/product/unit-economics/) | ru | открыто | **keep** | Канон рядом с Красинским |
| [vc.ru — LTV/CAC где счёт врёт](https://vc.ru/marketing/3052938-unit-ekonomika-privlecheniya-ltv-cac) | ru | открыто | **keep** | Зрелость когорт, горизонт LTV |
| [vc.ru — юнит + JTBD-сценарии](https://vc.ru/marketing/899322-kak-rasschitat-yunit-ekonomiku-naiti-tochki-rosta-cherez-jtbd-scenarii-i-mnogoe-drugoe) | ru | открыто | adapt | Стык М1.2↔М1.3; не путать ARPPU/CLTV |
| [Habr — CAC длинный B2B-цикл](https://habr.com/ru/articles/1045170/) | ru | открыто | adapt | Когорта по появлению сделки; опция сильным |
| [Пустовалов — когортный retention/LTV](https://dipustovalov.ru/blog/kogortnyy-analiz-retention-2026) | ru | открыто | adapt | Чтение матрицы; Метрика/Sheets |
| [KI Professionals — unit econ one day](https://www.linkedin.com/pulse/guide-understand-unit-economics-one-day-examples-ki-professionals) | en | Pulse часто открыт; **зеркало Medium** | **keep** / wishlist | Когортный AMPU vs CPUser |
| Medium-зеркало того же: `@KI_professionals/...a9dd822c5441` и `aleksandr-palchikov.medium.com/...6ab1c41edcaf` | en | Medium 403 из облака | wishlist | Качать md у kir |

### 3.4. A/B literacy (М2.4–М2.5)

| Источник | Яз. | Доступ | Решение | Заметка |
|---|---|---|---|---|
| [GoPractice design-ab-test](https://gopractice.ru/data/design-ab-test/) | ru | открыто | **keep** | Шаблон дизайна |
| [GoPractice ab-tests-guide](https://gopractice.ru/data/ab-tests-guide/) | ru | открыто | **keep** | Вход для продакта |
| [Habr 996860 — как правильно провести A/B](https://habr.com/ru/articles/996860/) | ru | открыто | **keep** | Guardrail, MDE, до старта |
| [Habr 978702 — trustworthy B2C](https://habr.com/ru/articles/978702/) | ru | открыто | adapt | Ratio / линеаризация — сильным |
| [Habr Avito — A/B малых выборок](https://habr.com/ru/companies/avito/articles/1041336/) | ru | открыто | adapt | DAG метрик; не ядро Ритма |
| [Habr 983060 — выбор метода](https://habr.com/ru/articles/983060/) | ru | открыто | adapt | χ² / bootstrap / CUPED обзор |
| Evan Miller calculators | en | открыто | keep | Уже в инвентаре |
| KISSmetrics A/B workflow | en | PDF/блог фрагментарно | adapt / низкий | Исторически в medium-linkedin; **замена = GoPractice + Habr 996860** |
| [stats-ab-course](https://github.com/gavnukkk97/stats-ab-course) (kir) | ru | открыто (репо) | **adapt** → тела М2.4/М2.5 | Не студенческий dump: карта [`../internal/stats-ab-weave.md`](../internal/stats-ab-weave.md) |

### 3.5. BI storytelling / дашборд под решение (М5.1–М5.4)

| Источник | Яз. | Доступ | Решение | Заметка |
|---|---|---|---|---|
| [GoPractice product-health-dashboard](https://gopractice.ru/insights/product-health-dashboard/) | ru | открыто | **keep** | Три блока «здоровья» |
| [Habr 929770 — продуктовый дашборд](https://habr.com/ru/articles/929770/) | ru | открыто | **keep** | NSM + воронка ценности + tabs |
| [IBS — дашборд для руководителя](https://ibs.ru/media/kak-sdelat-dashbord-ponyatnym-dlya-rukovoditelya-bazovye-printsipy/) | ru | открыто | **keep** | 5–7 KPI, сигнал→drill-down |
| [Kariernik — дашборд для PM](https://kariernik.ru/blog/dashboard-dlya-pm) | ru | открыто | **keep** | Health / features / funnels layout |
| [Habr 838144 — сторителлинг в BI](https://habr.com/ru/articles/838144/) | ru | открыто | adapt | Narrative после анализа |
| [Habr Beeline — дашборд ↔ бизнес](https://habr.com/ru/companies/beeline_tech/articles/847596/) | ru | открыто | adapt | Overview vs product deep-dive |
| storytellingwithdata chart guide | en | открыто | keep | Уже в инвентаре М5.3 |
| Metabase Learn | en | открыто | keep | Стек курса |

### 3.6. Метрики / NSM / рамка системы (М0.1, М1.5, М5.1)

| Источник | Яз. | Доступ | Решение | Заметка |
|---|---|---|---|---|
| [Seregina — Пирамида too much](https://medium.com/@elenest/metrics-frameworks-d7c800f91246) | ru | Medium 403 | **keep** + wishlist | Вопросы→метрики |
| [Seregina — Иерархия vs Пирамида / NSM](https://medium.com/@elenest/%D0%B8%D0%B5%D1%80%D0%B0%D1%80%D1%85%D0%B8%D1%8F-%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%BA-vs-%D0%BF%D0%B8%D1%80%D0%B0%D0%BC%D0%B8%D0%B4%D0%B0-%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%BA-8eeda61fdefe) | ru | Medium 403 | wishlist | Пара к М1.5 |
| [Zaleuska — North Star tree (Pulse)](https://www.linkedin.com/pulse/product-metrics-designer-to-pm-transitioners-north-star-alla-zaleuska-8tafc) | en | Pulse часто открыт | **keep** / wishlist логин | NSM → 3–5 inputs |
| [Swartz — Hierarchy of Product Metrics](https://www.linkedin.com/pulse/hierarchy-product-metrics-luke-swartz-miywc) | en | Pulse | **keep** / wishlist | Retention keystone |
| [Geoghegan — End-to-End PA Strategy](https://towardsdatascience.com/your-end-to-end-product-analytics-strategy-648ecfa586c2/) | en | TDS/Medium риск | adapt + wishlist | Стадии продукта × аналитика |
| Зеркало IIA: [iianalytics.com/.../your-end-to-end-product-analytics-strategy](https://iianalytics.com/community/blog/your-end-to-end-product-analytics-strategy) | en | проверить | **mirror** | Если TDS режет — пробовать IIA |

### 3.7. Продукт / JTBD / CustDev / поток (М1.1–М1.2, М4.2, М4.4)

| Источник | Яз. | Доступ | Решение | Заметка |
|---|---|---|---|---|
| [Beskov CustDev — vc.ru](https://vc.ru/marketing/53090-vvedenie-v-customer-development) | ru | открыто | **keep** + **mirror** | Не слать студентам Medium-URL |
| Medium оригинал Product Story | ru | 403 | skip URL | Только если kir нужен оригинал |
| [Kustov JTBD — ScrumTrek](https://scrumtrek.ru/blog/product-management/2492/gajd-po-tehnike-jobs-to-be-done-jtbd/) | ru | открыто | **keep** + **mirror** | Medium `dimkakustov...7e01a528f442` — 403 риск |
| [Habr User flow](https://habr.com/ru/articles/1081360/) | ru | открыто | **keep** | Вместо прототипирования Voloshyn |
| GoPractice JTBD / CustDev.me | ru | открыто / SSL quirks | keep | Уже в инвентаре |
| Ivano «Дилеммы продакта» Medium | ru | открыто | **skip** | Нет аналитического ядра |
| Voloshyn прототипирование Medium | ru | 403 | **skip** | Анти-скоуп дизайна |
| LinkedIn: Benediktsson / Meduzzen MVP | en | открыто | **skip** | Маркетинг/агентство |
| LinkedIn Ashworth — только RICE | en | открыто | **adapt** | Кусок приоритизации М1.8 |

### 3.8. SQL / когорты руками (стык М3.2; детали в sql-python)

| Источник | Решение | Заметка |
|---|---|---|
| Kariernik / HireHi / Habr 1010980 / OTUS когорты | keep | Открытый канон без Medium |
| Medium DuckDB/windows/cohorts (wishlist §1) | wishlist | Глубина примеров окон |
| GoPractice SQL Simulator | развилка kir | Платный; не блокер стенда Ритма |

---

## 4. Карта «модуль → якоря»

| Модуль | Якоря (открытые first) | Офлайн (`uploads/`) | В теле урока |
|---|---|---|---|
| М0.1 / М0.2 | GoPractice data-informed (инвентарь); Habr 1066650 | Geoghegan end-to-end | М0.1 **woven** (стадии) |
| М1.1 | Beskov vc.ru | — | — |
| М1.2 | Kustov ScrumTrek; GoPractice JTBD | — | [`lessons/m1-2-jtbd.md`](./lessons/m1-2-jtbd.md) · **написан** |
| М1.3 | GoPractice unit-econ; vc.ru 3052938; Pulse/Medium KI | GoPractice + vc.ru + KI + Min LTV/CAC | **woven** |
| М1.4 | GoPractice unit-econ; vc.ru LTV/CAC; payback guides | GoPractice + Min LTV/CAC uploads | [`lessons/m1-4-product-finance.md`](./lessons/m1-4-product-finance.md) · **написан** |
| М1.5 / М5.1 | Zaleuska / Swartz; Seregina; GoPractice NSM | Seregina ×2 · Zaleuska · Swartz | М5.1 **woven**; М1.5 **написан** |
| М1.6 | Бюро UI; Habr user flow / friction | — | [`lessons/m1-6-benefit-tax.md`](./lessons/m1-6-benefit-tax.md) · **написан** |
| М1.8 | Ashworth RICE (кусок); RCA Product Heroes | Tyler RICE excerpt | **woven** |
| М2.3 | GoPractice retention; Красинский; Kariernik/Habr SQL | Swartz · Duckweave · Habr SQL | **woven** |
| М2.4–М2.5 | GoPractice A/B; Habr 996860; Evan Miller; **stats-ab** (адаптация) | Geoghegan (мышца эксперимента) | М2.4 + М2.5 **углублены** (SRM/CUPED-lite/N×2); см. `internal/stats-ab-weave.md` |
| М2.6 | Statsig/DoorDash switchback; GoPractice A/B границы | — | [`lessons/m2-6-when-ab-impossible.md`](./lessons/m2-6-when-ab-impossible.md) · **написан** |
| М3.2 | sql-python канон; Medium windows | Hashblock · Mohit · Shaun · Sneha · Kariernik | **woven** |
| М3.4 | sql-python pandas/polars | Nick Patel Pandas→DuckDB | **написан** |
| М3.6 | Habr 1066650 + 944010; zasqlpython | — | — |
| М4.2 | Habr User flow; Habr Proto friction | — | [`lessons/m4-2-flow-friction.md`](./lessons/m4-2-flow-friction.md) · **написан** |
| М4.3 | Surf; Habr Лавка; Habr OTUS события | — | — |
| М4.4 | Beskov; Замесин; Habr Альфа (ux-sources) | — | — |
| М5.2–М5.4 | GoPractice health; Habr 929770; IBS; Kariernik PM-дашборд; Metabase Learn | GoPractice health · Habr дашборд | М5.2 **woven** |
| М5.5 | Metabase Learn organization; product team dashboard; adoption rituals | — | [`lessons/m5-5-analytics-in-team.md`](./lessons/m5-5-analytics-in-team.md) · **написан** |

---

## 5. Что сознательно не берём

- Paywalled пиратские копии книг / курсов.  
- Агентский LinkedIn-SEO (MVP «поставьте аналитику»).  
- Medium как **единственный** URL обязательного чтения для студентов (403 у части аудитории) — только зеркало, выгрузка в `uploads/`, или концепт уже в теле урока.  
- Полный awesome-PM списком студентам.  
- Дубликат всего каталога GoPractice / Красинского — см. основной инвентарь.

---

## 6. Пробелы после волны weave (2026-09-14)

| Пробел | Статус |
|---|---|
| Концепты uploads только в «Дальше читать» | **Снято** для ядра P1–P4 носителей: см. weave-map |
| М1.5 / М3.4 полные уроки | **написаны** в `lessons/` |
| М2.4 / М2.5 глубокий A/B | **снято** в store: углублены уроки из stats-ab-course (не uploads); sync в GitHub-pack — по запросу |
| М2.6 полный текст / Bayes / causal deep | **М2.6 написан** (switchback/квази обзор); Bayes/causal deep — optional stats-ab М5–М6 private ref |
| М3.6 методика приёмки AI | Риторика закрыта открытым Habr; авторский набор ложных ответов на схеме Ритма — есть в уроке |
| М4.3 «дизайн, ломающий данные» | Процесс разметки усилен (Лавка/OTUS); авторский антипример в уроке |
| М1.2 / М1.4 / М1.6 / М4.2 | **написаны** 14.09.2026 |
| М5.5 жизнь аналитики в команде | **написан** (`m5-5-analytics-in-team.md`); ритуал + Metabase org |
| EN Medium SQL windows | md в [`uploads/`](./uploads/); идеи **woven** в М3.2 под Postgres |
| LinkedIn без логина | md в uploads |

*Обновлено 14 сентября 2026 (nice-to-have gap closure + self-contained weave + stats-ab A/B).*
