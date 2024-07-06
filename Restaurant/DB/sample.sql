SELECT * FROM alembic_version;

DELETE FROM alembic_version;

SELECT * FROM information_schema.tables WHERE table_schema = 'public';

INSERT INTO menu (name, description, price, availability) VALUES ('Pasta', 'Delicious pasta with tomato sauce', 12.99, TRUE);
INSERT INTO menu (name, description, price, availability) VALUES ('Pizza', 'qqqqqqqqqqqq pizza with pepperoni', 15.99, TRUE);
