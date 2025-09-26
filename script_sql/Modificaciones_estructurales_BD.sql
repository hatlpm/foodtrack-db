-- Modifcaciones estructurales

-- Revision de las bases datos

USE FoodTrackBD;

SELECT COUNT(*)
FROM foodtrucks;

SELECT *
FROM orders;

SELECT *
FROM order_items;

SELECT *
FROM products;

-- Agregar un orden nueva del foodtrucks 2


INSERT INTO orders (foodtruck_id, order_date, status, total)
VALUES (2,2023-10-05,'entregado',50), (2,2023-10-05,'entregado',80);

-- product_id,quantity