Select * from alembic_version;
Delete from alembic_version;
Select * from information_schema.tables where table_schema = 'public';

Insert into menu (name,description,price,availability) values ('pasta','Delicious pasta with tomato sauce',12.99,True);
Insert into menu (name,description,price,availability) values ('pizza','pizza with pepperoni',15.99, True);
