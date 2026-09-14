# Учебный стенд «Ритм»

Локальный **Postgres + Metabase** и синтетические данные продукта курса **Ритм** (B2C-привычки, freemium → Pro). Имена таблиц и событий совпадают с уроками М4.3 / М3.2 / М5.2 / М5.4.

| Сервис | Адрес по умолчанию |
|---|---|
| Postgres | `localhost:54329`, БД `ritm`, пользователь/пароль `ritm` / `ritm_local` |
| Metabase | [http://localhost:3847](http://localhost:3847) |

---

## Быстрый старт

```bash
cd docs/stand          # эта папка
cp .env.example .env
docker compose up -d
```

1. Дождаться healthy у `ritm-postgres` и `ritm-metabase` (`docker compose ps`).
2. Открыть Metabase → создать admin → **Add database** → PostgreSQL:
   - Host: `postgres` (из контейнера Metabase) или `host.docker.internal` / IP хоста, если подключаетесь иначе  
   - Port: `5432` (внутри сети compose)  
   - Database / User / Password: из `.env` (`ritm` / `ritm` / `ritm_local`)
3. Проверить: `SELECT count(*) FROM users;`, `events`, `subscriptions`.
4. Собрать карточки по эскизам в [`sql/04_metabase_card_sketches.sql`](./sql/04_metabase_card_sketches.sql).

Семпл уже заливается при **первом** `initdb` из `sql/03_seed.sql`. Повторная загрузка CSV:

```bash
bash scripts/load_seed.sh
```

Полный датасет (~2500 users):

```bash
bash scripts/load_generated.sh 2500 42
```

Сброс volume (если схема поменялась):

```bash
docker compose down -v && docker compose up -d
```

---

## Состав папки

| Путь | Назначение |
|---|---|
| `docker-compose.yml` | Postgres 16 + Metabase |
| `.env.example` | порты и креды |
| `sql/01_schema.sql` | `users`, `events`, `subscriptions` |
| `sql/02_views.sql` | depth / воронка / QA-вьюхи |
| `sql/03_seed.sql` | маленький INSERT-семпл для initdb |
| `sql/04_metabase_card_sketches.sql` | SQL под дашборд М5.4 |
| `seed/*.csv` | тот же семпл в CSV |
| `generator/generate_ritm.py` | синтетика + грязь + A/B |
| `scripts/load_*.sh` | загрузка в живой Postgres |

---

## Модель данных (как в М4.3)

**`users`** — 1 строка = 1 пользователь: `user_id`, `installed_at`, `platform`, `is_internal`, плюс учебные `ab_variant` / `ab_experiment`.

**`events`** — сырой поток: `event_id`, `user_id`, `event_name`, `ts`, `props` (jsonb).

**`subscriptions`** — оплата Pro: `subscription_id`, `user_id`, `started_at`, `plan` (`month`/`year`), `status`, `price_rub`.

События tracking plan: `app_open`, `onboarding_completed`, `habit_created`, `check_in`, `streak_3_reached`, `paywall_view`, `subscribe_started`. В грязном слое также встречаются `session_restored`, `onboarding_step_viewed`, `button_click` (антипаттерн).

Цены Pro в данных: **299 ₽/мес**, **1990 ₽/год**.

---

## Синтетика и «грязь»

Генератор намеренно портит часть данных, чтобы ловить ломаные запросы (М3.2 / М3.6):

- дубли `check_in` и `paywall_view`;
- пустые `props` / нет `habit_id` или `local_date`;
- schema drift: `local_date` vs `local_day`, `schema_version` 1/2;
- несколько `habit_created` на user (правки);
- две строки в `subscriptions` (month → year) — ловушка JOIN;
- `is_internal = true`;
- шум `button_click`.

```bash
python3 generator/generate_ritm.py --n-users 80 --seed 42
python3 generator/generate_ritm.py --full --seed 42   # 2500 users
```

Только stdlib Python 3.10+.

---

## A/B (завершённый, с известным исходом)

Эксперимент `paywall_timing_2026q3`:

- **control** — paywall часто рано (`day_7` / `feature_lock`);
- **treatment** — paywall в основном после `streak_3_reached`.

Студенты считают эффект по `users.ab_variant`. Ключ исхода A/B в этот публичный репозиторий **не входит**. На малом семпле шум большой — для М2.5 / капстоуна используйте `--full`.

---

## Карта к урокам

| Урок | Что делать на стенде |
|---|---|
| **М3.1** Зерно таблиц | Карточка зерна `users` / `events` / `subscriptions`; count vs count distinct |
| **М4.3** Tracking plan | Сверить имена событий/props; QA: `v_qa_duplicate_check_ins`, `v_qa_paywall_without_habit` |
| **М3.2** SQL → окна | DAU, depth≥3, ломаные A/B/C на живых таблицах; `v_first_habit`, `v_depth_d7` |
| **М1.3** Юнит-экономика | Цены Pro в `subscriptions`; воронка → лист CAC/LTV (числа с SQL или учебной таблицы) |
| **М5.1** Словарь метрик | Привязать определения к сырому / view; QA на грязи |
| **М5.2** Дашборд на бумаге | Те же KPI: depth, habit→check_in, early paywall, new Pro |
| **М5.4** Metabase | Compose + карточки из `04_metabase_card_sketches.sql`; фильтр `platform` |
| **М1.8** Диагностика | Воронка/сегменты на тех же view; гипотезы → метрики словаря |
| **М2.4** ДИ / N | Оценка + 95% ДИ на долях / Δ; семпл vs full как контрпример ширины |
| **М2.5** A/B | Full датасет; `users.ab_variant` / `paywall_timing_2026q3`; ключ исхода не публикуется |
| **М4.4** Коридор | Не стенд Postgres; опора к гипотезам P3 (метрики из словаря → потом SQL) |

Контрольные запросы после подъёма:

```sql
SELECT count(*) FROM users;
SELECT count(*) FROM events;
SELECT event_name, count(*) FROM events GROUP BY 1 ORDER BY 2 DESC;
SELECT * FROM v_depth_d7 LIMIT 10;
```

---

## Требования

- Docker + Docker Compose v2
- `psql` на хосте — только для `scripts/load_*.sh` (опционально)
- Python 3.10+ — для перегенерации

Учебный стенд, не прод-DWH. Данные синтетические, не содержат реальных пользователей.
