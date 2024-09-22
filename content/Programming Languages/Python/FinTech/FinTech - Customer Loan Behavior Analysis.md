
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/customer_loan_behavior_analysis.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

### Description:  
You're a financial analyst at a leading digital lending platform. Your company provides personal loans to customers based on their creditworthiness. The business development team wants to analyze customer loan repayment behavior to inform their marketing strategies. They've asked you to prepare a dataset that combines customer information, loan details, and repayment history.  

### Tasks:  
- Calculate the total repayment amount made by the customer and merge this information with the loan details dataset. Ensure the resulting dataset includes all columns from the loan details dataset.  
- Group customers by age brackets (25-34, 35-44, 45-54, 55+) and calculate the average loan amount and average credit score for each age group.  
- Use the pivot_table method to reshape the repayment history dataset, showing:  
	- **Rows:** Months of repayment (January to December)  
	- **Columns:** Years of repayment (e.g., 2022, 2023)  
	- **Values:** Total repayment amount made in each month of each year

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

The dataset represents a digital lending platform's customer loan data, comprising three tables: customer information (demographics), loan details (loan amounts and issuance dates), and repayment history (repayment amounts and dates). The dataset includes 1,000 customers, 1,000 loans, and 5,000 repayment records, providing a comprehensive view of customer loan behavior.  

**customer_info.csv:** Contains customer demographic information.  
- customer_id (unique identifier)
- age
- income
- credit_score

**loan_details.csv:** Contains loan information.  
- loan_id (unique identifier)
- customer_id (foreign key referencing customer_info)
- loan_amount
- loan_issued_date  

**repayment_history.csv:** Contains repayment information.  
- repayment_id (unique identifier)
- loan_id (foreign key referencing loan_details)
- repayment_date
- repayment_amount

```python
# set the seed
np.random.seed(0)

# customer information
customer_info = pd.DataFrame({
    'customer_id': np.arange(1000),
    'age': np.random.randint(25, 60, 1000),
    'income': np.random.randint(50000, 150000, 1000),
    'credit_score': np.random.randint(600, 850, 1000)
})

# loan details
loan_details = pd.DataFrame({
    'loan_id': np.arange(1000),
    'customer_id': np.random.choice(customer_info['customer_id'], 1000),
    'loan_amount': np.random.randint(1000, 50000, 1000),
    'loan_issued_date': pd.date_range('2022-01-01', periods=1000, freq='D')
})

# repayment history
repayment_history = pd.DataFrame({
    'repayment_id': np.arange(5000),
    'loan_id': np.random.choice(loan_details['loan_id'], 5000),
    'repayment_date': pd.date_range('2022-01-01', periods=5000, freq='D'),
    'repayment_amount': np.random.randint(50, 500, 5000)
})

# save the datasets to CSV files
customer_info.to_csv('customer_info.csv', index=False)
loan_details.to_csv('loan_details.csv', index=False)
repayment_history.to_csv('repayment_history.csv', index=False)
```

Let us read into memory the csv files and take a look at the data types of each dataset.

```python
# create dataframes
customer_info_df = pd.read_csv('customer_info.csv')
loan_details_df = pd.read_csv('loan_details.csv')

# you can use the parse_dates parameter to specify that column "repayment_date" should be parsed as a date object.
repayment_history_df = pd.read_csv('repayment_history.csv', parse_dates=['repayment_date'])
```


```python
customer_info_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1000 entries, 0 to 999
    Data columns (total 4 columns):
     #   Column        Non-Null Count  Dtype
    ---  ------        --------------  -----
     0   customer_id   1000 non-null   int64
     1   age           1000 non-null   int64
     2   income        1000 non-null   int64
     3   credit_score  1000 non-null   int64
    dtypes: int64(4)
    memory usage: 31.4 KB
    

We will need to convert the column "loan_issue_date" to a date object.

```python
loan_details_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1000 entries, 0 to 999
    Data columns (total 4 columns):
     #   Column            Non-Null Count  Dtype 
    ---  ------            --------------  ----- 
     0   loan_id           1000 non-null   int64 
     1   customer_id       1000 non-null   int64 
     2   loan_amount       1000 non-null   int64 
     3   loan_issued_date  1000 non-null   object
    dtypes: int64(3), object(1)
    memory usage: 31.4+ KB
    


