SELECT DISTINCT
    CASE
        WHEN c1.full_name < c2.full_name THEN c1.full_name
        ELSE c2.full_name
        END AS customer1,
    CASE
        WHEN c1.full_name < c2.full_name THEN c2.full_name
        ELSE c1.full_name
        END AS customer2

    FROM customer c1, customer c2

    WHERE c1.city = c2.city
        AND c1.customer_id <> c2.customer_id
        AND c1.manager_id = c2.manager_id;