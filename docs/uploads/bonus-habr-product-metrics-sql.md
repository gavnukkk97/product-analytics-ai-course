---
title: "Продуктовые метрики: пример расчета на SQL"
source: https://habr.com/ru/articles/1010980/
author: Habr
modules: [M3.2, M2.3]
downloaded: 2026-09-14
kind: bonus-open
---

# Продуктовые метрики: пример расчета на SQL

*Автор: Habr*  
*Источник: https://habr.com/ru/articles/1010980/*

У нас есть классифайд (например, Avito) и нам нужно рассчитать ключевые метрики, которые показывают здоровье продукта:

- **DAU/MAU** – вовлеченность
- **Conversion Rate** – конверсия в целевое действие (у нас это создание объявления)
- **Retention** – удержание пользователей
- **LTV** – жизненная ценность клиента
- **ARPPU** – средний доход с платящего пользователя

Разберем последовательный расчет с примером синтетических данных и готового кода.

Прежде всего, сформулируем, зачем нам это считать, на какие вопросы мы хотим ответить:

1. **Сколько у нас пользователей и активны ли они?** (DAU, MAU)
2. **Как пользователи доходят до создания объявления?** (Воронка)
3. **Возвращаются ли они?** (Retention)
4. **Сколько мы зарабатываем и с кого?** (ARPU, ARPPU, LTV)

### Шаг 1. DAU (Daily Active Users) Активные пользователи за день

Считаем количество уникальных пользователей, которые совершили хотя бы одно действие на сайте/в приложении за день. Метрика показывает "живую" аудиторию и если DAU падает - то пользователи уходят.

**Простой вариант:**

```
SELECT 
    event_date,
    COUNT(DISTINCT user_id) as dau
FROM user_events
WHERE event_date = '2024-01-15' -- конкретный день
GROUP BY event_date;

![]()
```

**Проблема:** Мы смотрим только один день и не видим динамику.

**Правильный вариант – смотрим на целый период, например, неделю с изменениями:**

```
WITH daily_users AS (
    -- Считаем DAU для каждого дня за последнюю неделю
    SELECT 
        event_date,
        COUNT(DISTINCT user_id) as dau,
        -- Сразу посчитаем отдельно мобилу и десктоп, чтобы видеть тренды
        COUNT(DISTINCT CASE WHEN device_type = 'mobile' THEN user_id END) as mobile_dau,
        COUNT(DISTINCT CASE WHEN device_type = 'desktop' THEN user_id END) as desktop_dau
    FROM user_events
    WHERE event_date BETWEEN CURRENT_DATE - 7 AND CURRENT_DATE - 1
    GROUP BY event_date
)
SELECT 
    event_date,
    dau,
    mobile_dau,
    desktop_dau,
    -- Считаем изменение в процентах к прошлому дню
    -- LAG берет значение предыдущей строки
    ROUND(
        (dau - LAG(dau) OVER (ORDER BY event_date)) * 100.0 / 
        LAG(dau) OVER (ORDER BY event_date), 
        2
    ) as daily_change_percent
FROM daily_users
ORDER BY event_date DESC;

![]()
```

#### Из важного в коде:

1. **WITH daily\_users AS (...)** тут создаем временную таблицу, чтобы не пересчитывать несколько раз
2. **COUNT(DISTINCT user\_id)** используем именно DISTINCT, чтобы одного пользователя, который зашел 10 раз, посчитать один раз
3. **CASE WHEN device\_type = 'mobile'** тут фильтруем внутри COUNT, чтобы получить мобильную аудиторию
4. **LAG(dau) OVER (ORDER BY event\_date)** здесь смотрим значение из предыдущей строки (вчерашний день)
5. **(dau - LAG(...)) / LAG(...)** тут считаем прирост в процентах

#### Пример результата с пояснением:

| event\_date | dau | mobile\_dau | desktop\_dau | daily\_change |
| --- | --- | --- | --- | --- |
| 2024-01-15 | 12500 | 9800 | 2700 | +2.5% |
| 2024-01-14 | 12200 | 9500 | 2700 | -1.2% |
| 2024-01-13 | 12350 | 9600 | 2750 | +5.8% |

