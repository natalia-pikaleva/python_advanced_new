SELECT c.full_name
    FROM customer c
    WHERE NOT EXISTS (
        SELECT 1
        FROM 'order' o
        WHERE c.customer_id = o.customer_id
                     );