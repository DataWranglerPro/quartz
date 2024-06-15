
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/How_to_Create_Basic_Pandas_Visualizations.ipynb), offering an alternative platform for your learning convenience.
> - [Pandas Data Analysis Bundle](https://hedaro.gumroad.com/l/jVeRh): Take your skills to the next level with comprehensive Jupyter Notebook tutorials covering dates, group by, plotting, pivot tables, and more. Includes specialized tutorials for Excel and SQL developers, helping you master data analysis with Pandas.

### Description:

You are a fintech professional working for a bank. Your team has collected a dataset of credit card transactions from various customers, including transaction dates, amounts, categories, and merchant names. However, the data is messy and needs to be cleaned and analyzed to extract valuable insights.

### Task:

Use pandas to clean and analyze the dataset, answering the following questions:

- What is the total transaction amount for each category (e.g., Food, Entertainment, Shopping)?
- Which merchant has the highest total transaction amount?
- What is the average transaction amount per day for each category?

### Bonus Question:

Identify the top 3 categories with the highest average transaction amount on weekends (Saturday and Sunday).

**Answer:** Travel, Entertainment, Food (in that order)

``` python
# import libraries
import pandas as pd
import numpy as np
```

# Generate the data

The code below generates a sample dataset with 105 rows and 4 columns (date, amount, category, and merchant). The data includes some missing values and duplicates to simulate real data in the wild.

``` python
# set the seed
np.random.seed(0)

# hold the values to randomly pick from
categories = ['Food', 'Entertainment', 'Shopping', 'Travel']
merchants = ['McDonalds', 'Amazon', 'Netflix', 'Expedia', 'Starbucks']
dates = pd.date_range('2024-01-01', '2024-01-31')

# generate the data
data = {
'date': np.random.choice(dates, size=100),
'amount': np.random.uniform(10, 100, size=100),
'category': np.random.choice(categories, size=100),
'merchant': np.random.choice(merchants, size=100)
}

# add the data to our dataframe
df = pd.DataFrame(data)

# introduce some missing values
# we randomly select 5 index values and set the column "amount" to null
df.loc[np.random.choice(df.index, size=5), 'amount'] = np.nan

# introduce some duplicates
# we select the first 5 rows and append them to the dataframe
dupes = df.iloc[:5]
df = pd.concat([df, dupes])

df.head()
```

|     |date|amount|category|merchant|
|---|---|---|---|---|
| 0   |2024-01-13|67.084665|Food|Starbucks|
| 1   |2024-01-16|96.305434|Shopping|Expedia|
| 2   |2024-01-22|68.751129|Travel|Expedia|
| 3   |2024-01-01|67.155299|Travel|Amazon|
| 4   |2024-01-04|NaN|Entertainment|Amazon|

The data types of the columns look good.

Do you see the **Non-Null** count column and the value of 99? This is how we can determine if our data has any null values.

``` python
df.info()
```

<class 'pandas.core.frame.DataFrame'>
Index: 105 entries, 0 to 4
Data columns (total 4 columns):
 #   Column    Non-Null Count  Dtype         
---  ------    --------------  -----         
 0   date      105 non-null    datetime64\[ns]
 1   amount    99 non-null     float64       
 2   category  105 non-null    object        
 3   merchant  105 non-null    object        
dtypes: datetime64\[ns](1), float64(1), object(2)
memory usage: 4.1+ KB

# Duplicates

Let's take care of the duplicates in the data

``` python
# here is how we can identify the duplicates
df[df.duplicated()]
```

|     | date       | amount    | category      | merchant  |
| --- | ---------- | --------- | ------------- | --------- |
| 0   | 2024-01-13 | 67.084665 | Food          | Starbucks |
| 1   | 2024-01-16 | 96.305434 | Shopping      | Expedia   |
| 2   | 2024-01-22 | 68.751129 | Travel        | Expedia   |
| 3   | 2024-01-01 | 67.155299 | Travel        | Amazon    |
| 4   | 2024-01-04 | NaN       | Entertainment | Amazon    |

``` python
# here is how we can pinpoint one of the duplicates
df[df.loc[:,'amount'].apply(lambda x: np.isclose(x,67.084665))]
```

|     | date       | amount    | category | merchant  |
| --- | ---------- | --------- | -------- | --------- |
| 0   | 2024-01-13 | 67.084665 | Food     | Starbucks |
| 0   | 2024-01-13 | 67.084665 | Food     | Starbucks |

``` python
# pandas makes it very easy to get rid of the duplicates
df = df.drop_duplicates()

df.head()
```

|     | date       | amount    | category      | merchant  |
| --- | ---------- | --------- | ------------- | --------- |
| 0   | 2024-01-13 | 67.084665 | Food          | Starbucks |
| 1   | 2024-01-16 | 96.305434 | Shopping      | Expedia   |
| 2   | 2024-01-22 | 68.751129 | Travel        | Expedia   |
| 3   | 2024-01-01 | 67.155299 | Travel        | Amazon    |
| 4   | 2024-01-04 | NaN       | Entertainment | Amazon    |

# Missing Values

Here I am just going to fill any missing values with the previous known value. If I don't find any, I will simply get rid of the row.

``` python
# these are the null values
df[df.loc[:,'amount'].isna()]
```

|     | date       | amount | category      | merchant  |
| --- | ---------- | ------ | ------------- | --------- |
| 4   | 2024-01-04 | NaN    | Entertainment | Amazon    |
| 23  | 2024-01-15 | NaN    | Food          | Expedia   |
| 24  | 2024-01-25 | NaN    | Travel        | McDonalds |
| 49  | 2024-01-08 | NaN    | Entertainment | McDonalds |
| 87  | 2024-01-24 | NaN    | Shopping      | McDonalds |

Let's see if we can look at the null rows and the previous row so we can see if forward fill will work for all the rows.

As you can see from the table below, we don't have a previous not-null value for any of our missing data. This means we cannot make a guess on what should be there and we just need to remove those rows.

``` python
# make sure data is ordered
df = df.sort_values(by=['date','category','merchant'])

# make sure index values are in order
# drop=True, this is to completely get rid of the old index and prevent it from being added as a column
df = df.reset_index(drop=True)

# get null rows
null_rows = df[df['amount'].isnull()]

# get null indexes
null_indices = null_rows.index

# get previous rows
previous_rows = df.loc[null_indices - 1]

# combine them
pd.concat([null_rows,previous_rows]).sort_index()
```

|     | date       | amount    | category      | merchant  |
| --- | ---------- | --------- | ------------- | --------- |
| 11  | 2024-01-03 | 70.789517 | Food          | Netflix   |
| 12  | 2024-01-04 | NaN       | Entertainment | Amazon    |
| 28  | 2024-01-08 | 18.313650 | Entertainment | Amazon    |
| 29  | 2024-01-08 | NaN       | Entertainment | McDonalds |
| 47  | 2024-01-14 | 71.979506 | Travel        | McDonalds |
| 48  | 2024-01-15 | NaN       | Food          | Expedia   |
| 80  | 2024-01-24 | 50.604329 | Shopping      | Expedia   |
| 81  | 2024-01-24 | NaN       | Shopping      | McDonalds |
| 85  | 2024-01-25 | 77.425285 | Entertainment | Netflix   |
| 86  | 2024-01-25 | NaN       | Travel        | McDonalds |

Let's remove the null rows under the **amount** column

``` python
# drop nulls
df = df.dropna()

# verify
df.info()
```

<class 'pandas.core.frame.DataFrame'>
Index: 95 entries, 0 to 99
Data columns (total 4 columns):
 #   Column    Non-Null Count  Dtype         
---  ------    --------------  -----         
 0   date      95 non-null     datetime64\[ns]
 1   amount    95 non-null     float64       
 2   category  95 non-null     object        
 3   merchant  95 non-null     object        
dtypes: datetime64\[ns](1), float64(1), object(2)
memory usage: 3.7+ KB

# Let's Answer The Questions

``` python
# What is the total transaction amount for each category (e.g., Food, Entertainment, Shopping)?
group = df.groupby('category')

group.sum(numeric_only=True)
```

|               | amount      |
| ------------- | ----------- |
| category      |             |
| Entertainment | 1576.840628 |
| Food          | 1063.905275 |
| Shopping      | 1060.962022 |
| Travel        | 1822.804450 |

``` python
# Which merchant has the highest total transaction amount?
group = df.groupby('merchant')

group.sum(numeric_only=True).sort_values(by='amount', ascending=False).head(1)
```

|           | amount      |
| --------- | ----------- |
| merchant  |             |
| McDonalds | 1453.475029 |
``` python
# What is the average transaction amount per day for each category?
group = df.groupby(['date','category'])

# show top 7 rows
group.mean(numeric_only=True).head(7)
```

|            |               | amount    |
| ---------- | ------------- | --------- |
| date       | category      |           |
| 2024-01-01 | Entertainment | 29.657538 |
| Shopping   | 73.336355     |           |
| Travel     | 46.258544     |           |
| 2024-01-02 | Entertainment | 19.257702 |
| Food       | 35.962879     |           |
| Shopping   | 89.060697     |           |
| Travel     | 89.037412     |           |

# Can You Solve the Bonus Question?

Identify the top 3 categories with the highest average transaction amount on weekends (Saturday and Sunday).