**Что видим:** Аудитория растет, в основном за счет мобайла, десктоп в целом стабилен.

### Шаг 2. Stickiness (Липкость) MAU/DAU

Отношение средней дневной аудитории к месячной, метрика показывает, как часто пользователи возвращаются, если у вас 1 млн пользователей в месяц, но каждый день заходит только 100 тыс. – это плохо (липкость 10%), значит люди пришли, посмотрели и забыли, здесь хороший показатель от 20%.

#### Логика расчета

```
WITH monthly_stats AS (
    -- Считаем MAU (уникальные пользователи за 30 дней)
    SELECT 
        COUNT(DISTINCT user_id) as mau
    FROM user_events
    WHERE event_date BETWEEN CURRENT_DATE - 30 AND CURRENT_DATE - 1
),
daily_avg AS (
    -- Считаем средний DAU за те же 30 дней
    SELECT 
        AVG(daily_users) as avg_dau
    FROM (
        SELECT 
            event_date,
            COUNT(DISTINCT user_id) as daily_users
        FROM user_events
        WHERE event_date BETWEEN CURRENT_DATE - 30 AND CURRENT_DATE - 1
        GROUP BY event_date
    ) t
)
SELECT 
    ROUND(avg_dau / mau * 100, 2) as stickiness_percent
FROM monthly_stats, daily_avg;

![]()
```

### Из важного в коде:

1. **MAU** – это все, кто хоть раз зашел за месяц (потенциальная аудитория)
2. **Средний DAU** – это сколько в среднем приходит каждый день
3. **Делим avg\_DAU на MAU** – так мы получаем долю месячной аудитории, которая приходит ежедневно

**Пример:** MAU = 100 000, средний DAU = 25 000 тогда Stickiness = 25%, отлично, каждый четвертый пользователь заходит ежедневно.

### Шаг 3. Воронка конверсии (Conversion Funnel)

Считаем сколько пользователей доходит до ключевых шагов: зашел – поискал – создал объявление, так монимаем, где теряем пользователей, то есть если до поиска доходят 80%, а до создания только 5% значит, проблема в форме создания объявления.

**Сначала думаем, какие шаги есть в воронке:**  
**Визит** – пользователь зашел на сайт  
**Поиск** – начал искать (значит, заинтересован)  
**Создание** – дошел до публикации объявления (наша цель)

```
WITH funnel_base AS (
    -- Для каждого пользователя отмечаем, делал ли он каждый шаг
    SELECT 
        user_id,
        -- MAX дает 1, если было хоть одно такое событие
        MAX(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) as visited,
        MAX(CASE WHEN event_type = 'search' THEN 1 ELSE 0 END) as searched,
        MAX(CASE WHEN event_type = 'create_ads' THEN 1 ELSE 0 END) as created_ads
    FROM user_events
    WHERE event_date BETWEEN CURRENT_DATE - 30 AND CURRENT_DATE - 1
    GROUP BY user_id
),
funnel_stats AS (
    SELECT 
        COUNT(*) as total_users, -- вообще все, кто был активен
        SUM(visited) as visited_users,
        SUM(searched) as searched_users,
        SUM(created_ads) as creators
    FROM funnel_base
)
SELECT 
    visited_users as step_1_visit,
    -- Конверсия из визита в поиск
    ROUND(100.0 * searched_users / visited_users, 2) as search_conv_percent,
    searched_users as step_2_search,
    -- Конверсия из поиска в создание
    ROUND(100.0 * creators / searched_users, 2) as create_conv_percent,
    creators as step_3_create,
    -- Общая конверсия (из визита в создание)
    ROUND(100.0 * creators / visited_users, 2) as overall_conv_percent
FROM funnel_stats;

![]()
```

### Из важного в коде:

1. **MAX(CASE WHEN...)** – если у пользователя было событие, MAX вернет 1, если не было то 0.
2. **SUM(visited)** – сколько пользователей с visited = 1
3. **100.0 \* searched\_users / visited\_users** – тут умножаем на 100.0, чтобы получить дробное число, а не целое (иначе будет целочисленное деление)

#### Что видим в результате:

