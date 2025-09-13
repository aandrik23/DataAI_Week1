# DATA SCIENCE AND AI - WEEK 1
## Sales Transactions 
Hello to my first project for the Data Science and AI Piscine!

For this project we have a CSV file from the last year's sales transactions from an e-shop and we should :
    
    1. Detect and clean the missing values
    2. Normalize product names
    3. Standardise dates
    4. Remove dulicates
    5. Handle outliers

Now i have fixed this and here are the steps to run the project :

```
python3 data_cleaning_and_import.py
```
To run the code and make the new CSV file named cleaned_sales.csv.

```
psql -d eshop
```
To open PostgresSQL.

```
SELECT product_name, COUNT(*) AS num_sales
FROM sales
GROUP BY product_name
ORDER BY num_sales DESC;
```
To find the number of sales of each product.

```
SELECT product_name, SUM(quantity) AS total_quantity
FROM sales
GROUP BY product_name
ORDER BY total_quantity DESC;
```
To find the of pieces of each product.

```
SELECT product_name, SUM(total_price) AS total_revenue
FROM sales
GROUP BY product_name
ORDER BY total_revenue DESC;
```
The total per product.

```
SELECT transaction_date, COUNT(*) AS num_sales, SUM(total_price) AS daily_revenue
FROM sales
GROUP BY transaction_date
ORDER BY transaction_date;
```
The number of sales per day.

