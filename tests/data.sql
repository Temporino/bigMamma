INSERT INTO sales (date, item_id, item_name, quantity, price, total_price)
VALUES
  ('2021-01-01', 1, 'Pizza Mammargarita', 2, 10, 20),
  ('2021-01-01', 2, 'Tiramisu', 1, 5, 5);

INSERT OR REPLACE INTO items (id, name, price, category)
VALUES
  (1, 'Pizza Mammargarita', 10, 'Plat'),
  (2, 'Tiramisu', 5, 'Dessert');

INSERT INTO events (id, name, sport, dateFrom, dateTo, country)
VALUES
  (1, 'Tour de France', 'Cycling', '2021-01-01T00:00:00', '2021-01-31T00:00:00', 'France');