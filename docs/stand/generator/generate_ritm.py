#!/usr/bin/env python3
"""
Генератор синтетики Ритма (учебный стенд).

Пишет CSV в --out (по умолчанию ../seed).
Ключ A/B преподавателя в публичный пакет не входит; --write-key только локально у инструктора.

Запуск из docs/stand:
  python3 generator/generate_ritm.py --n-users 80 --seed 42
  python3 generator/generate_ritm.py --n-users 2500 --seed 42 --full
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import uuid
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

MSK = timezone(timedelta(hours=3))
HABIT_TYPES = ("morning", "water", "steps", "reading", "meditation")
PLATFORMS = ("ios", "android", "web")
PLATFORM_W = (0.42, 0.48, 0.10)


@dataclass
class Config:
    n_users: int
    seed: int
    start: date
    end: date
    out_dir: Path
    key_path: Path
    dirt_rate: float
    write_key: bool


def uid(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def dt_between(rng: random.Random, start: datetime, end: datetime) -> datetime:
    span = max(1, int((end - start).total_seconds()))
    return start + timedelta(seconds=rng.randint(0, span))


def local_date_str(ts: datetime) -> str:
    return ts.astimezone(MSK).date().isoformat()


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    """Пустые поля = SQL NULL при \\copy ... NULL ''."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        w.writeheader()
        for r in rows:
            out = {k: ("" if r.get(k) is None else str(r.get(k, ""))) for k in fieldnames}
            w.writerow(out)


