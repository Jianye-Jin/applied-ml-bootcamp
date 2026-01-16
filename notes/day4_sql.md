# Day 4 — SQL x2 (Time Window + Conversion)

## Data
Tables: `users`, `events`, `orders` (SQLite: `data/day2.db`)

## Window definition (口径)
To make the “last 7 days” query stable even if we run it later, we anchor the window by the latest date in the dataset:
- `end_date` = MAX date across `events.ts` and `orders.created_at`
- `start_date` = `end_date - 6 days`
- Window is inclusive: `DATE(...) BETWEEN start_date AND end_date`

## Query 1 — Time window: daily paid orders (last 7 days)

**Definition:** paid orders grouped by day within the anchored 7-day window.

```sql
WITH max_dates AS (
  SELECT MAX(d) AS end_date
  FROM (
    SELECT DATE(ts) AS d FROM events
    UNION ALL
    SELECT DATE(created_at) AS d FROM orders
  )
),
window AS (
  SELECT DATE(end_date, '-6 day') AS start_date, end_date
  FROM max_dates
)
SELECT
  DATE(o.created_at) AS day,
  COUNT(*) AS paid_orders,
  ROUND(SUM(o.amount), 2) AS paid_revenue
FROM orders o, window w
WHERE o.status = 'paid'
  AND DATE(o.created_at) BETWEEN w.start_date AND w.end_date
GROUP BY day
ORDER BY day;
```

Result:
|    day     | paid_orders | paid_revenue |
|------------|-------------|--------------|
| 2026-01-10 | 1           | 10.0         |
| 2026-01-11 | 3           | 147.98       |
| 2026-01-12 | 4           | 129.5        |
| 2026-01-13 | 3           | 205.0        |

## Query 2 — Conversion: event users -> paid order users (last 7 days)

**Definition (口径):**
- Active (event) users: distinct users with >=1 event in the window.
- Converted users: active users with >=1 paid order in the same window.
- Conversion rate = converted / active.

```sql
WITH max_dates AS (
  SELECT MAX(d) AS end_date
  FROM (
    SELECT DATE(ts) AS d FROM events
    UNION ALL
    SELECT DATE(created_at) AS d FROM orders
  )
),
window AS (
  SELECT DATE(end_date, '-6 day') AS start_date, end_date
  FROM max_dates
),
active AS (
  SELECT DISTINCT e.user_id
  FROM events e, window w
  WHERE DATE(e.ts) BETWEEN w.start_date AND w.end_date
),
buyers AS (
  SELECT DISTINCT o.user_id
  FROM orders o, window w
  WHERE o.status = 'paid'
    AND DATE(o.created_at) BETWEEN w.start_date AND w.end_date
)
SELECT
  u.country,
  COUNT(DISTINCT a.user_id) AS active_users,
  COUNT(DISTINCT CASE WHEN b.user_id IS NOT NULL THEN a.user_id END) AS converted_users,
  ROUND(
    1.0 * COUNT(DISTINCT CASE WHEN b.user_id IS NOT NULL THEN a.user_id END)
    / NULLIF(COUNT(DISTINCT a.user_id), 0),
    4
  ) AS conversion_rate
FROM users u
JOIN active a ON u.user_id = a.user_id
LEFT JOIN buyers b ON a.user_id = b.user_id
GROUP BY u.country
ORDER BY conversion_rate DESC, active_users DESC;
```

Result:
| country | active_users | converted_users | conversion_rate |
|---------|--------------|-----------------|-----------------|
| UK      | 4            | 4               | 1.0             |
| CN      | 1            | 1               | 1.0             |
| DE      | 1            | 1               | 1.0             |
| ES      | 1            | 1               | 1.0             |
| FR      | 1            | 0               | 0.0             |

