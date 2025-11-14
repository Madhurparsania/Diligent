-- Comprehensive join to show customer, order, order item, product, and payment details
SELECT
    Customers.CustomerID,
    Customers.FirstName,
    Customers.LastName,
    Orders.OrderID,
    Orders.OrderDate,
    Orders.OrderStatus,
    Products.ProductName,
    OrderItems.Quantity,
    OrderItems.UnitPrice,
    OrderItems.Subtotal,
    Payments.PaymentID,
    Payments.PaymentDate,
    Payments.PaymentAmount,
    Payments.PaymentMethod,
    Payments.PaymentStatus
FROM Customers
    -- Each order is placed by a customer
    JOIN Orders ON Customers.CustomerID = Orders.CustomerID
    -- Each order has multiple order items
    JOIN OrderItems ON Orders.OrderID = OrderItems.OrderID
    -- Each order item is linked to a product
    JOIN Products ON OrderItems.ProductID = Products.ProductID
    -- Each payment is for one order
    JOIN Payments ON Orders.OrderID = Payments.OrderID
ORDER BY Orders.OrderDate DESC;