| Метрика | Значение |
| --- | --- |
| Визиты | 45,000 |
| Поиск | 28,000 (62,2%) |
| Создание | 3,200 (11,4% от поиска, 7,1% от визитов) |

**Вывод:** Проблема не в привлечении (62% ищут), а в создании (только 11% ищущих создают объявление), нужно упрощать форму или как минимум улучшать онбординг пользователей.

### Шаг 4. Детализация воронки по категориям

Считаем конверсию в создание объявления для разных категорий товаров. Может быть такое, в авто конверсия высокая (там профессионалы), а в услугах низкая (там сложнее оформить), так будем улучшать проблемные категории.

#### Логика

```
WITH ads_funnel AS (
    SELECT 
        u.user_id,
        u.city,
        -- Берем категорию из объявления, если оно есть
        COALESCE(a.category_id::text, 'no_ads') as category,
        -- Был ли факт создания объявления за период
        MAX(CASE WHEN ue.event_type = 'create_ads' THEN 1 ELSE 0 END) as created
    FROM users u
    -- Присоединяем события (LEFT JOIN, чтобы были все пользователи)
    LEFT JOIN user_events ue ON u.user_id = ue.user_id 
        AND ue.event_date BETWEEN CURRENT_DATE - 30 AND CURRENT_DATE - 1
    -- Присоединяем объявления, созданные за период
    LEFT JOIN ads a ON u.user_id = a.user_id 
        AND a.created_at BETWEEN CURRENT_DATE - 30 AND CURRENT_DATE - 1
    WHERE u.registration_date <= CURRENT_DATE - 1
    GROUP BY u.user_id, u.city, COALESCE(a.category_id::text, 'no_ads')
)
SELECT 
    category,
    COUNT(*) as users_in_category,
    SUM(created) as created_ads,
    ROUND(100.0 * SUM(created) / COUNT(*), 2) as conversion_rate
FROM ads_funnel
WHERE category != 'no_ads' -- убираем тех, у кого нет объявлений
GROUP BY category
ORDER BY conversion_rate DESC;

![]()
```

#### Из важного в коде:

1. **LEFT JOIN user\_events** – берем всех пользователей, даже если у них не было событий (на всякий случай)
2. **LEFT JOIN ads** – берем объявления пользователей
3. **COALESCE** – если категории нет (нет объявлений), пишем 'no\_ads'
4. **WHERE category != 'no\_ads'** – в финале смотрим только на тех, у кого есть объявления (иначе конверсия будет 0% у всех без объявлений)

### Шаг 5. Retention (Удержание) — когортный анализ

Считаем сколько пользователей возвращается через 1, 2, 4 недели после регистрации. Это показывает качество трафика, если retention высокий то это говорит о том, что пользователям нравится продукт и они за ним возвращаются, а если после первой недели остаются 10% значит, что мы кого-то не тех привлекаем.

#### Логика (пошагово)

**Шаг 1. Определяем когорты**  
Когорта – это группа пользователей, зарегистрировавшихся в одну неделю.

```
WITH user_cohorts AS (
    SELECT 
        user_id,
        -- Округляем дату до начала недели
        DATE_TRUNC('week', registration_date) as cohort_week
    FROM users
    WHERE registration_date >= CURRENT_DATE - 90
)

![]()
```

**Шаг 2. Смотрим активность этих пользователей по неделям**

```
,
user_activity AS (
    SELECT 
        uc.user_id,
        uc.cohort_week,
        -- Округляем дату события до недели
        DATE_TRUNC('week', ue.event_date) as activity_week
    FROM user_cohorts uc
    JOIN user_events ue ON uc.user_id = ue.user_id
    WHERE ue.event_date >= uc.cohort_week -- только после регистрации
    GROUP BY uc.user_id, uc.cohort_week, DATE_TRUNC('week', ue.event_date)
)

![]()
```

**Шаг 3. Считаем размер каждой когорты**

```
,
cohort_size AS (
    SELECT 
        cohort_week,
        COUNT(DISTINCT user_id) as users_in_cohort
    FROM user_cohorts
    GROUP BY cohort_week
)

![]()
```

