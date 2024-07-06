INSERT INTO orders (customer_id, order_details, order_status, timestamp)
VALUES
    (1, '{"items": [{"name": "Burger", "quantity": 1}, {"name": "Fries", "quantity": 1}]}', 'delivered', CURRENT_TIMESTAMP),
    (2, '{"items": [{"name": "Salad", "quantity": 2}]}', 'pending', CURRENT_TIMESTAMP);