```python
repayment_history_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 5000 entries, 0 to 4999
    Data columns (total 4 columns):
     #   Column            Non-Null Count  Dtype         
    ---  ------            --------------  -----         
     0   repayment_id      5000 non-null   int64         
     1   loan_id           5000 non-null   int64         
     2   repayment_date    5000 non-null   datetime64[ns]
     3   repayment_amount  5000 non-null   int64         
    dtypes: datetime64[ns](1), int64(3)
    memory usage: 156.4 KB
    

# Task #1  

Calculate the total repayment amount made by the customer and merge this information with the loan details dataset. Ensure the resulting dataset includes all columns from the loan details dataset.

For this task, Let us merge all three datasets and then calculate the total repayment amount per customer. This is the dataframe we will use for the rest of the tutorial. 

```python
df = customer_info_df.merge(loan_details_df, on='customer_id').merge(repayment_history_df, on='loan_id')
df.head()
```

|     | customer_id | age | income | credit_score | loan_id | loan_amount | loan_issued_date | repayment_id | repayment_date | repayment_amount |
| --- | ----------- | --- | ------ | ------------ | ------- | ----------- | ---------------- | ------------ | -------------- | ---------------- |
| 0   | 0           | 25  | 141445 | 725          | 1       | 11142       | 2022-01-02       | 1710         | 2026-09-07     | 303              |
| 1   | 0           | 25  | 141445 | 725          | 840     | 25736       | 2024-04-20       | 527          | 2023-06-12     | 492              |
| 2   | 0           | 25  | 141445 | 725          | 840     | 25736       | 2024-04-20       | 589          | 2023-08-13     | 281              |
| 3   | 0           | 25  | 141445 | 725          | 840     | 25736       | 2024-04-20       | 1281         | 2025-07-05     | 99               |
| 4   | 0           | 25  | 141445 | 725          | 840     | 25736       | 2024-04-20       | 2831         | 2029-10-02     | 117              |


We can see from the data below that our new dataframe has 5,000 rows and we do not have any null values. Remember that by defaul the `.merge` method will do an inner merge. This means the columns we merged on (customer_id and loan_id) need to have matching values on both dataframes being merged. If the values do not match, that row will not make it to the final result.  

In this specific case, we did loose some of the data, for example:
- The customer_info_df has a customer_id=1
- Customer_id=1 is not present in the loan_details_df
- This means the final dataframe (df), does not contain customer_id=1

```python
# here is customer_id=1
mask = customer_info_df.loc[:,'customer_id'] == 1
customer_info_df[mask]
```

|     | customer_id | age | income | credit_score |
| --- | ----------- | --- | ------ | ------------ |
| 1   | 1           | 28  | 92694  | 692          |



```python
# customer_id=1 is not found in loan_details_df
mask = loan_details_df.loc[:,'customer_id'] == 1
loan_details_df[mask]
```

| loan_id | customer_id | loan_amount | loan_issued_date |
| ------- | ----------- | ----------- | ---------------- |



```python
# customer_id=1 is not found in df
mask = df.loc[:,'customer_id'] == 1
df[mask]
```

|customer_id|age|income|credit_score|loan_id|loan_amount|loan_issued_date|repayment_id|repayment_date|repayment_amount|
|---|---|---|---|---|---|---|---|---|---|




To calculate the total repayment amount per customer, we can make use of the `.groupby` method.

```python
# create group object
group = df.groupby('customer_id')

