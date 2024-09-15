
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/digital_wallet.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

### Description:  
You're a fintech professional working for a digital wallet company. Your company has partnered with several merchants to offer exclusive discounts to customers. However, the data team has been struggling to consolidate the discount offers and customer transactions efficiently. The current process involves manually merging and transforming data from different sources, leading to errors and delays. Your task is to develop a robust Pandas solution to streamline the data processing pipeline.

### Tasks:
- **Data Merging:** Merge two datasets, discount_offers and customer_transactions, based on the merchant_id column. Ensure the merged dataset retains all columns from both tables.
- **Data Transformation:** Convert the discount_start_date and discount_end_date columns from string format (YYYY-MM-DD) to datetime format. Then, calculate the duration of each discount offer in days.
- **Data Reshaping:** Pivot the merged dataset to create a new table with merchant_id as the index, discount_type as columns, and the corresponding discount_duration values.

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

**Discount Offers Dataset:** This dataset contains information about exclusive discounts offered by various merchants, including the type of discount, start and end dates, and the associated merchant ID. It has 1000 rows and 4 columns.  

**Customer Transactions Dataset:** This dataset contains transactional data for customers, including the merchant ID, customer ID, transaction date, and transaction amount, with 5000 rows and 4 columns, representing purchases made by customers at different merchants.  

### Columns:  

The **discount_offers** dataset contains 1000 rows and 4 columns:
- **merchant_id (int):** Unique identifier for each merchant
- **discount_type (str):** Type of discount offered (percentage or fixed)
- **discount_start_date (str):** Start date of the discount offer (YYYY-MM-DD)
- **discount_end_date (str):** End date of the discount offer (YYYY-MM-DD)

The **customer_transactions** dataset contains 5000 rows and 4 columns:
- **merchant_id (int):** Unique identifier for each merchant
- **customer_id (int):** Unique identifier for each customer
- **transaction_date (str):** Date of the transaction (YYYY-MM-DD)
- **transaction_amount (float):** Amount of the transaction

```python
# set the seed
np.random.seed(0)

# generate discount_offers dataset
discount_offers = pd.DataFrame({
    'merchant_id': np.random.randint(1, 100, size=1000),
    'discount_type': np.random.choice(['percentage', 'fixed'], size=1000),
    'discount_start_date': pd.date_range('2022-01-01', periods=1000).strftime('%Y-%m-%d'),
    'discount_end_date': pd.date_range('2022-01-15', periods=1000).strftime('%Y-%m-%d')
})

# generate customer_transactions dataset
customer_transactions = pd.DataFrame({
    'merchant_id': np.random.randint(1, 100, size=5000),
    'customer_id': np.random.randint(1, 1000, size=5000),
    'transaction_date': pd.date_range('2022-01-01', periods=5000).strftime('%Y-%m-%d'),
    'transaction_amount': np.random.uniform(10, 100, size=5000)
})
```

Let us take a look at the data types.

The date columns on both dataframes are not of type datetime, we will need to fix this as we work through the tasks.

```python
discount_offers.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1000 entries, 0 to 999
    Data columns (total 4 columns):
     #   Column               Non-Null Count  Dtype 
    ---  ------               --------------  ----- 
     0   merchant_id          1000 non-null   int32 
     1   discount_type        1000 non-null   object
     2   discount_start_date  1000 non-null   object
     3   discount_end_date    1000 non-null   object
    dtypes: int32(1), object(3)
    memory usage: 27.5+ KB
    


```python
customer_transactions.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 5000 entries, 0 to 4999
    Data columns (total 4 columns):
     #   Column              Non-Null Count  Dtype  
    ---  ------              --------------  -----  
     0   merchant_id         5000 non-null   int32  
     1   customer_id         5000 non-null   int32  
     2   transaction_date    5000 non-null   object 
     3   transaction_amount  5000 non-null   float64
    dtypes: float64(1), int32(2), object(1)
    memory usage: 117.3+ KB
    

# Data Merging  

Merge two datasets, discount_offers and customer_transactions, based on the merchant_id column. Ensure the merged dataset retains all columns from both tables.

```python
merged_df = customer_transactions.merge(discount_offers, on='merchant_id')
merged_df.head()
```

|     | merchant_id | customer_id | transaction_date | transaction_amount | discount_type | discount_start_date | discount_end_date |
| --- | ----------- | ----------- | ---------------- | ------------------ | ------------- | ------------------- | ----------------- |
| 0   | 16          | 572         | 2022-01-01       | 30.199690          | fixed         | 2022-03-31          | 2022-04-14        |
| 1   | 16          | 572         | 2022-01-01       | 30.199690          | fixed         | 2023-08-24          | 2023-09-07        |
| 2   | 16          | 572         | 2022-01-01       | 30.199690          | fixed         | 2024-03-14          | 2024-03-28        |
| 3   | 16          | 572         | 2022-01-01       | 30.199690          | percentage    | 2024-04-25          | 2024-05-09        |
| 4   | 5           | 677         | 2022-01-02       | 97.575916          | percentage    | 2022-03-03          | 2022-03-17        |


