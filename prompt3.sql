-- Comprehensive join between Customers, Orders, OrderItems, Products, and Payments
SELECT
    Customers.CustomerID,
    Customers.FirstName,
    Customers.LastName,
    Orders.OrderID,
    Orders.OrderDate,
    Orders.OrderStatus,
    Products.ProductName,
    OrderItems.Quantity,
    Products.Price,
    Payments.PaymentID,
    Payments.PaymentDate,
    Payments.Amount
FROM Customers
    -- Join Orders to Customers by CustomerID
    JOIN Orders ON Customers.CustomerID = Orders.CustomerID
    -- Join OrderItems to Orders by OrderID
    JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
    -- Join Products to OrderItems by ProductID
    JOIN Products ON OrderItems.ProductID = Products.ProductID
    -- Join Payments to Orders by OrderID
    JOIN Payments ON Orders.OrderID = Payments.OrderID
ORDER BY Orders.OrderDate DESC;