# get the total repayment amount for the group
group['repayment_amount'].sum()
```


    customer_id
    0      1663
    2      4450
    3       725
    4      2104
    5      2094
           ... 
    994     675
    995    2513
    996    1156
    997    1155
    998     442
    Name: repayment_amount, Length: 629, dtype: int64



If you wanted to verify the math is correct...  

We can find select one customer_id and manually add the values.  
- 303 + 492 + 281 + 99 + 117 + 371 = 1,663

```python
mask = df.loc[:,'customer_id'] == 0
df.loc[mask,'repayment_amount']
```

    0    303
    1    492
    2    281
    3     99
    4    117
    5    371
    Name: repayment_amount, dtype: int64


# Task #2  

Group customers by age brackets (25-34, 35-44, 45-54, 55+) and calculate the average loan amount and average credit score for each age group.  

- **bins** defines the edges of the bins.
- **labels** assigns names to each bin.
- **float('inf')** represents infinity, making the last bin open-ended (55+).
- **include_lowest=True** ensures that the lowest value (55) is included in the last bin.

```python
# create bins for the (25-34), (35-44), (45-54) and (55+) categories
bins = [25, 34, 44, 55, float('inf')]  
 
# labels for the three categories
labels = ['25-34', '35-44', '45-54', '55+'] 
 
# bin it up!
df['age_brackets'] = pd.cut(df['age'], bins=bins, labels=labels, include_lowest=True)
 
# here we get a frequency count of the categories
df['age_brackets'].value_counts()
```

    age_brackets
    25-34    1552
    35-44    1535
    45-54    1411
    55+       502
    Name: count, dtype: int64


The observed parameter in `df.groupby` affects grouping behavior when using Categorical columns, and setting it to True (future default) treats categories as part of the data's index, whereas setting it to False (current default) treats them as "unobserved" variables.  

I went in more detail in a previous tutorial: [Education-Analytics-Challenge](https://hedaro.com/Programming-Languages/Python/Data-Analyst/Data-Analyst---Education-Analytics-Challenge)

```python
# calculate the average loan amount and average credit score for each age group
df.groupby('age_brackets', observed=True).agg(
     avg_loan_amount=pd.NamedAgg(column="loan_amount", aggfunc="mean"),
     avg_credit_score=pd.NamedAgg(column="credit_score", aggfunc="mean")
)
```

|                  | avg_loan_amount | avg_credit_score |
| ---------------- | --------------- | ---------------- |
| **age_brackets** |                 |                  |
| **25-34**        | 25107.916237    | 715.453608       |
| **35-44**        | 25182.748534    | 725.331596       |
| **45-54**        | 25559.566265    | 725.663359       |
| **55+**          | 28249.966135    | 712.916335       |

# Task #3  

Use the pivot_table method to reshape the repayment history dataset, showing:  
- **Rows:** Months of repayment (January to December)  
- **Columns:** Years of repayment (e.g., 2022, 2023)  
- **Values:** Total repayment amount made in each month of each year 

In order to sort the months correctly, we need to use a map as shown below.

```python
month_order = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
               'May': 5, 'June': 6, 'July': 7, 'August': 8,
               'September': 9, 'October': 10, 'November': 11, 'December': 12}

repayment_pivot = repayment_history_df.pivot_table(values='repayment_amount', 
                                 index=repayment_history_df['repayment_date'].dt.strftime('%B'), 
                                 columns=repayment_history_df['repayment_date'].dt.year, aggfunc='sum')

