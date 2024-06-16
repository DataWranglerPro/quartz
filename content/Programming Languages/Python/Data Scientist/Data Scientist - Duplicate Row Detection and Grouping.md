
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/duplicate_row_detection_grouping.ipynb), offering an alternative platform for your learning convenience.
> - [Pandas Data Analysis Bundle](https://hedaro.gumroad.com/l/jVeRh): Take your skills to the next level with comprehensive Jupyter Notebook tutorials covering dates, group by, plotting, pivot tables, and more. Includes specialized tutorials for Excel and SQL developers, helping you master data analysis with Pandas.

### Description:

You are a data scientist working for an e-commerce company. The marketing team has collected customer data from various sources, including website interactions, social media, and customer surveys. However, due to the diverse sources, there are duplicate records in the dataset.

### Task:

Your task is to identify and combine duplicate rows based on specific criteria, and calculate the total spend for each unique customer.

- Identify duplicate rows based on CustomerID, Name, and Email.
- Combine duplicate rows into a single row, adding up the values in the Spent column.
- Calculate the total spend for each unique customer.

### Bonus Question:

- What is the average spend per customer for the top 3 customers with the highest total spend? (**Answer:** 700.00)

``` python
# import libraries
import pandas as pd
import numpy as np
```

# Generate the data

Here is a tiny dataset composed of 12 rows that represents customer information, including their ID, name, email, and amount spent.

### Columns:

``` data
CustomerID (string): unique customer identifier
Name (string): customer name
Email (string): customer email
Spent (integer): amount spent by the customer
```


``` python
# sample data placed in a dictionary
data = {
'CustomerID': ['C001', 'C002', 'C003', 'C001', 'C002', 'C004', 'C005', 'C003', 'C006'],
'Name': ['John', 'Mary', 'David', 'John', 'Mary', 'Emily', 'Michael', 'David', 'Sarah'],
'Email': ['john@example.com', 'mary@example.com', 'david@example.com', 'john@example.com', 'mary@example.com', 'emily@example.com', 'michael@example.com', 'david@example.com', 'sarah@example.com'],
'Spent': [100, 200, 300, 100, 200, 400, 500, 300, 600]
}

# create the dataframe
df = pd.DataFrame(data)

# introduce duplicates
duplicates = pd.DataFrame({'CustomerID': ['C001', 'C002', 'C003'], 'Name': ['John', 'Mary', 'David'], 'Email': ['john@example.com', 'mary@example.com', 'david@example.com'], 'Spent': [100, 200, 300]})

# combine the dataframes
df = pd.concat([df, duplicates], ignore_index=True)
  
df
```

|     | CustomerID | Name    | Email               | Spent |
| --- | ---------- | ------- | ------------------- | ----- |
| 0   | C001       | John    | `john@example.com`  | 100   |
| 1   | C002       | Mary    | `mary@example.com`    | 200   |
| 2   | C003       | David   | `david@example.com`   | 300   |
| 3   | C001       | John    | `john@example.com`    | 100   |
| 4   | C002       | Mary    | `mary@example.com`    | 200   |
| 5   | C004       | Emily   | `emily@example.com`   | 400   |
| 6   | C005       | Michael | `michael@example.com` | 500   |
| 7   | C003       | David   | `david@example.com`   | 300   |
| 8   | C006       | Sarah   | `sarah@example.com`   | 600   |
| 9   | C001       | John    | `john@example.com`    | 100   |
| 10  | C002       | Mary    | `mary@example.com`    | 200   |
| 11  | C003       | David   | `david@example.com`   | 300   |

# Identify Duplicates

``` python
df[df.duplicated()].sort_values(by='CustomerID')

# Intentionally not removing duplicates, as they represent additional payments from the same customer
```

|     | CustomerID | Name  | Email             | Spent |
| --- | ---------- | ----- | ----------------- | ----- |
| 3   | C001       | John  | `john@example.com`  | 100   |
| 9   | C001       | John  | `john@example.com`  | 100   |
| 4   | C002       | Mary  | `mary@example.com`  | 200   |
| 10  | C002       | Mary  | `mary@example.com`  | 200   |
| 7   | C003       | David | `david@example.com` | 300   |
| 11  | C003       | David | `david@example.com` | 300   |

# Total Spent per Customer

I probably would have removed the duplicate rows. In this example, we are treating the duplicates as additional payments received from the customer. Remember, we are collecting data from various sources.

``` python
group = df.groupby(['CustomerID','Name','Email'])

# calculate the sum
group.sum()
```

|            |         |                     | Spent |
| ---------- | ------- | ------------------- | ----- |
| CustomerID | Name    | Email               |       |
| C001       | John    | `john@example.com`    | 300   |
| C002       | Mary    | `mary@example.com`    | 600   |
| C003       | David   | `david@example.com`   | 900   |
| C004       | Emily   | `emily@example.com`   | 400   |
| C005       | Michael | `michael@example.com` | 500   |
| C006       | Sarah   | `sarah@example.com`   | 600   |

# Can You Solve the Bonus Question?

- What is the average spend per customer for the top 3 customers with the highest total spend? (**Answer:** 700.00)