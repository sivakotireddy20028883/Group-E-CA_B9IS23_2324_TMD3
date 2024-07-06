INSERT INTO customers (name, contact_details, order_history)
VALUES
    ('John Doe', '123-456-7890', '[{"date": "2024-06-20", "items": [{"name": "Burger", "price": 9.99}, {"name": "Fries", "price": 4.99}]}]'),
    ('Jane Smith', '456-789-0123', '[{"date": "2024-06-19", "items": [{"name": "Salad", "price": 7.99}, {"name": "Soup", "price": 5.99}]}]');

INSERT INTO menu (name, description, price, availability)
VALUES
    ('Burger', 'Juicy beef patty with cheese and veggies', 9.99, TRUE),
    ('Fries', 'Crispy golden fries', 4.99, TRUE),
    ('Salad', 'Fresh greens with assorted vegetables', 7.99, TRUE),
    ('Soup', 'Homemade soup of the day', 5.99, TRUE),
    ('Pizza', 'Classic Italian pizza with various toppings', 12.99, TRUE);

INSERT INTO orders (customer_id, order_details, order_status, timestamp)
VALUES
    (1, '{"items": [{"name": "Burger", "quantity": 1}, {"name": "Fries", "quantity": 1}]}', 'delivered', CURRENT_TIMESTAMP),
    (2, '{"items": [{"name": "Salad", "quantity": 2}]}', 'pending', CURRENT_TIMESTAMP);

INSERT INTO users (username, password, role)
VALUES
    ('admin', 'admin123', 'admin'),
    ('manager', 'manager123', 'manager'),
    ('waiter1', 'waiter123', 'waiter'),
    ('chef1', 'chef123', 'chef');
