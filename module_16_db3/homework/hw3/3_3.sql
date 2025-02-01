SELECT DISTINCT maker
FROM Product, PC
WHERE Product.Model = PC.model
    AND PC.speed >= 450;