# Data Transformation

Convert the discount_start_date and discount_end_date columns from string format (YYYY-MM-DD) to datetime format. Then, calculate the duration of each discount offer in days.

```python
# convert to date object
merged_df['discount_start_date'] = pd.to_datetime(merged_df['discount_start_date'])
merged_df['discount_end_date'] = pd.to_datetime(merged_df['discount_end_date'])

merged_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 50980 entries, 0 to 50979
    Data columns (total 7 columns):
     #   Column               Non-Null Count  Dtype         
    ---  ------               --------------  -----         
     0   merchant_id          50980 non-null  int32         
     1   customer_id          50980 non-null  int32         
     2   transaction_date     50980 non-null  object        
     3   transaction_amount   50980 non-null  float64       
     4   discount_type        50980 non-null  object        
     5   discount_start_date  50980 non-null  datetime64[ns]
     6   discount_end_date    50980 non-null  datetime64[ns]
    dtypes: datetime64[ns](2), float64(1), int32(2), object(2)
    memory usage: 2.3+ MB
    

Now that we have converted our dates into date objects, let's do some date math and calculate delta between the date columns.

**Note:** I was able to access to access the days via `.dt.days`

```python
merged_df['discount_duration'] = (merged_df['discount_end_date'] - merged_df['discount_start_date']).dt.days
merged_df.head()
```

|     | merchant_id | customer_id | transaction_date | transaction_amount | discount_type | discount_start_date | discount_end_date | discount_duration |
| --- | ----------- | ----------- | ---------------- | ------------------ | ------------- | ------------------- | ----------------- | ----------------- |
| 0   | 16          | 572         | 2022-01-01       | 30.199690          | fixed         | 2022-03-31          | 2022-04-14        | 14                |
| 1   | 16          | 572         | 2022-01-01       | 30.199690          | fixed         | 2023-08-24          | 2023-09-07        | 14                |
| 2   | 16          | 572         | 2022-01-01       | 30.199690          | fixed         | 2024-03-14          | 2024-03-28        | 14                |
| 3   | 16          | 572         | 2022-01-01       | 30.199690          | percentage    | 2024-04-25          | 2024-05-09        | 14                |
| 4   | 5           | 677         | 2022-01-02       | 97.575916          | percentage    | 2022-03-03          | 2022-03-17        | 14                |


# Data Reshaping

Pivot the merged dataset to create a new table with merchant_id as the index, discount_type as columns, and the corresponding discount_duration values.

```python
# create pivot table
new_df = merged_df.pivot_table(index='merchant_id', columns='discount_type', values='discount_duration')
new_df.head()
```

| discount_type   | fixed | percentage |
| --------------- | ----- | ---------- |
| **merchant_id** |       |            |
| **1**               | 14.0  | 14.0       |
| **2**               | 14.0  | 14.0       |
| **3**               | 14.0  | 14.0       |
| **4**               | 14.0  | 14.0       |
| **5**               | 14.0  | 14.0       |


Here are a few key points to note about the results from the pivot table we just created.

- **The fixed and percentage columns all have the same value of 14.0:**

When we created the synthetic data, here is the code we used:  
    `'discount_start_date': pd.date_range('2022-01-01', periods=1000).strftime('%Y-%m-%d')`  
    `'discount_end_date': pd.date_range('2022-01-15', periods=1000).strftime('%Y-%m-%d')`  

As you can see we have 14 days between the start and end dates. This is the reason we are seeing all of the rows with the same value of fourteen.

- **We are calculating the mean on the "discount_duration" column:**

From the pandas documentation:    
"If aggfunc is None (default), the aggregation function will default to mean for numeric data, and first for object data (strings).  

This means the average is being calculated on the results, but since they are all equal to 14, we really don't notice. I just wanted to point it out so you realize this is happening in the background and that this aggregate function can be changed if needed."

# Summary:  
The tutorial demonstrated how to use Pandas to streamline a data processing pipeline for a digital wallet company. It involved merging two datasets (discount offers and customer transactions), transforming the data by converting date columns to datetime format and calculating the duration of discount offers, and reshaping the data using a pivot table.  

### Key Takeaways:  
- Merged two datasets (discount_offers and customer_transactions) based on the merchant_id column using `customer_transactions.merge(discount_offers, on='merchant_id')`.
- Converted date columns (discount_start_date and discount_end_date) from string format to datetime format using `pd.to_datetime()`.
- Calculated the duration of discount offers in days using `(merged_df['discount_end_date'] - merged_df['discount_start_date']).dt.days`.
- Created a pivot table with merchant_id as the index, discount_type as columns, and discount_duration values using `merged_df.pivot_table()`.
- Understood that the pivot table calculates the mean of discount_duration values by default, which can be changed if needed.
- Recognized that the synthetic data generated for the tutorial resulted in a consistent 14-day duration for all discount offers, leading to identical values in the pivot table.
