SELECT c.full_name, m.full_name, o.purchase_amount, o.date
    FROM customer c, manager m, 'order' o
    WHERE c.customer_id = o.customer_id AND
          m.manager_id = o.manager_id;