repayment_pivot.sort_index(key=lambda x: x.map(month_order))
```

| repayment_date     | 2022   | 2023   | 2024   | 2025   | 2026   | 2027   | 2028   | 2029   | 2030   | 2031   | 2032    | 2033   | 2034   | 2035   |
| ------------------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------- | ------ | ------ | ------ |
| **repayment_date** |        |        |        |        |        |        |        |        |        |        |         |        |        |        |
| **January**        | 7876.0 | 8834.0 | 9711.0 | 8979.0 | 9236.0 | 8772.0 | 8576.0 | 8084.0 | 9712.0 | 8340.0 | 8167.0  | 7108.0 | 7630.0 | 8604.0 |
| **February**       | 7917.0 | 8264.0 | 8113.0 | 8181.0 | 7965.0 | 6685.0 | 7884.0 | 8308.0 | 8039.0 | 7589.0 | 7676.0  | 7565.0 | 8783.0 | 7098.0 |
| **March**          | 8090.0 | 8245.0 | 9570.0 | 9039.0 | 7522.0 | 8419.0 | 8936.0 | 7896.0 | 7604.0 | 7817.0 | 7499.0  | 8310.0 | 7289.0 | 8927.0 |
| **April**          | 7950.0 | 9636.0 | 8574.0 | 8980.0 | 9272.0 | 8009.0 | 8171.0 | 8437.0 | 7657.0 | 8692.0 | 8601.0  | 8754.0 | 8644.0 | 8464.0 |
| **May**            | 9821.0 | 8433.0 | 9034.0 | 8423.0 | 8261.0 | 8928.0 | 7685.0 | 9209.0 | 8665.0 | 8259.0 | 8926.0  | 8598.0 | 8573.0 | 9337.0 |
| **June**           | 7999.0 | 9103.0 | 7305.0 | 7271.0 | 9419.0 | 8276.0 | 7641.0 | 9278.0 | 8966.0 | 8488.0 | 8390.0  | 8898.0 | 8626.0 | 8272.0 |
| **July**           | 7786.0 | 9393.0 | 9565.0 | 8010.0 | 8378.0 | 9542.0 | 8496.0 | 8251.0 | 8633.0 | 8975.0 | 10388.0 | 7370.0 | 8617.0 | 8241.0 |
| **August**         | 7587.0 | 8239.0 | 8548.0 | 8866.0 | 8559.0 | 8532.0 | 8008.0 | 9171.0 | 8203.0 | 8873.0 | 7762.0  | 9981.0 | 7278.0 | 9633.0 |
| **September**      | 8666.0 | 8986.0 | 7753.0 | 8168.0 | 8277.0 | 8769.0 | 9079.0 | 8666.0 | 7734.0 | 7779.0 | 7864.0  | 9420.0 | 6240.0 | 2101.0 |
| **October**        | 9202.0 | 8138.0 | 7779.0 | 8989.0 | 7725.0 | 7485.0 | 9331.0 | 8433.0 | 9347.0 | 8671.0 | 9127.0  | 9622.0 | 9030.0 | NaN    |
| **November**       | 9295.0 | 8768.0 | 8246.0 | 8136.0 | 7776.0 | 8842.0 | 8161.0 | 8071.0 | 8535.0 | 8646.0 | 8221.0  | 7041.0 | 7790.0 | NaN    |
| **December**       | 8295.0 | 8646.0 | 7134.0 | 7425.0 | 8097.0 | 8750.0 | 9667.0 | 8965.0 | 8523.0 | 7022.0 | 8990.0  | 8686.0 | 7727.0 | NaN    |

# Summary:  

The Pandas tutorial provided a comprehensive guide to analyzing customer loan behavior using three datasets: customer information, loan details, and repayment history. The tutorial covered merging datasets, grouping data, calculating aggregates, and reshaping data using pivot tables.  

### Key Takeaways:  
- **Merging datasets:** Combine customer information, loan details, and repayment history datasets using the `merge` method.
- **Data grouping:** Group customers by age brackets using `pd.cut` and calculate average loan amounts and credit scores using `groupby` and `agg`.
- **Data aggregation:** Calculate total repayment amounts per customer using `groupby` and `sum`.
- **Pivot tables:** Reshape repayment history data using `pivot_table` to show monthly repayment amounts by year.
- **Data sorting:** Sort months correctly using a custom sorting map.
- **Data inspection:** Use `info` and `value_counts` to understand data distribution and quality.
