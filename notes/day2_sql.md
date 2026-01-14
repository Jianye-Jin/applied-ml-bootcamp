# Day 2 — SQL Basics (SQLite)

This note contains:
- Toy tables: `users`, `events`, `orders`
- Query 1: GROUP BY aggregation
- Query 2: JOIN between users and orders

## Query 1 — GROUP BY (paid orders per user)

```sql
SELECT
  user_id,
  COUNT(*) AS paid_order_count,
  ROUND(SUM(amount), 2) AS paid_total_amount
FROM orders
WHERE status = 'paid'
GROUP BY user_id
ORDER BY paid_total_amount DESC;
```

Result:
| user_id | paid_order_count | paid_total_amount |
|---------|------------------|-------------------|
| 3       | 2                | 130.0             |
| 2       | 1                | 99.0              |
| 8       | 1                | 60.0              |
| 1       | 2                | 59.49             |
| 4       | 1                | 55.0              |
| 7       | 2                | 50.0              |
| 5       | 2                | 38.99             |

## Query 2 — JOIN (users + orders)

```sql
SELECT
  u.user_id,
  u.name,
  u.country,
  COUNT(o.order_id) AS paid_orders,
  ROUND(COALESCE(SUM(o.amount), 0), 2) AS paid_total
FROM users u
LEFT JOIN orders o
  ON u.user_id = o.user_id
 AND o.status = 'paid'
GROUP BY u.user_id, u.name, u.country
ORDER BY paid_total DESC, paid_orders DESC;
```

Result:
| user_id |    name     | country | paid_orders | paid_total |
|---------|-------------|---------|-------------|------------|
| 3       | Bob Chen    | CN      | 2           | 130.0      |
| 2       | Alice Wang  | UK      | 1           | 99.0       |
| 8       | Gavin Sun   | ES      | 1           | 60.0       |
| 1       | Jianye Jin  | UK      | 2           | 59.49      |
| 4       | Charlie Li  | UK      | 1           | 55.0       |
| 7       | Fiona Wu    | UK      | 2           | 50.0       |
| 5       | Daisy Zhang | DE      | 2           | 38.99      |
| 6       | Ethan Zhou  | FR      | 0           | 0.0        |

