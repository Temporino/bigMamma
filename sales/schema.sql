DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS events;

CREATE TABLE sales (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date DATE NOT NULL,
  item_id INTEGER NOT NULL,
  item_name TEXT,
  quantity INTEGER,
  price FLOAT,
  total_price FLOAT
);

CREATE TABLE items (
  id INTEGER PRIMARY KEY,
  name TEXT,
  price FLOAT,
  category TEXT
);

CREATE TABLE events (
  id INTEGER PRIMARY KEY,
  name TEXT,
  sport TEXT,
  dateFrom date,
  dateTo date,
  country TEXT
);