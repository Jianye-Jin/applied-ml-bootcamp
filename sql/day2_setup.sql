-- Day2: toy schema + seed data (SQLite)

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS orders;

CREATE TABLE users (
  user_id     INTEGER PRIMARY KEY,
  name        TEXT NOT NULL,
  email       TEXT NOT NULL,
  country     TEXT NOT NULL,
  signup_date TEXT NOT NULL
);

CREATE TABLE events (
  event_id    INTEGER PRIMARY KEY,
  user_id     INTEGER NOT NULL,
  event_type  TEXT NOT NULL,
  ts          TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE orders (
  order_id    INTEGER PRIMARY KEY,
  user_id     INTEGER NOT NULL,
  amount      REAL NOT NULL,
  status      TEXT NOT NULL, -- paid/refunded/failed
  created_at  TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users (user_id, name, email, country, signup_date) VALUES
  (1, 'Jianye Jin',  'jianye@example.com', 'UK', '2026-01-01'),
  (2, 'Alice Wang',  'alice@example.com', 'UK', '2026-01-02'),
  (3, 'Bob Chen',    'bob@example.com',   'CN', '2026-01-03'),
  (4, 'Charlie Li',  'charlie@example.com','UK','2026-01-03'),
  (5, 'Daisy Zhang', 'daisy@example.com', 'DE', '2026-01-04'),
  (6, 'Ethan Zhou',  'ethan@example.com', 'FR', '2026-01-05'),
  (7, 'Fiona Wu',    'fiona@example.com', 'UK', '2026-01-06'),
  (8, 'Gavin Sun',   'gavin@example.com', 'ES', '2026-01-07');

INSERT INTO events (event_id, user_id, event_type, ts) VALUES
  (1, 1, 'page_view', '2026-01-10T10:00:00Z'),
  (2, 1, 'signup',    '2026-01-01T09:00:00Z'),
  (3, 2, 'page_view', '2026-01-10T11:00:00Z'),
  (4, 2, 'purchase',  '2026-01-11T12:00:00Z'),
  (5, 3, 'page_view', '2026-01-10T12:30:00Z'),
  (6, 4, 'page_view', '2026-01-10T13:00:00Z'),
  (7, 5, 'purchase',  '2026-01-11T15:00:00Z'),
  (8, 6, 'page_view', '2026-01-12T16:00:00Z'),
  (9, 7, 'purchase',  '2026-01-12T18:00:00Z'),
  (10,8, 'page_view', '2026-01-13T08:00:00Z');

INSERT INTO orders (order_id, user_id, amount, status, created_at) VALUES
  (101, 1, 39.99, 'paid',     '2026-01-11T12:01:00Z'),
  (102, 1, 19.50, 'paid',     '2026-01-12T09:10:00Z'),
  (103, 1, 12.00, 'refunded', '2026-01-12T09:30:00Z'),
  (104, 2, 99.00, 'paid',     '2026-01-11T12:05:00Z'),
  (105, 2, 15.00, 'failed',   '2026-01-11T12:06:00Z'),
  (106, 3, 10.00, 'paid',     '2026-01-10T10:10:00Z'),
  (107, 3, 120.00,'paid',     '2026-01-13T10:10:00Z'),
  (108, 4, 55.00, 'paid',     '2026-01-12T14:00:00Z'),
  (109, 5, 8.99,  'paid',     '2026-01-11T15:10:00Z'),
  (110, 5, 30.00, 'paid',     '2026-01-12T15:20:00Z'),
  (111, 6, 70.00, 'refunded', '2026-01-12T16:10:00Z'),
  (112, 7, 25.00, 'paid',     '2026-01-12T18:10:00Z'),
  (113, 7, 25.00, 'paid',     '2026-01-13T18:10:00Z'),
  (114, 8, 60.00, 'paid',     '2026-01-13T08:10:00Z');