**Шаг 4. Считаем retention**

```
SELECT 
    cs.cohort_week,
    cs.users_in_cohort,
    -- Неделя 0 (неделя регистрации)
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN ua.activity_week = cs.cohort_week THEN ua.user_id END) / cs.users_in_cohort, 2) as week_0,
    -- Неделя 1 (регистрация + 7 дней)
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN ua.activity_week = cs.cohort_week + INTERVAL '1 week' THEN ua.user_id END) / cs.users_in_cohort, 2) as week_1,
    -- Неделя 2
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN ua.activity_week = cs.cohort_week + INTERVAL '2 week' THEN ua.user_id END) / cs.users_in_cohort, 2) as week_2,
    -- Неделя 4
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN ua.activity_week = cs.cohort_week + INTERVAL '4 week' THEN ua.user_id END) / cs.users_in_cohort, 2) as week_4
FROM cohort_size cs
LEFT JOIN user_activity ua ON cs.cohort_week = ua.cohort_week
GROUP BY cs.cohort_week, cs.users_in_cohort
ORDER BY cs.cohort_week DESC;

![]()
```

#### Что значит каждая колонка?

**week\_0** — 100% всегда (все зашли в неделю регистрации)  
**week\_1** — сколько вернулось через неделю  
**week\_2** — через две  
**week\_4** — через месяц

**Пример хорошего retention:**

| Когорта | Week 0 | Week 1 | Week 2 | Week 4 |
| --- | --- | --- | --- | --- |
| 2024-12-01 | 100% | 35% | 30% | 25% |

Это значит: через месяц возвращается каждый четвертый

### Шаг 6. Метрики монетизации (ARPU, ARPPU)

**ARPU (Average Revenue Per User)** – это средний доход со ВСЕХ пользователей

**ARPPU (Average Revenue Per Paying User)** – это средний доход с ПЛАТЯЩИХ пользователей

ARPU показывает общую эффективность монетизации, а ARPPU уже сколько тратят те, кто платит (качество платящей аудитории).

#### Логика

```
WITH monthly_revenue AS (
    SELECT 
        DATE_TRUNC('month', payment_date) as month,
        COUNT(DISTINCT user_id) as paying_users,
        SUM(amount) as total_revenue,
        AVG(amount) as avg_check
    FROM payments
    WHERE payment_date >= CURRENT_DATE - 90
    GROUP BY DATE_TRUNC('month', payment_date)
),
monthly_active AS (
    SELECT 
        DATE_TRUNC('month', event_date) as month,
        COUNT(DISTINCT user_id) as active_users
    FROM user_events
    WHERE event_date >= CURRENT_DATE - 90
    GROUP BY DATE_TRUNC('month', event_date)
)
SELECT 
    mr.month,
    ma.active_users,
    mr.paying_users,
    -- Доля платящих
    ROUND(100.0 * mr.paying_users / ma.active_users, 2) as paying_share_percent,
    -- ARPU = весь доход / все активные
    ROUND(mr.total_revenue / ma.active_users, 2) as arpu,
    -- ARPPU = весь доход / платящие
    ROUND(mr.total_revenue / mr.paying_users, 2) as arppu,
    ROUND(mr.avg_check, 2) as avg_check
FROM monthly_revenue mr
JOIN monthly_active ma ON mr.month = ma.month
ORDER BY mr.month DESC;

![]()
```

#### Важное различие:

**ARPU** всегда меньше ARPPU (если платят не все)  
**ARPU = ARPPU × (% paying users)**

**Пример:**

Активных: 100 000  
Платящих: 3 000 (3%)  
Доход: 1 500 000 руб.

ARPU = 1 500 000 / 100 000 = 15 руб.  
ARPPU = 1 500 000 / 3 000 = 500 руб.

Каждый платящий приносит 500 руб., но в среднем по всем — 15 руб.

### Шаг 7. LTV (Life Time Value) – упрощенный расчет

Считаем сколько денег приносит пользователь за все время жизни, чтобы понимать, сколько мы можем потратить на привлечение пользователя (CAC должен быть меньше LTV).

#### Логика (по месяцам с момента регистрации)

