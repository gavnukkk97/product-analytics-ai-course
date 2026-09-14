# С чего начать студенту

Курс: **продуктовая аналитика в эпоху AI**. Учебный продукт — **Ритм** (B2C-привычки, freemium → Pro). Практика крутится вокруг четырёх вех **P1–P4** на одних и тех же синтетических данных.

Этот файл — входная дверь. Карта модулей и календарь ~8 недель — в [`course-structure.md`](./course-structure.md). Список уже написанных уроков — [`lessons/README.md`](./lessons/README.md).

**Для преподавателя:** операционный ранбук потока — [`instructor-guide.md`](./instructor-guide.md) (в Context store; в public student pack ключ A/B не входит).

---

## 0. Что поставить

- **Docker** + Docker Compose v2  
- Браузер (Metabase)  
- Опционально: `psql`, Python 3.10+ (перегенерация полного датасета)  
- AI-со-пилот по желанию — но **цифру и вывод проверяете вы** (см. М0.2, М3.6)

Учётные данные стенда учебные (`ritm` / `ritm_local`) — только localhost, не для продакшена.

---

## 1. Поднять стенд «Ритм»

```bash
cd docs/stand
cp .env.example .env
docker compose up -d
docker compose ps    # postgres и metabase — healthy
```

| Сервис | Адрес |
|---|---|
| Postgres | `localhost:54329`, БД `ritm`, user/password `ritm` / `ritm_local` |
| Metabase | http://localhost:3847 |

1. Откройте Metabase → создайте admin → **Add database** → PostgreSQL.  
   - Host из контейнера Metabase: `postgres`, port `5432`  
   - Database / User / Password: как в `.env`  
2. Проверка в SQL:

```sql
SELECT count(*) FROM users;
SELECT count(*) FROM events;
SELECT event_name, count(*) FROM events GROUP BY 1 ORDER BY 2 DESC;
```

Семпл заливается при первом старте. Полный датасет для A/B (P4):

```bash
bash scripts/load_generated.sh 2500 42
```

Подробности, грязный слой и карта к урокам — [`stand/README.md`](./stand/README.md).

**Важно:** папка `stand/instructor/` (если встретится) — **не для студентов**. Ключ исхода A/B смотрит только преподаватель.

---

## 2. Порядок уроков (по вехам)

Не обязательно читать «всю карту курса». Для сдач идите по цепочке ниже. Внутри недели можно параллелить «руки» и «решение», но **ядро** каждой вехи лучше не перескакивать.

### Рамка (неделя 1, до цифр)

1. [`lessons/m0-1-contour.md`](./lessons/m0-1-contour.md) — контур решения  
2. [`lessons/m0-2-ai-in-contour.md`](./lessons/m0-2-ai-in-contour.md) — договор с AI  

### P1. Метрики (недели 1–2)

3. [`m1-1-problem-market.md`](./lessons/m1-1-problem-market.md) — проблема и рынок Ритма  
4. [`m3-1-data-grain.md`](./lessons/m3-1-data-grain.md) — зерно таблиц стенда  
5. [`m4-3-tracking-plan.md`](./lessons/m4-3-tracking-plan.md) — tracking plan 10–15 событий  
6. [`m1-3-unit-economics.md`](./lessons/m1-3-unit-economics.md) — древо метрик (старт)  
7. [`m3-2-sql-zero-to-windows.md`](./lessons/m3-2-sql-zero-to-windows.md) — SQL: первая честная цифра  
8. К демо-2 / словарю: [`m5-1-metrics-layer.md`](./lessons/m5-1-metrics-layer.md)  

**Сдача P1:** сценарий понят · древо · tracking plan · SQL с сырых без вранья JOIN/зерна.

### P2. Когорты и юнит (недели 2–3)

9. Дожим [`m1-3-unit-economics.md`](./lessons/m1-3-unit-economics.md) — экономика на одном листе  
10. [`m2-3-conversion-cohorts.md`](./lessons/m2-3-conversion-cohorts.md) — четыре способа конверсии / ретеншн  
11. Окна в [`m3-2-sql-zero-to-windows.md`](./lessons/m3-2-sql-zero-to-windows.md) — первое событие, когорта  

**Сдача P2:** четыре конверсии/ретеншн на синтетике · юнит-лист · названное узкое место.

### Мост к дашборду (неделя 4)

12. [`m3-6-verify-ai-sql.md`](./lessons/m3-6-verify-ai-sql.md) — поймать ложь AI  
13. [`m5-1-metrics-layer.md`](./lessons/m5-1-metrics-layer.md) — словарь определений  
14. [`m5-2-dashboard-decision.md`](./lessons/m5-2-dashboard-decision.md) — дашборд на бумаге  

### P3. Точки роста (неделя 5)

15. [`m1-7-cjm-journey.md`](./lessons/m1-7-cjm-journey.md) — CJM сценария  
16. [`m1-8-product-diagnosis.md`](./lessons/m1-8-product-diagnosis.md) — диагноз + 3 гипотезы  
17. [`m4-4-corridor-tests.md`](./lessons/m4-4-corridor-tests.md) — качественная опора  
18. [`m5-4-metabase-dashboard.md`](./lessons/m5-4-metabase-dashboard.md) — сборка в Metabase  

**Сдача P3:** диагностика · сегменты · 3 приоритизированные гипотезы · живой (или эскизный) дашборд.

### P4. A/B и защита (недели 6–8)

19. [`m2-4-confidence-intervals.md`](./lessons/m2-4-confidence-intervals.md) — ДИ / хватит ли N  
20. [`m2-5-ab-design-read.md`](./lessons/m2-5-ab-design-read.md) — дизайн и чтение `paywall_timing_*` (**full** датасет)  
21. [`m1-10-insight-to-decision.md`](./lessons/m1-10-insight-to-decision.md) — цифра → деньги → решение  
22. [`m6-1-capstone-defense.md`](./lessons/m6-1-capstone-defense.md) — защита 10 минут  

**Сдача P4:** карточка эксперимента · честный расчёт · решение «растим / разворачиваем / убиваем» · живая защита.

Часть модулей календаря (М1.4, М1.6, М2.6, М4.1…) может ещё писаться — **вехи P1–P4 на уже готовых текстах закрываются** без них. Если файла нет в `lessons/`, смотрите актуальный список в [`lessons/README.md`](./lessons/README.md).

---

## 3. Как сдавать задания

В каждом уроке одно задание = **ядро** (все) + расширение **«руки»** и/или **«решение»**. Нужно ядро и хотя бы одно расширение.

Критерии приёмки — чеклист в конце урока. AI можно использовать для кода и черновиков; в сдачу идёт только то, что вы **проверили** контрольными запросами / определениями из словаря.

---

## 4. Если что-то сломалось

| Симптом | Что сделать |
|---|---|
| Metabase пустой / нет таблиц | Дождаться healthy postgres; переподключить БД; `docker compose logs postgres` |
| Старая схема после правок SQL | `docker compose down -v && docker compose up -d` (сотрёт volume) |
| A/B «не сходится» на семпле | Для М2.5 / капстоуна — `load_generated.sh 2500 42`, не маленький seed |
| Расхождение count vs count distinct | Вернитесь к М3.1 / грязному слою в README стенда — это учебная ловушка |

Вопросы по содержанию модулей — преподавателю потока. Этот репозиторий — материалы и стенд, не прод-поддержка Docker.
