# Part 1: W3Schools SQL Lab

*Introductory level SQL*

--

This challenge uses the [W3Schools SQL playground](http://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all). Please add solutions to this markdown file and submit.

1. Which customers are from the UK?
```
Around the Horn
B's Beverages
Consolidated Holdings
Eastern Connection
Island Trading
North/South
Seven Seas Imports
```

```sql
SELECT CustomerName FROM Customers WHERE Country = 'UK';
```

2. What is the name of the customer who has the most orders?

```
CustomerName	Orders
Ernst Handel	10
```

```sql
SELECT CustomerName, MAX(temp.Count) AS Orders
	FROM (SELECT CustomerID, COUNT(*) AS Count FROM Orders GROUP BY CustomerID) temp
JOIN Customers ON temp.CustomerID = Customers.CustomerID
```

3. Which supplier has the highest average product price?
```
SupplierName	            Price
Aux joyeux ecclésiastiques	140.75
```

```sql
SELECT SupplierName, MAX(temp.Avg_Price) AS Price
	FROM (SELECT SupplieriD, AVG(Price) AS Avg_Price FROM Products GROUP BY SupplierID) temp
JOIN Suppliers ON temp.SupplierID = Suppliers.SupplierID
```

4. How many different countries are all the customers from? (*Hint:* consider [DISTINCT](http://www.w3schools.com/sql/sql_distinct.asp).)
```
21
```
```sql
SELECT COUNT(DISTINCT(Country)) FROM Customers
```

5. What category appears in the most orders?
```
CategoryName	max_orders
Dairy Products	100
```
```sql
SELECT Categories.CategoryName, MAX(temp.Num_Orders) as max_orders
FROM
	(SELECT Products.CategoryID, COUNT(OrderID) as Num_Orders
      FROM OrderDetails
      JOIN Products ON Products.ProductID = OrderDetails.ProductID
      GROUP BY CategoryID) temp
JOIN Categories ON temp.CategoryID = Categories.CategoryID
```

6. What was the total cost for each order?
```
Number of Records: 196
OrderID	TotalCost
10248	566
10249	2329.25
10250	2267.25
...
```
```sql
SELECT OrderID, SUM(Products.Price * OrderDetails.Quantity) as TotalCost
FROM OrderDetails
JOIN Products ON OrderDetails.ProductID = Products.ProductID
GROUP BY OrderID
```

7. Which employee made the most sales (by total price)?
```
FirstName	LastName	MaxSale
Steven	    Buchanan	15353.6
```
```sql
SELECT FirstName, LastName , MAX(temp.TotalCost) AS MaxSale
FROM
  (SELECT OrderID, SUM(Products.Price * OrderDetails.Quantity) as TotalCost
  FROM OrderDetails
  JOIN Products ON OrderDetails.ProductID = Products.ProductID
  GROUP BY OrderID) temp
JOIN Orders ON temp.OrderID = Orders.OrderID
JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
```

8. Which employees have BS degrees? (*Hint:* look at the [LIKE](http://www.w3schools.com/sql/sql_like.asp) operator.)
```
LastName	FirstName
Leverling	Janet
Buchanan	Steven
```
```sql
SELECT LastName, FirstName
FROM Employees
WHERE Notes LIKE '%BS%'
```

9. Which supplier of three or more products has the highest average product price? (*Hint:* look at the [HAVING](http://www.w3schools.com/sql/sql_having.asp) operator.)

```
SupplierName	                    AvgPrice
Plutzer Lebensmittelgroßmärkte AG	44.68
```
```sql
SELECT SupplierName, ROUND(MAX(temp.AvgPrice),2) AS AvgPrice
FROM
  (SELECT SupplierID, AVG(Price) AS AvgPrice
  FROM Products
  GROUP BY SupplierID
  HAVING COUNT(ProductID) > 3) temp
JOIN Suppliers ON temp.SupplierID = Suppliers.SupplierID
```