```
WITH user_ltv AS (
    SELECT 
        u.user_id,
        DATE_TRUNC('month', u.registration_date) as cohort,
        -- Сколько месяцев прошло с регистрации до платежа
        EXTRACT(MONTH FROM AGE(p.payment_date, u.registration_date)) as lifetime_month,
        SUM(p.amount) as monthly_revenue
    FROM users u
    LEFT JOIN payments p ON u.user_id = p.user_id
    WHERE u.registration_date >= CURRENT_DATE - 180
    GROUP BY u.user_id, DATE_TRUNC('month', u.registration_date), 
             EXTRACT(MONTH FROM AGE(p.payment_date, u.registration_date))
)
SELECT 
    cohort,
    lifetime_month,
    COUNT(DISTINCT user_id) as users_in_cohort,
    SUM(monthly_revenue) as total_revenue,
    -- Накопленный доход на пользователя
    ROUND(SUM(monthly_revenue) / NULLIF(COUNT(DISTINCT user_id), 0), 2) as revenue_per_user
FROM user_ltv
WHERE lifetime_month <= 6
GROUP BY cohort, lifetime_month
ORDER BY cohort, lifetime_month;

![]()
```

#### Что мы видим:

Для когорты января:  
1-й месяц: доход 15 руб/чел  
2-й месяц: +5 руб/чел  
3-й месяц: +3 руб/чел  
Итого LTV за 3 месяца = 23 руб/чел

Значит, на привлечение можно тратить не больше 23 руб. (если хотим окупаться за 3 месяца).

### Шаг 8. Итоговый сбор (все метрики на одной странице)

```
-- Все метрики за сегодня
WITH today_metrics AS (
    SELECT 
        (SELECT COUNT(DISTINCT user_id) 
         FROM user_events 
         WHERE event_date = CURRENT_DATE) as dau,
        
        (SELECT COUNT(*) 
         FROM ads 
         WHERE created_at = CURRENT_DATE) as new_ads_today,
        
        (SELECT COALESCE(SUM(amount), 0) 
         FROM payments 
         WHERE payment_date = CURRENT_DATE) as revenue_today,
        
        (SELECT COUNT(DISTINCT user_id) 
         FROM payments 
         WHERE payment_date = CURRENT_DATE) as paying_users_today
)
SELECT 
    dau,
    new_ads_today,
    revenue_today,
    paying_users_today,
    -- Процент платящих от активных
    CASE 
        WHEN dau > 0 
        THEN ROUND(100.0 * paying_users_today / dau, 2)
        ELSE 0 
    END as paying_share_percent,
    -- ARPU за сегодня
    CASE 
        WHEN dau > 0 
        THEN ROUND(revenue_today / dau, 2)
        ELSE 0 
    END as arpu_today
FROM today_metrics;

![]()
```

#### Что мы видим с утра:

**DAU**: 12 500 человек уже зашли  
**New Ads**: 450 новых объявлений  
**Revenue**: 125 000 руб заработали  
**Paying Users**: 380 человек заплатили  
**Paying Share**: 3,04% платящих  
**ARPU**: 10 руб с пользователя

### Важные замечания при расчете метрик:

1. **Всегда используйте DISTINCT** в COUNT пользователей, иначе одного человека посчитаете много раз
2. **Дроби умножайте на 100.0**, а не на 100, чтобы получить проценты с дробной частью
3. **NULLIF(знаменатель, 0)** – это защита от деления на ноль
4. **Считайте в динамике** (не только сегодня, но и вчера, неделю назад)
5. **Детализируйте** (по устройствам, городам, категориям), иначе не увидите проблемы

Для генерации данных, чтобы повторить код используйте скрипты из пункта ниже

### Генерация тестовых данных для классифайда

