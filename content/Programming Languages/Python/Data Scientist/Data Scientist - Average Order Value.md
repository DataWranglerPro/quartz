
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/Average_order_value.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

### Description:

You are a data scientist at an e-commerce company. You have two datasets: orders and products. Your task is to merge these datasets and calculate the average order value for each region.

### Task:

- Merge the orders and products datasets on the ProductID column.
- Calculate the total order value for each order by summing the product prices.
- Calculate the average order value for each region.

### Bonus Question:

- What is the average order value only including products with a price greater than $8.00? **Answer:** $25.64

``` python
# import libraries
import pandas as pd
import numpy as np
import sys

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
print('Numpy version ' + np.__version__)
```

``` output
Python version 3.11.7 | packaged by Anaconda, Inc. | (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
Pandas version 2.2.1
Numpy version 1.26.4
```

### The Data

The **orders** table contains information about each order, such as the region it was made in and the customer who made it, while the **products** table contains information about each product, including its price and the order it was part of. The two tables are linked by the ProductID column, which allows you to match products to the orders they were part of.

##### Orders:

- OrderID (int): Unique identifier for each order
- Region (str): Geographic region where the order was made (e.g. North, South, East, West)
- CustomerID (int): Unique identifier for each customer
- OrderDate (str): Date the order was made (in YYYY-MM-DD format)
- ProductID (int): Foreign key referencing the ProductID in the Products table

##### Products:
- ProductID (int): Unique identifier for each product
- ProductPrice (float): Price of each product

``` python
orders = pd.DataFrame({
'OrderID': [3, 3, 3, 5, 5],
'Region': ['North', 'South', 'East', 'West', 'North'],
'CustomerID': [1, 2, 3, 4, 5],
'ProductID': [1, 1, 2, 3, 4],
'OrderDate': ['2022-01-01', '2022-01-15', '2022-02-01', '2022-03-01', '2022-04-01']
})

orders.head()
```

|     | OrderID | Region | CustomerID | ProductID | OrderDate  |
| --- | ------- | ------ | ---------- | --------- | ---------- |
| 0   | 3       | North  | 1          | 1         | 2022-01-01 |
| 1   | 3       | South  | 2          | 1         | 2022-01-15 |
| 2   | 3       | East   | 3          | 2         | 2022-02-01 |
| 3   | 5       | West   | 4          | 3         | 2022-03-01 |
| 4   | 5       | North  | 5          | 4         | 2022-04-01 |

``` python
# make sure the datatypes look good
orders.info()
```

``` output
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5 entries, 0 to 4
Data columns (total 5 columns):
 #   Column      Non-Null Count  Dtype 
---  ------      --------------  ----- 
 0   OrderID     5 non-null      int64 
 1   Region      5 non-null      object
 2   CustomerID  5 non-null      int64 
 3   ProductID   5 non-null      int64 
 4   OrderDate   5 non-null      object
dtypes: int64(3), object(2)
memory usage: 332.0+ bytes
```

I want to convert the date column from string to datetime. We want our dates to be date objects and not treated as strings.

``` python
orders['OrderDate'] = pd.to_datetime(orders['OrderDate'] )

orders.info()
```

``` output
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5 entries, 0 to 4
Data columns (total 5 columns):
 #   Column      Non-Null Count  Dtype         
---  ------      --------------  -----         
 0   OrderID     5 non-null      int64         
 1   Region      5 non-null      object        
 2   CustomerID  5 non-null      int64         
 3   ProductID   5 non-null      int64         
 4   OrderDate   5 non-null      datetime64[ns]
dtypes: datetime64[ns](1), int64(3), object(1)
memory usage: 332.0+ bytes
```

``` python
products = pd.DataFrame({
'ProductID': [1, 2, 3, 4, 5],
'ProductPrice': [10.99, 5.99, 7.99, 12.99, 8.99]
})

products.head()
```

|     | ProductID | ProductPrice |
| --- | --------- | ------------ |
| 0   | 1         | 10.99        |
| 1   | 2         | 5.99         |
| 2   | 3         | 7.99         |
| 3   | 4         | 12.99        |
| 4   | 5         | 8.99         |

``` python
# make sure datatypes look ok

products.info()
```

``` output
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5 entries, 0 to 4
Data columns (total 2 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   ProductID     5 non-null      int64  
 1   ProductPrice  5 non-null      float64
dtypes: float64(1), int64(1)
memory usage: 212.0 bytes
```

### Merge the two dataframes

Thanks to the common column named ProductID, merging the dataframes is a simple task.

``` python
# Merge the orders and products datasets on the ProductID column.
df = orders.merge(products, on='ProductID')

df
```

|     | OrderID | Region | CustomerID | ProductID | OrderDate  | ProductPrice |
| --- | ------- | ------ | ---------- | --------- | ---------- | ------------ |
| 0   | 3       | North  | 1          | 1         | 2022-01-01 | 10.99        |
| 1   | 3       | South  | 2          | 1         | 2022-01-15 | 10.99        |
| 2   | 3       | East   | 3          | 2         | 2022-02-01 | 5.99         |
| 3   | 5       | West   | 4          | 3         | 2022-03-01 | 7.99         |
| 4   | 5       | North  | 5          | 4         | 2022-04-01 | 12.99        |

**Calculate the total order value for each order by summing the product prices.**

I started by creating a basic group object and then getting the sum of the **ProductPrice** column. I then realized I needed to get these two numbers back into the original dataframe.

> I immediately thought about using transform, but to be honest, my mind is drawing a blank this morning...

``` python
# create group object
group = df.groupby('OrderID')

# get order value for group
group['ProductPrice'].sum(numeric_only=True)
```

``` output
OrderID
3    27.97
5    20.98
Name: ProductPrice, dtype: float64
```

Ok, let's start by converting the series into a proper dataframe.

``` python
agg = pd.DataFrame(group['ProductPrice'].sum(numeric_only=True)).reset_index()

agg
```

|     | OrderID | ProductPrice |
| --- | ------- | ------------ |
| 0   | 3       | 27.97        |
| 1   | 5       | 20.98        |

Since we are going to be merging the new **agg** dataframe, we should probably rename the ProductPrice column to something else so it doesn't clash with the other dataframe.

Since this column represents the total order value, that is what we should call it.

``` python
# rename columns

agg.columns = ['OrderID', 'TotalOrderValue']
```

Now we could have stopped after we calculated the sum on the group. We did get the total order value for each OrderID (27.50 for OderID 3 and 20.98 for OrderID 5). At the same time my mind said, how do we then add this information back to the original dataframe?

``` python
df.merge(agg, on='OrderID')
```

|     | OrderID | Region | CustomerID | ProductID | OrderDate  | ProductPrice | TotalOrderValue |
| --- | ------- | ------ | ---------- | --------- | ---------- | ------------ | --------------- |
| 0   | 3       | North  | 1          | 1         | 2022-01-01 | 10.99        | 27.97           |
| 1   | 3       | South  | 2          | 1         | 2022-01-15 | 10.99        | 27.97           |
| 2   | 3       | East   | 3          | 2         | 2022-02-01 | 5.99         | 27.97           |
| 3   | 5       | West   | 4          | 3         | 2022-03-01 | 7.99         | 20.98           |
| 4   | 5       | North  | 5          | 4         | 2022-04-01 | 12.99        | 20.98           |

### Can you solve the BONUS question?

- What is the average order value only including products with a price greater than $8.00? **Answer:** $25.64