def generate(cfg: Config) -> dict:
    rng = random.Random(cfg.seed)
    users: list[dict] = []
    events: list[dict] = []
    subs: list[dict] = []

    # Скрытая правда A/B (только instructor key)
    # treatment: paywall чаще после streak_3 → выше CR habit→subscribe, ниже early paywall
    truth = {
        "experiment_id": "paywall_timing_2026q3",
        "hypothesis": (
            "Показывать paywall в основном после streak_3_reached "
            "повышает конверсию habit→subscribe за 14д и снижает долю ранних paywall_view."
        ),
        "primary_metric": "habit_to_subscribe_14d",
        "guardrails": ["d7_depth_ge3", "early_paywall_share"],
        "assignment": "50/50 на install (исключая is_internal)",
        "true_effects": {
            "control": {
                "habit_to_subscribe_14d": 0.08,
                "d7_depth_ge3": 0.48,
                "early_paywall_share": 0.43,
            },
            "treatment": {
                "habit_to_subscribe_14d": 0.14,
                "d7_depth_ge3": 0.62,
                "early_paywall_share": 0.10,
            },
            "absolute_lift_pp": {
                "habit_to_subscribe_14d": 6.0,
                "d7_depth_ge3": 14.0,
                "early_paywall_share": -33.0,
            },
            "winner": "treatment",
            "significant_primary": True,
            "note": "Эффекты — целевые параметры генератора; выборка шумит вокруг них.",
        },
        "student_visible_columns": ["ab_variant", "ab_experiment"],
        "do_not_share_with_students": True,
    }

    start_dt = datetime.combine(cfg.start, datetime.min.time(), tzinfo=MSK)
    end_dt = datetime.combine(cfg.end, datetime.max.time().replace(microsecond=0), tzinfo=MSK)

    ab_counts = {"control": 0, "treatment": 0, None: 0}
    metric_hits = {
        "control": {"habit": 0, "sub14": 0, "depth3": 0, "paywall": 0, "early_pw": 0},
        "treatment": {"habit": 0, "sub14": 0, "depth3": 0, "paywall": 0, "early_pw": 0},
    }

    for i in range(cfg.n_users):
        is_internal = rng.random() < 0.03
        installed = dt_between(rng, start_dt, end_dt - timedelta(days=8))
        platform = rng.choices(PLATFORMS, weights=PLATFORM_W, k=1)[0]

        if is_internal:
            variant = None
        else:
            variant = "control" if rng.random() < 0.5 else "treatment"
        ab_counts[variant] += 1

        user_id = f"u_{cfg.seed:04d}_{i:05d}"
        users.append(
            {
                "user_id": user_id,
                "installed_at": installed.isoformat(),
                "platform": platform,
                "is_internal": str(is_internal).lower(),
                "ab_variant": variant or "",
                "ab_experiment": "paywall_timing_2026q3" if variant else "",
                "country": "RU" if rng.random() > 0.08 else rng.choice(["KZ", "BY", "UZ"]),
            }
        )

        # --- воронка ---
        # app_open почти всегда
        if rng.random() < 0.97:
            events.append(make_event(rng, user_id, "app_open", installed, {"platform": platform}))

        # silent session_restored (грязь / антипаттерн из М4.3)
        if rng.random() < 0.12:
            events.append(
                make_event(
                    rng,
                    user_id,
                    "session_restored",
                    installed + timedelta(minutes=rng.randint(1, 40)),
                    {"platform": platform},
                )
            )

        # onboarding
        did_onb = rng.random() < (0.72 if not is_internal else 0.9)
        onb_ts = installed + timedelta(minutes=rng.randint(2, 90))
        if did_onb:
            if rng.random() < 0.15:
                # schema drift lite: step events вместо только completed
                for step in ("welcome", "goal", "reminder"):
                    events.append(
                        make_event(
                            rng,
                            user_id,
                            "onboarding_step_viewed",
                            onb_ts + timedelta(seconds=rng.randint(5, 120)),
                            {"step_name": step, "schema_version": "2"},
                        )
                    )
            events.append(
                make_event(
                    rng,
                    user_id,
                    "onboarding_completed",
                    onb_ts,
                    {"schema_version": rng.choice(["1", "1", "2"])},
                )
            )

        # habit
        habit_p = 0.58 if did_onb else 0.12
        if is_internal:
            habit_p = 0.85
        did_habit = rng.random() < habit_p
        habit_id = None
        habit_at = None
        if did_habit:
            habit_at = onb_ts + timedelta(minutes=rng.randint(1, 180)) if did_onb else installed + timedelta(hours=rng.randint(1, 48))
            habit_id = uid("hab")
            events.append(
                make_event(
                    rng,
                    user_id,
                    "habit_created",
                    habit_at,
                    {
                        "habit_id": habit_id,
                        "habit_type": rng.choice(HABIT_TYPES),
                        "schema_version": "1",
                    },
                )
            )
            # редкие правки = второй habit_created (ломает зерно, если count(*))
            if rng.random() < 0.08:
                events.append(
                    make_event(
                        rng,
                        user_id,
                        "habit_created",
                        habit_at + timedelta(days=rng.randint(1, 5)),
                        {
                            "habit_id": habit_id,
                            "habit_type": rng.choice(HABIT_TYPES),
                            "schema_version": "1",
                            "edit": True,
                        },
                    )
                )

        # check-ins / streak / depth
        check_days: set[date] = set()
        streak3_at = None
        if did_habit and habit_at is not None:
            # treatment чуть лучше удерживает чек-ины (слабый эффект на depth)
            base_keep = 0.55 if variant == "treatment" else 0.52
            n_days_active = 0
            for d in range(0, 21):
                day_dt = habit_at + timedelta(days=d, hours=rng.randint(6, 22))
                if day_dt > end_dt:
                    break
                p = base_keep * (0.92**d)
                if rng.random() < p:
                    n_days_active += 1
                    local_d = day_dt.astimezone(MSK).date()
                    check_days.add(local_d)
                    props = {
                        "habit_id": habit_id,
                        "source": rng.choice(["tap", "tap", "swipe"]),
                        "schema_version": "1",
                    }
                    # schema drift: иногда local_day вместо local_date; иногда null
                    if rng.random() < 0.12:
                        props["local_day"] = local_d.isoformat()
                    elif rng.random() < 0.08:
                        pass  # нет даты в props
                    else:
                        props["local_date"] = local_d.isoformat()

                    events.append(make_event(rng, user_id, "check_in", day_dt, props))

                    # дубли check_in (грязь)
                    if rng.random() < cfg.dirt_rate * 0.8:
                        events.append(
                            make_event(
                                rng,
                                user_id,
                                "check_in",
                                day_dt + timedelta(seconds=rng.randint(1, 30)),
                                {**props, "dup": True},
                            )
                        )

            # streak_3 когда накопили 3 уникальных дня
            if len(check_days) >= 3:
                ordered = sorted(check_days)
                third = ordered[2]
                streak3_at = datetime.combine(third, datetime.min.time(), tzinfo=MSK) + timedelta(
                    hours=rng.randint(8, 20)
                )
                events.append(
                    make_event(
                        rng,
                        user_id,
                        "streak_3_reached",
                        streak3_at,
                        {"habit_id": habit_id, "schema_version": "1"},
                    )
                )

        # paywall + subscribe (A/B)
        did_paywall = False
        early_paywall = False
        subscribed = False
        if did_habit and habit_at is not None:
            # control: часто early (day_7 / feature_lock); treatment: чаще streak_3
            if variant == "treatment":
                early_p, streak_p = 0.12, 0.55
            else:
                early_p, streak_p = 0.42, 0.35

            paywall_ts = None
            trigger = None
            if streak3_at and rng.random() < streak_p:
                paywall_ts = streak3_at + timedelta(minutes=rng.randint(1, 120))
                trigger = "streak_3"
            elif rng.random() < early_p:
                paywall_ts = habit_at + timedelta(days=rng.randint(0, 6), hours=rng.randint(1, 12))
                trigger = rng.choice(["day_7", "feature_lock"])
                early_paywall = True

            if paywall_ts and paywall_ts <= end_dt:
                did_paywall = True
                events.append(
                    make_event(
                        rng,
                        user_id,
                        "paywall_view",
                        paywall_ts,
                        {
                            "trigger": trigger,
                            "schema_version": "1",
                            # иногда null plan до выбора
                            **({"plan": None} if rng.random() < 0.2 else {}),
                        },
                    )
                )
                # дубль paywall_view в тот же день (модалка без дедупа)
                if rng.random() < 0.18:
                    events.append(
                        make_event(
                            rng,
                            user_id,
                            "paywall_view",
                            paywall_ts + timedelta(seconds=rng.randint(5, 90)),
                            {"trigger": trigger, "schema_version": "1", "dup": True},
                        )
                    )

                # CR subscribe от paywall: treatment выше (primary A/B)
                sub_p = 0.22 if variant == "treatment" else 0.12
                if is_internal:
                    sub_p = 0.45
                if rng.random() < sub_p:
                    subscribed = True
                    plan = rng.choices(["month", "year"], weights=[0.7, 0.3], k=1)[0]
                    sub_ts = paywall_ts + timedelta(minutes=rng.randint(1, 40))
                    events.append(
                        make_event(
                            rng,
                            user_id,
                            "subscribe_started",
                            sub_ts,
                            {"plan": plan, "schema_version": "1"},
                        )
                    )
                    price = 299 if plan == "month" else 1990
                    status = "active"
                    ended = None
                    if rng.random() < 0.12:
                        status = "canceled"
                        ended = (sub_ts + timedelta(days=rng.randint(10, 60))).isoformat()
                    # редко вторая подписка (month → year) — ловушка JOIN
                    subs.append(
                        {
                            "subscription_id": uid("sub"),
                            "user_id": user_id,
                            "started_at": sub_ts.isoformat(),
                            "plan": plan,
                            "status": status,
                            "price_rub": price,
                            "ended_at": ended or "",
                        }
                    )
                    if status == "active" and plan == "month" and rng.random() < 0.06:
                        year_ts = sub_ts + timedelta(days=rng.randint(20, 90))
                        if year_ts <= end_dt:
                            subs.append(
                                {
                                    "subscription_id": uid("sub"),
                                    "user_id": user_id,
                                    "started_at": year_ts.isoformat(),
                                    "plan": "year",
                                    "status": "active",
                                    "price_rub": 1990,
                                    "ended_at": "",
                                }
                            )
                            events.append(
                                make_event(
                                    rng,
                                    user_id,
                                    "subscribe_started",
                                    year_ts,
                                    {"plan": "year", "schema_version": "1", "upgrade": True},
                                )
                            )

        # антипаттерн button_click (шум)
        if rng.random() < cfg.dirt_rate * 1.5:
            events.append(
                make_event(
                    rng,
                    user_id,
                    "button_click",
                    installed + timedelta(minutes=rng.randint(1, 500)),
                    {"label": rng.choice(["orange_big", "continue", "screen_4"])},
                )
            )

        # null props / битый json-подобное (пустое)
        if rng.random() < cfg.dirt_rate * 0.5 and did_habit:
            events.append(
                make_event(
                    rng,
                    user_id,
                    "check_in",
                    habit_at + timedelta(days=rng.randint(0, 3)),  # type: ignore[operator]
                    {},  # нет habit_id / local_date
                )
            )

        # метрики для сверки ключа (только не internal)
        if variant in ("control", "treatment") and did_habit:
            m = metric_hits[variant]
            m["habit"] += 1
            depth_ge3 = len({d for d in check_days if habit_at and d <= (habit_at.astimezone(MSK).date() + timedelta(days=6))}) >= 3
            if depth_ge3:
                m["depth3"] += 1
            if did_paywall:
                m["paywall"] += 1
            if early_paywall:
                m["early_pw"] += 1
            if subscribed:
                # упрощённо: subscribe в данных уже в окне генерации ~14д
                m["sub14"] += 1

    # редкие дубли event_id (грязь) — второй insert с новым id, но тем же смыслом уже есть;
    # плюс один конфликтный дубль имени события с тем же payload
    if events and rng.random() < 0.5:
        clone = dict(rng.choice(events))
        clone["event_id"] = uid("evt")
        clone["props"] = clone["props"]  # already string later
        events.append(clone)

    # сериализуем props
    for e in events:
        if isinstance(e["props"], dict):
            # убрать Python None → JSON null
            e["props"] = json.dumps(e["props"], ensure_ascii=False, default=str)

    write_csv(
        cfg.out_dir / "users.csv",
        users,
        ["user_id", "installed_at", "platform", "is_internal", "ab_variant", "ab_experiment", "country"],
    )
    write_csv(
        cfg.out_dir / "events.csv",
        events,
        ["event_id", "user_id", "event_name", "ts", "props"],
    )
    write_csv(
        cfg.out_dir / "subscriptions.csv",
        subs,
        ["subscription_id", "user_id", "started_at", "plan", "status", "price_rub", "ended_at"],
    )

    # realized rates в ключ
    realized = {}
    for v in ("control", "treatment"):
        h = metric_hits[v]["habit"] or 1
        realized[v] = {
            "n_habit": metric_hits[v]["habit"],
            "habit_to_subscribe_14d": round(metric_hits[v]["sub14"] / h, 4),
            "d7_depth_ge3": round(metric_hits[v]["depth3"] / h, 4),
            "early_paywall_share_among_paywall": round(
                metric_hits[v]["early_pw"] / max(1, metric_hits[v]["paywall"]), 4
            ),
        }
    truth["realized_in_this_seed"] = realized
    truth["generator"] = {
        "seed": cfg.seed,
        "n_users": cfg.n_users,
        "window": [cfg.start.isoformat(), cfg.end.isoformat()],
        "ab_assignment_counts": {str(k): v for k, v in ab_counts.items()},
        "n_events": len(events),
        "n_subscriptions": len(subs),
    }

    if cfg.write_key:
        cfg.key_path.parent.mkdir(parents=True, exist_ok=True)
        cfg.key_path.write_text(json.dumps(truth, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "users": len(users),
        "events": len(events),
        "subscriptions": len(subs),
        "key": str(cfg.key_path) if cfg.write_key else None,
    }


def make_event(rng: random.Random, user_id: str, name: str, ts: datetime, props: dict) -> dict:
    # иногда сдвигаем ts микрошумом
    ts = ts + timedelta(seconds=rng.randint(0, 3))
    return {
        "event_id": uid("evt"),
        "user_id": user_id,
        "event_name": name,
        "ts": ts.isoformat(),
        "props": props,
    }


def csv_to_seed_sql(seed_dir: Path, out_sql: Path, limit_users: int | None = None) -> None:
    """Компактный SQL INSERT для initdb (маленький семпл)."""

    def cell(v: str) -> str:
        return "" if v is None else v

    users_raw = list(csv.DictReader((seed_dir / "users.csv").open(encoding="utf-8")))
    users = [{k: cell(v) for k, v in u.items()} for u in users_raw]
    if limit_users is not None:
        users = users[:limit_users]
    user_ids = {u["user_id"] for u in users}

    events = [
        {k: cell(v) for k, v in r.items()}
        for r in csv.DictReader((seed_dir / "events.csv").open(encoding="utf-8"))
        if cell(r["user_id"]) in user_ids
    ]
    subs = [
        {k: cell(v) for k, v in r.items()}
        for r in csv.DictReader((seed_dir / "subscriptions.csv").open(encoding="utf-8"))
        if cell(r["user_id"]) in user_ids
    ]

    lines = [
        "-- Автогенерированный семпл для docker initdb (можно перегенерировать)",
        "BEGIN;",
        "TRUNCATE subscriptions, events, users CASCADE;",
    ]

    def esc(s: str) -> str:
        return s.replace("'", "''")

    for u in users:
        ab = "NULL" if not u["ab_variant"] else f"'{esc(u['ab_variant'])}'"
        abe = "NULL" if not u["ab_experiment"] else f"'{esc(u['ab_experiment'])}'"
        lines.append(
            "INSERT INTO users (user_id, installed_at, platform, is_internal, ab_variant, ab_experiment, country) VALUES ("
            f"'{esc(u['user_id'])}', '{esc(u['installed_at'])}', '{esc(u['platform'])}', "
            f"{u['is_internal']}, {ab}, {abe}, '{esc(u['country'])}');"
        )

    for e in events:
        lines.append(
            "INSERT INTO events (event_id, user_id, event_name, ts, props) VALUES ("
            f"'{esc(e['event_id'])}', '{esc(e['user_id'])}', '{esc(e['event_name'])}', "
            f"'{esc(e['ts'])}', '{esc(e['props'])}'::jsonb);"
        )

    for s in subs:
        ended = "NULL" if not s["ended_at"] else f"'{esc(s['ended_at'])}'"
        lines.append(
            "INSERT INTO subscriptions (subscription_id, user_id, started_at, plan, status, price_rub, ended_at) VALUES ("
            f"'{esc(s['subscription_id'])}', '{esc(s['user_id'])}', '{esc(s['started_at'])}', "
            f"'{esc(s['plan'])}', '{esc(s['status'])}', {int(s['price_rub'])}, {ended});"
        )

    lines.append("COMMIT;")
    out_sql.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    here = Path(__file__).resolve().parent
    stand = here.parent
    p = argparse.ArgumentParser(description="Синтетика Ритма")
    p.add_argument("--n-users", type=int, default=80)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--start", default="2026-07-01")
    p.add_argument("--end", default="2026-09-10")
    p.add_argument("--out", type=Path, default=stand / "seed")
    p.add_argument("--key", type=Path, default=stand / "instructor" / "ab_ground_truth.json")
    p.add_argument("--no-key", action="store_true", help="Не писать ключ преподавателя (совместимость; по умолчанию ключ не пишется)")
    p.add_argument("--write-key", action="store_true", help="Писать ключ преподавателя (только локально у инструктора)")
    p.add_argument("--dirt-rate", type=float, default=0.12)
    p.add_argument("--full", action="store_true", help="Большой датасет (если n-users не задан явно — 2500)")
    p.add_argument("--write-sql-seed", action="store_true", help="Также пересобрать sql/03_seed.sql из CSV")
    p.add_argument("--sql-user-limit", type=int, default=80, help="Сколько users в sql/03_seed.sql")
    args = p.parse_args()

    n = args.n_users
    if args.full and args.n_users == 80:
        n = 2500

    cfg = Config(
        n_users=n,
        seed=args.seed,
        start=date.fromisoformat(args.start),
        end=date.fromisoformat(args.end),
        out_dir=args.out,
        key_path=args.key,
        dirt_rate=args.dirt_rate,
        write_key=bool(args.write_key) and not bool(args.no_key),
    )
    stats = generate(cfg)
    print(json.dumps(stats, ensure_ascii=False, indent=2))

    if args.write_sql_seed or n <= 120:
        csv_to_seed_sql(cfg.out_dir, stand / "sql" / "03_seed.sql", limit_users=args.sql_user_limit)
        print(f"wrote {stand / 'sql' / '03_seed.sql'}")


if __name__ == "__main__":
    main()
