Запуск:

1 `docker build -t airflow-with-dependencies .`

2 `docker-compose up --build`


Для репликации запустить dag "data_replication_dag"

Для инициализации витрин запустить dag "create_datamarket_dag", перед этим настроить соединение:

Connection id: postgresql

Host: postgres_target

Database: orders

Login: airflow

Password: airflow



Всего 3 витрины со следующими схемами:
```sql
-- Витрина: Сводка по продажам
CREATE TABLE sales_summary AS
SELECT
    pc.name AS category_name,
    SUM(od.total_price) AS total_sales,
    COUNT(DISTINCT o.id) AS total_orders,
    SUM(od.quantity) AS total_products_sold
FROM orderdetails od
JOIN product p ON od.product_id = p.id
JOIN productcategory pc ON p.category_id = pc.id
JOIN "order" o ON od.order_id = o.id
WHERE o.status = 3 -- Только завершенные заказы
GROUP BY pc.name;

-- Витрина: Анализ пользователей по программе лояльности
CREATE TABLE user_loyalty_summary AS
SELECT
    u.id AS user_id,
    u.first_name || ' ' || u.last_name AS full_name,
    u.loyalty_status,
    COUNT(o.id) AS total_orders,
    SUM(o.total_amount) AS total_spent
FROM "user" u
LEFT JOIN "order" o ON u.id = o.user_id
WHERE o.status = 3 -- Только завершенные заказы
GROUP BY u.id, u.first_name, u.last_name, u.loyalty_status;

-- Витрина: Статус складских запасов товаров
CREATE TABLE product_stock_status AS
SELECT
    p.id AS product_id,
    p.name AS product_name,
    pc.name AS category_name,
    p.stock_quantity,
    CASE 
        WHEN p.stock_quantity = 0 THEN 'Out of Stock'
        WHEN p.stock_quantity < 10 THEN 'Low Stock'
        ELSE 'In Stock'
    END AS stock_status
FROM product p
JOIN productcategory pc ON p.category_id = pc.id;
```
