
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/repayment_mystery.ipynb), offering an alternative platform for your learning convenience.
> - [Pandas Ninja](https://hedaro.gumroad.com/l/jVeRh): Take your skills to the next level with comprehensive Jupyter Notebook tutorials covering dates, group by, plotting, pivot tables, and more. Includes specialized tutorials for Excel and SQL developers, helping you master data analysis with Pandas.

### Description:  
Imagine you're a Data Analyst at a bank, and your manager just dropped a bombshell on you. It seems that the bank's financial reports are a mess, and they need your expertise to sort it out. The problem is that the data is scattered across multiple files, with different formats and inconsistencies. Your task is to use your Pandas skills to wrangle the data, identify the issues, and provide insights to help the bank get back on track.  

### Tasks:  
- **Data Unification:** Combine the 'transactions.csv' and 'customers.xlsx' files into a single dataframe, handling missing values and data type inconsistencies. Ensure that the 'customer_id' column is of numeric type (int or float) and the 'date' column is in datetime format.

- **Transaction Categorization:** Create a new column 'transaction_category' and categorize each transaction as either 'deposit', 'withdrawal', or 'transfer' based on the 'transaction_type' column. Calculate the total value and average amount for each transaction category.

- **Customer Insights:** Group by 'gender' and 'location', and calculate the average account balance (sum of 'amount' column) and transaction frequency (count of transactions) for each group. Output the results as a new dataframe.

```python
# import libraries
import pandas as pd
import numpy as np
import sys

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
print('Numpy version ' + np.__version__)
```

    Python version 3.11.7 | packaged by Anaconda, Inc. | (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
    Pandas version 2.2.1
    Numpy version 1.26.4
    

# The Data  

The dataset contains financial transaction records for 1,000 bank customers, including 10,000 transactions (deposits, withdrawals, and transfers) across two files (transactions.csv and customers.xlsx), with demographic information about each customer, such as age, gender, and location.

### Summary of Data:  

#### Transactions:  
- **customer_id (int):** unique customer identifier  
- **transaction_type (str):** type of transaction (deposit, withdrawal, transfer)  
- **amount (float):** transaction amount  
- **date (datetime):** transaction date     

#### Customers:  
- **customer_id (int):** unique customer identifier  
- **age (int):** customer age  
- **gender (str):** customer gender  
- **location (str):** customer location (urban/rural)

```python
# set the seed
np.random.seed(0)

transactions = pd.DataFrame({
    'customer_id': np.random.randint(1, 1000, 10000),
    'transaction_type': np.random.choice(['deposit', 'withdrawal', 'transfer'], 10000),
    'amount': np.random.uniform(100, 1000, 10000),
    'date': pd.date_range('2024-01-01', periods=10000)
})

# select 100 unique customer IDs
missing_ids = np.random.choice(transactions['customer_id'].unique(), 100, replace=False)

# for each of the selected customer IDs, set a random 'amount' value to null
for customer_id in missing_ids:
    idx = np.random.choice(transactions[transactions['customer_id'] == customer_id].index)
    transactions.loc[idx, 'amount'] = np.nan

customers = pd.DataFrame({
    'customer_id': np.arange(1, 1001),
    'age': np.random.randint(25, 65, 1000),
    'gender': np.random.choice(['male', 'female'], 1000),
    'location': np.random.choice(['urban', 'rural'], 1000)
})

# save data to disc
transactions.to_csv('transactions.csv', index=False)
customers.to_excel('customers.xlsx', index=False)
```

# Data Unification:  

- Combine the 'transactions.csv' and 'customers.xlsx' files into a single dataframe, handling missing values and data type inconsistencies.
- Ensure the 'customer_id' column is of numeric type (int or float) and the 'date' column is in datetime format.

Let us start by reading in the CSV and Excel file. We will then look at their data types to ensure they are correct.

```python
transactions_df = pd.read_csv('transactions.csv')
transactions_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 10000 entries, 0 to 9999
    Data columns (total 4 columns):
     #   Column            Non-Null Count  Dtype  
    ---  ------            --------------  -----  
     0   customer_id       10000 non-null  int64  
     1   transaction_type  10000 non-null  object 
     2   amount            9900 non-null   float64
     3   date              10000 non-null  object 
    dtypes: float64(1), int64(1), object(2)
    memory usage: 312.6+ KB
    

From the table above, we can see we need to update the `date` column so it is represented as a date object. Currently it is represented as a string object.  

The easiest way is to use the `pd.to_datetime` method.

```python
transactions_df['date'] = pd.to_datetime(transactions_df['date'])
transactions_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 10000 entries, 0 to 9999
    Data columns (total 4 columns):
     #   Column            Non-Null Count  Dtype         
    ---  ------            --------------  -----         
     0   customer_id       10000 non-null  int64         
     1   transaction_type  10000 non-null  object        
     2   amount            9900 non-null   float64       
     3   date              10000 non-null  datetime64[ns]
    dtypes: datetime64[ns](1), float64(1), int64(1), object(1)
    memory usage: 312.6+ KB
    

Let us now import the Excel file and perform the same process as we did with the CSV import.  

I am not seeing any issues with the datatypes after importing from Excel. Yay!

```python
customers_df = pd.read_excel('customers.xlsx')
customers_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1000 entries, 0 to 999
    Data columns (total 4 columns):
     #   Column       Non-Null Count  Dtype 
    ---  ------       --------------  ----- 
     0   customer_id  1000 non-null   int64 
     1   age          1000 non-null   int64 
     2   gender       1000 non-null   object
     3   location     1000 non-null   object
    dtypes: int64(2), object(2)
    memory usage: 31.4+ KB
    

Now we can try to merge the dataframes. The common key between them is `customer_id` and we will use the `.merge()` method to accomplish this portion of the task.

```python
df = pd.merge(transactions_df, customers_df, on='customer_id')
df.head()
```

|     | customer_id | transaction_type | amount     | date       | age | gender | location |
| --- | ----------- | ---------------- | ---------- | ---------- | --- | ------ | -------- |
| 0   | 685         | withdrawal       | 189.852038 | 2024-01-01 | 37  | female | rural    |
| 1   | 560         | withdrawal       | 626.720139 | 2024-01-02 | 36  | male   | urban    |
| 2   | 630         | withdrawal       | 657.841588 | 2024-01-03 | 28  | male   | rural    |
| 3   | 193         | deposit          | 327.129016 | 2024-01-04 | 48  | male   | rural    |
| 4   | 836         | transfer         | 798.239145 | 2024-01-05 | 41  | male   | urban    |


# Transaction Categorization:  

Using the 'transaction_type' column, calculate the total value and average amount for each transaction category.  

The transaction_type column contains the strings 'deposit', 'withdrawal', and 'transfer'. Since we are looking for total values in addition to the averages of these three categories, let us see if a pivot table would work for this task.  

**Notes on the `df.pivot_table`:**  
- By default the pivot table will calcuate the mean of `values`
- To change the aggregate function you need to add the parameter, i.e. aggfunc='sum'
- To get a different perspective: replace `index` with `columns`

```python
df.pivot_table(index=['transaction_type'], values=['amount'], aggfunc=['sum','mean'])
```
  
|                      | sum          | mean       |
| -------------------- | ------------ | ---------- |
|                      | **amount**   | **amount** |
| **transaction_type** |              |            |
| **deposit**          | 1.794246e+06 | 547.694277 |
| **transfer**         | 1.843336e+06 | 548.611931 |
| **withdrawal**       | 1.785630e+06 | 547.067914 |

# Customer Insights:  

Group by 'gender' and 'location', and calculate the average account balance (sum of 'amount' column) and transaction frequency (count of transactions) for each group. Output the results as a new dataframe.

The `agg()` method gives us a really nice API to work with. We not only can use multiple aggregate functions, but Pandas allows us to choose and name the column. 

```python
# create group object
group = df.groupby(['gender','location'])

# get the total and average of the group
group.agg(
     amount_sum=pd.NamedAgg(column="amount", aggfunc="sum"),
     amount_count=pd.NamedAgg(column="amount", aggfunc="count")
)
```

|            |              | amount_sum   | amount_count |
| ---------- | ------------ | ------------ | ------------ |
| **gender** | **location** |              |              |
| **female** | **rural**    | 1.447087e+06 | 2620         |
|            | **urban**    | 1.280509e+06 | 2298         |
| **male**   | **rural**    | 1.312961e+06 | 2419         |
|            | **urban**    | 1.382655e+06 | 2563         |

# Summary  
In this tutorial, you have completed three tasks and learned valuable skills along the way. You unified data by combining multiple files into a single DataFrame, categorized transactions to calculate totals and averages, and gained customer insights by grouping data by gender and location. Through these tasks, you have learned how to work with Pandas, including saving and loading data, checking and converting data types, merging DataFrames, using pivot tables, and grouping data to calculate aggregate values.

# Key Takeaways  
Here are the important skills you learned in this tutorial:
- How to create DataFrames from dictionaries and save them to CSV and Excel files  
- How to read CSV and Excel files into DataFrames  
- How to check the data types of a DataFrame's columns  
- How to convert data types (e.g., converting a column to datetime format)  
- How to merge DataFrames based on a common column (e.g., customer_id)  
- How to use pivot tables to calculate aggregate values (e.g., sum and mean) for transaction categories  
- How to group data by multiple columns (e.g., gender and location) and calculate aggregate values (e.g., sum and mean) for each group.