```
-- Создаем схемы
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS user_events;
DROP TABLE IF EXISTS ads;
DROP TABLE IF EXISTS users;

-- 1. Таблица пользователей (1000 пользователей)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    registration_date DATE,
    user_type VARCHAR(20),
    city VARCHAR(100),
    is_verified BOOLEAN
);

-- Генерируем пользователей с разными паттернами
INSERT INTO users (registration_date, user_type, city, is_verified)
SELECT 
    -- Регистрации равномерно за последние 180 дней
    CURRENT_DATE - (random() * 180)::int,
    -- 70% частных, 30% бизнесов
    CASE WHEN random() < 0.7 THEN 'private' ELSE 'business' END,
    -- Города с весами
    CASE 
        WHEN random() < 0.4 THEN 'Москва'
        WHEN random() < 0.6 THEN 'СПб'
        WHEN random() < 0.75 THEN 'Казань'
        WHEN random() < 0.85 THEN 'Новосибирск'
        ELSE 'Другой'
    END,
    -- 60% верифицированных
    random() < 0.6
FROM generate_series(1, 1000);

-- 2. Таблица объявлений (5000 объявлений)
CREATE TABLE ads (
    ad_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    category_id INT,
    price DECIMAL(10,2),
    created_at DATE,
    status VARCHAR(20)
);

-- Генерируем объявления
INSERT INTO ads (user_id, category_id, price, created_at, status)
SELECT 
    u.user_id,
    -- Категории с распределением
    CASE 
        WHEN random() < 0.25 THEN 1 -- Авто
        WHEN random() < 0.45 THEN 2 -- Недвижимость
        WHEN random() < 0.65 THEN 3 -- Услуги
        WHEN random() < 0.80 THEN 4 -- Электроника
        ELSE 5 -- Прочее
    END,
    -- Цены в зависимости от категории
    CASE 
        WHEN random() < 0.25 THEN (random() * 1500000 + 50000)::int -- Авто дорого
        WHEN random() < 0.45 THEN (random() * 10000000 + 1000000)::int -- Недвижимость очень дорого
        WHEN random() < 0.65 THEN (random() * 5000 + 500)::int -- Услуги среднее
        WHEN random() < 0.80 THEN (random() * 30000 + 1000)::int -- Электроника
        ELSE (random() * 10000 + 100)::int -- Прочее
    END,
    -- Дата создания за последние 90 дней
    CURRENT_DATE - (random() * 90)::int,
    -- Статус: 60% активны, 30% проданы, 10% в архиве
    CASE 
        WHEN random() < 0.6 THEN 'active'
        WHEN random() < 0.9 THEN 'sold'
        ELSE 'archived'
    END
FROM users u, generate_series(1, 5) -- по 5 объявлений на пользователя в среднем
WHERE random() < 0.7; -- но не у всех

-- 3. Таблица событий (активность пользователей) - 50,000 записей
CREATE TABLE user_events (
    event_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    event_date DATE,
    event_type VARCHAR(50),
    page_url VARCHAR(200),
    device_type VARCHAR(20)
);

-- Генерируем события
INSERT INTO user_events (user_id, event_date, event_type, page_url, device_type)
SELECT 
    u.user_id,
    -- Дата события в течение последних 60 дней
    CURRENT_DATE - (random() * 60)::int,
    -- Тип события с распределением
    CASE 
        WHEN random() < 0.5 THEN 'view'
        WHEN random() < 0.75 THEN 'search'
        WHEN random() < 0.9 THEN 'create_ads'
        WHEN random() < 0.97 THEN 'call'
        ELSE 'payment'
    END,
    -- URL в зависимости от события
    CASE 
        WHEN random() < 0.5 THEN '/'
        ELSE '/category=' || (1 + (random() * 5)::int)
    END,
    -- 70% мобила, 30% десктоп
    CASE WHEN random() < 0.7 THEN 'mobile' ELSE 'desktop' END
FROM users u, generate_series(1, 50) -- по 50 событий на пользователя
WHERE random() < 0.6; -- но не у всех

-- 4. Таблица платежей (монетизация) - 1000 записей
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    payment_date DATE,
    amount DECIMAL(10,2),
    service_type VARCHAR(50)
);

-- Генерируем платежи (только для части пользователей)
INSERT INTO payments (user_id, payment_date, amount, service_type)
SELECT 
    u.user_id,
    -- Дата платежа за последние 90 дней
    CURRENT_DATE - (random() * 90)::int,
    -- Сумма в зависимости от услуги
    CASE 
        WHEN random() < 0.4 THEN 299 -- выделение
        WHEN random() < 0.7 THEN 999 -- поднятие
        ELSE 4990 -- пакет
    END,
    CASE 
        WHEN random() < 0.4 THEN 'vip'
        WHEN random() < 0.7 THEN 'raise'
        ELSE 'package'
    END
FROM users u, generate_series(1, 3) -- по 3 платежа максимум
WHERE random() < 0.15; -- только 15% пользователей платят

![]()
```

