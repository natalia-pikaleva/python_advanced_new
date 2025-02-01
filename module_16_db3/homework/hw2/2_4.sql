SELECT c.full_name AS customer_name, o.order_no AS order_number
    FROM `order` o
    JOIN customer c ON o.customer_id = c.customer_id
    WHERE o.manager_id IS NULL;