SELECT Product.model, PC.price
    FROM Product, PC
    WHERE Product.maker = 'B'
        AND Product.model = PC.model
UNION
SELECT Product.model, Laptop.price
    FROM Product, Laptop
    WHERE Product.maker = 'B'
        AND Product.model = Laptop.model
UNION
SELECT Product.model, Printer.price
    FROM Product, Printer
    WHERE Product.maker = 'B'
        AND Product.model = Printer.model;