### Создание реалистичных паттернов

Чтобы данные были максимально приближены к реальности, добавим **специфические паттерны поведения**:

#### 1. Добавим "золотых" клиентов (рекламодателей)

```
-- Создадим 20 "идеальных" рекламодателей
WITH gold_users AS (
    SELECT user_id FROM users 
    WHERE user_type = 'business' 
    ORDER BY random() 
    LIMIT 20
)
-- Добавим им много платежей
INSERT INTO payments (user_id, payment_date, amount, service_type)
SELECT 
    g.user_id,
    CURRENT_DATE - (random() * 180)::int,
    CASE WHEN random() < 0.3 THEN 4990 ELSE 999 END,
    CASE WHEN random() < 0.3 THEN 'package' ELSE 'raise' END
FROM gold_users g, generate_series(1, 10)
WHERE random() < 0.8;

-- Добавим им много объявлений
INSERT INTO ads (user_id, category_id, price, created_at, status)
SELECT 
    g.user_id,
    1 + (random() * 4)::int,
    (random() * 100000)::int,
    CURRENT_DATE - (random() * 60)::int,
    'active'
FROM gold_users g, generate_series(1, 20)
WHERE random() < 0.9;

![]()
```

#### 2. Добавим "мертвые души" (зарегистрировались и ушли)

```
-- 100 пользователей, которые были активны только в первую неделю
WITH dead_users AS (
    SELECT user_id FROM users 
    ORDER BY random() 
    LIMIT 100
)
-- Добавим им события только в первую неделю после регистрации
INSERT INTO user_events (user_id, event_date, event_type, page_url, device_type)
SELECT 
    d.user_id,
    u.registration_date + (random() * 7)::int,
    'view',
    '/',
    'mobile'
FROM dead_users d
JOIN users u ON d.user_id = u.user_id
WHERE random() < 0.3;

![]()
```

#### 3. Добавим сезонных продавцов

```
-- Продавцы шин (сезонный товар)
WITH tire_sellers AS (
    SELECT user_id FROM users 
    WHERE city IN ('Москва', 'СПб')
    ORDER BY random() 
    LIMIT 30
)
-- Добавим объявления о шинах (категория авто) только в октябре-ноябре
INSERT INTO ads (user_id, category_id, price, created_at, status)
SELECT 
    t.user_id,
    1, -- авто
    (random() * 20000 + 5000)::int,
    '2024-10-' || (10 + (random() * 20)::int), -- даты в октябре
    'active'
FROM tire_sellers t, generate_series(1, 5);

![]()
```

**💚Еще больше про будни и задачи аналитика данных в бигтехе в моем тг канале 🌸**[**Таня и Данные**](https://t.me/+hLjunyJnpFVmNGVi)**📊**

📙**Предыдущие статьи для старта карьеры:**  
  - [Базовый минимум для старта в аналитике](https://habr.com/ru/articles/1003704/)  
  - [Как стать аналитиком с нуля (и не потратить на это много денег)](https://habr.com/ru/articles/1004742/)  
  - [Обзор книг](https://habr.com/ru/articles/1007024/)  
 - [SQL в 2026 для аналитика (с чего начать, где учиться и что реально нужно знать)](https://habr.com/ru/articles/1008826/)  
 - [Что реально нужно знать в Python начинающему аналитик](https://habr.com/ru/articles/1010316/)у

Предыдущие статьи-разборы задач:  
[https://habr.com/ru/articles/1005262/](https://habr.com/ru/articles/1005262/https://habr.com/ru/articles/1005284/)  
[https://habr.com/ru/articles/1005284/](https://habr.com/ru/articles/1005262/https://habr.com/ru/articles/1005284/)
