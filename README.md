# Курс: продуктовая аналитика в эпоху AI

Публичный студенческий пакет курса. Учебный продукт — **Ритм** (B2C-привычки, freemium → Pro). Практика на четырёх вехах **P1–P4** на одних и тех же синтетических данных.

## Быстрый старт

1. Прочитайте [`docs/student-getting-started.md`](docs/student-getting-started.md).
2. Карта модулей: [`docs/course-structure.md`](docs/course-structure.md).
3. Уроки: [`docs/lessons/`](docs/lessons/).
4. Библиотека статей (офлайн): [`docs/uploads/`](docs/uploads/) и индекс [`docs/materials-library.md`](docs/materials-library.md).

## Поднять стенд «Ритм»

Нужны **Docker** и Docker Compose v2.

```bash
cd docs/stand
cp .env.example .env
docker compose up -d
docker compose ps
```

| Сервис | Адрес | Учётка |
|---|---|---|
| **Metabase** | http://localhost:3847 | создаёте admin при первом входе |
| **Postgres** | `localhost:54329` | БД `ritm`, user `ritm`, password `ritm_local` |

В Metabase → Add database → PostgreSQL:

- Host (из контейнера Metabase): `postgres`
- Port: `5432`
- Database / User / Password: `ritm` / `ritm` / `ritm_local`

Полный датасет для A/B (P4 / М2.5):

```bash
bash scripts/load_generated.sh 2500 42
```

Подробности: [`docs/stand/README.md`](docs/stand/README.md).

Учебные креды только для localhost — не для продакшена.

## Что в репозитории

- `docs/lessons/` — уроки и визуалы
- `docs/stand/` — Docker Compose, SQL, семпл, генератор
- `docs/uploads/` — выгрузки статей для самодостаточного курса
- `docs/course-structure.md`, `docs/student-getting-started.md`, `docs/materials-library.md`

Ключ исхода A/B и внутренние материалы преподавателя в публичный пакет **не входят**.
