
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/restaurant_revival_challenge.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

### Description:   
You're the Data Scientist hired by a popular restaurant chain to analyze their sales data and help them optimize their menu and marketing strategies. The chain has 500 locations across the US, each offering a unique blend of local and national menu items. Your task is to clean, preprocess, and analyze the sales data to identify trends, patterns, and insights that can drive business growth.

### Tasks:  
- **Menu Engineering:** Create a new feature that calculates the average sales per menu item across all locations. Use this feature to identify the top 10 best-selling menu items and the bottom 10 worst-selling menu items.
- **Location Analysis:** Merge the sales data with a separate location data frame to create a single data frame with location-specific sales data. Then, use pivoting to calculate the total sales for each location and the top 3 best-selling menu items at each location.
- **Seasonal Trends:** Use data transformation to convert the sales data into a weekly format (i.e., sales per week of the year). Then, use reshaping to calculate the average sales per week for each menu item and identify the peak sales periods for each item.

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

The dataset consists of 100,000 sales records from a restaurant chain with 500 locations across the US, detailing sales amounts, dates, menu items, and location information. It provides a comprehensive snapshot of sales activity across various menu items, locations, and time periods.  

### Columns:
- **sale_id:** Unique sale identifier
- **menu_item_id:** Unique menu item identifier
- **location_id:** Unique location identifier
- **sale_date:** Date of sale
- **sales_amount:** Total sales amount
- **item_name:** Menu item name
- **category:** Menu item category (Appetizer, Entree, Dessert)
- **city:** Location city
- **state:** Location state

```python
# set the seed
np.random.seed(0)

# generate menu item data
menu_items = pd.DataFrame({
    'menu_item_id': range(1, 101),
    'item_name': [f'Menu Item {i}' for i in range(1, 101)],
    'category': np.random.choice(['Appetizer', 'Entree', 'Dessert'], 100)
})

# generate location data
locations = pd.DataFrame({
    'location_id': range(1, 501),
    'city': [f'City {i}' for i in range(1, 501)],
    'state': np.random.choice(['CA', 'NY', 'TX', 'FL'], 500)
})

# generate sales data
sales = pd.DataFrame({
    'sale_id': range(1, 100001),
    'menu_item_id': np.random.randint(1, 101, 100000),
    'location_id': np.random.randint(1, 501, 100000),
    'sale_date': pd.date_range('2022-01-01', '2022-12-31', periods=100000),
    'sales_amount': np.random.uniform(10, 100, 100000)
})
```

# Menu Engineering: 

Create a new feature that calculates the average sales per menu item across all locations. Use this feature to identify the top 10 best-selling menu items and the bottom 10 worst-selling menu items.

We need the `sales` and `menu_items` dataframes for this task. Let us look at the data types for each dataframe.

```python
menu_items.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 100 entries, 0 to 99
    Data columns (total 3 columns):
     #   Column        Non-Null Count  Dtype 
    ---  ------        --------------  ----- 
     0   menu_item_id  100 non-null    int64 
     1   item_name     100 non-null    object
     2   category      100 non-null    object
    dtypes: int64(1), object(2)
    memory usage: 2.5+ KB


```python
sales.info()
```
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 100000 entries, 0 to 99999
    Data columns (total 5 columns):
     #   Column        Non-Null Count   Dtype         
    ---  ------        --------------   -----         
     0   sale_id       100000 non-null  int64         
     1   menu_item_id  100000 non-null  int32         
     2   location_id   100000 non-null  int32         
     3   sale_date     100000 non-null  datetime64[ns]
     4   sales_amount  100000 non-null  float64       
    dtypes: datetime64[ns](1), float64(1), int32(2), int64(1)
    memory usage: 3.1 MB
    

Here is my strategy to complete the task:  
- Merge the `sales` and the `menu_items` dataframes
- Create a group object and determine the average sales per menu
- Order the data to select the top/bottom 10 

```python
# we are doing an inner merge where both dataframes must have matching menu_item_ids
df = sales.merge(menu_items, on='menu_item_id')
df.head()
```

|     | sale_id | menu_item_id | location_id | sale_date                     | sales_amount | item_name    | category  |
| --- | ------- | ------------ | ----------- | ----------------------------- | ------------ | ------------ | --------- |
| 0   | 1       | 27           | 17          | 2022-01-01 00:00:00.000000000 | 65.635255    | Menu Item 27 | Appetizer |
| 1   | 2       | 97           | 496         | 2022-01-01 00:05:14.499144991 | 50.715654    | Menu Item 97 | Dessert   |
| 2   | 3       | 52           | 133         | 2022-01-01 00:10:28.998289982 | 39.340689    | Menu Item 52 | Entree    |
| 3   | 4       | 74           | 130         | 2022-01-01 00:15:43.497434974 | 22.613624    | Menu Item 74 | Appetizer |
| 4   | 5       | 54           | 500         | 2022-01-01 00:20:57.996579965 | 28.305376    | Menu Item 54 | Entree    |


Notice the two columns in the results above (`item_name` and `category`); these came from the `menu_items` dataframe. 

Now that the merge is complete, the code below will get us the average sales amount per menu item.

```python
# create group object
group = df.groupby('item_name')

# get the average sales_amount
avg_sales = group['sales_amount'].mean()
avg_sales.head()
```

    item_name
    Menu Item 1      56.313134
    Menu Item 10     55.226327
    Menu Item 100    54.597751
    Menu Item 11     53.615531
    Menu Item 12     55.214489
    Name: sales_amount, dtype: float64



Order the data to get the top/bottom 10 rows.

```python
# top 10
avg_sales.sort_values(ascending=False).head(10)
```

    item_name
    Menu Item 99    57.838223
    Menu Item 57    57.167071
    Menu Item 8     56.666762
    Menu Item 75    56.603161
    Menu Item 24    56.436106
    Menu Item 61    56.349409
    Menu Item 1     56.313134
    Menu Item 86    56.188104
    Menu Item 84    56.018658
    Menu Item 74    56.018637
    Name: sales_amount, dtype: float64


```python
# bottom 10
avg_sales.sort_values().head(10)
```

    item_name
    Menu Item 32    53.261398
    Menu Item 88    53.599913
    Menu Item 23    53.607014
    Menu Item 62    53.612730
    Menu Item 11    53.615531
    Menu Item 33    53.620281
    Menu Item 4     53.830895
    Menu Item 81    53.931528
    Menu Item 66    53.957063
    Menu Item 15    54.032607
    Name: sales_amount, dtype: float64


# Location Analysis: 

Merge the sales data with a separate location data frame to create a single data frame with location-specific sales data. Then, use pivoting to calculate the total sales for each location and the top 3 best-selling menu items at each location.

Our last task merged sales data with menu items data and placed it in `df`. We can reuse the dataframe for this task.

```python
# add in the location data
location = df.merge(locations, on='location_id')
location.head()
```

|     | sale_id | menu_item_id | location_id | sale_date                     | sales_amount | item_name    | category  | city     | state |
| --- | ------- | ------------ | ----------- | ----------------------------- | ------------ | ------------ | --------- | -------- | ----- |
| 0   | 1       | 27           | 17          | 2022-01-01 00:00:00.000000000 | 65.635255    | Menu Item 27 | Appetizer | City 17  | NY    |
| 1   | 2       | 97           | 496         | 2022-01-01 00:05:14.499144991 | 50.715654    | Menu Item 97 | Dessert   | City 496 | CA    |
| 2   | 3       | 52           | 133         | 2022-01-01 00:10:28.998289982 | 39.340689    | Menu Item 52 | Entree    | City 133 | CA    |
| 3   | 4       | 74           | 130         | 2022-01-01 00:15:43.497434974 | 22.613624    | Menu Item 74 | Appetizer | City 130 | FL    |
| 4   | 5       | 54           | 500         | 2022-01-01 00:20:57.996579965 | 28.305376    | Menu Item 54 | Entree    | City 500 | CA    |

```python
# create group object
group = location.groupby(['city','state','item_name'])

# calculate the total sales for each group
total_sales = group['sales_amount'].sum()
total_sales
```

    city     state  item_name    
    City 1   TX     Menu Item 1      370.460969
                    Menu Item 10     271.469363
                    Menu Item 100    134.266236
                    Menu Item 11     243.996257
                    Menu Item 12     168.741860
                                        ...    
    City 99  NY     Menu Item 94     100.391216
                    Menu Item 96     141.602043
                    Menu Item 97      59.668432
                    Menu Item 98     295.399819
                    Menu Item 99      68.530342
    Name: sales_amount, Length: 43135, dtype: float64


### Method 1:
Here is how I was able to get the top 3 menu items per location using a custom function.

**Notes:**  
- Performing an aggregate function on a group is pretty simple. Performing an additional calculation afterwards, this is a bit harder.
- Since I reset the index, it kind of got in the way, so I added code specifically to remove this column (I used `droplevel()` to accomplish this)

```python
def get_top_three(grp):
    ''' sort grp descending and return the top 3 rows '''
    sorted = grp.sort_values('sales_amount', ascending=False)
    return sorted.head(3)

# reset the index before performing another groupby operation
# group by city and state
# apply the get_top_three function on the group
results = total_sales.reset_index().groupby(['city','state']).apply(get_top_three, include_groups=False)

# get rid of number column in the index
results.index = results.index.droplevel(2)
results.head()
```

|             |           | item_name    | sales_amount |
| ----------- | --------- | ------------ | ------------ |
| **city**    | **state** |              |              |
| **City 1**  | **TX**    | Menu Item 86 | 419.518108   |
|             | **TX**    | Menu Item 1  | 370.460969   |
|             | **TX**    | Menu Item 30 | 342.247197   |
| **City 10** | **TX**    | Menu Item 63 | 300.661903   |
|             | **TX**    | Menu Item 40 | 298.190699   |

### Method 2:
Here is how I was able to get the top 3 menu items per location using a lambda function.

> See the number column in the index? It's the 3rd one after the state column.
This column was created after the `reset_index()` operation. Method #1 shows you code on how to get rid of it.  

I prefer Method #1 as that method uses cleaner code and it will be easier to maintain.

```python
results = total_sales.reset_index().groupby(['city','state']).apply(lambda x: x.sort_values('sales_amount', ascending=False).head(3), include_groups=False)
results.head()
```

  

|             |           | item_name | sales_amount |            |
| ----------- | --------- | --------- | ------------ | ---------- |
| **city**    | **state** |           |              |            |
| **City 1**  | **TX**    | 73        | Menu Item 86 | 419.518108 |
|             |           | 0         | Menu Item 1  | 370.460969 |
|             |           | 20        | Menu Item 30 | 342.247197 |
| **City 10** | **TX**    | 133       | Menu Item 63 | 300.661903 |
|             |           | 113       | Menu Item 40 | 298.190699 |

# Seasonal Trends: 

Use data transformation to convert the sales data into a weekly format (i.e., sales per week of the year). Then, use reshaping to calculate the average sales per week for each menu item and identify the peak sales periods for each item.

I will be using the Pandas `resample` method to convert the data to weekly data. Note that this method expects out data to be a time series. 

Here is what I look for to determine if I am working with time series data:
- No missing values
- Dates are ordered sequentially
- Dates occur at consistent intervals

Note that our synthetic data does not meet the typical criteria for time series data, as it does not contain consistent intervals. Keep this in mind when working through this tutorial.

```python
# let us order the location data
location = location.sort_values(by='sale_date')

# Note: We don't have any missing values. Unfortunately our dates do not occur at consistent intervals

# resample our data to weekly and calculate the average sales_amount
trends = location.groupby('item_name').apply(lambda x: x.resample('W', on='sale_date')['sales_amount'].mean(), include_groups=False)
trends.head()
```

    item_name    sale_date 
    Menu Item 1  2022-01-02    58.064839
                 2022-01-09    52.142763
                 2022-01-16    49.412837
                 2022-01-23    58.902413
                 2022-01-30    59.432552
    Name: sales_amount, dtype: float64


Using the same strategy for the Location Analysis, we can get the peak sales date and sales amount per menu item. 

```python
def get_peak_sales(grp):
    sorted = grp.sort_values('sales_amount', ascending=False)
    return sorted.head(1)

results = trends.reset_index().groupby('item_name').apply(get_peak_sales, include_groups=False)

# get rid of number column in the index
results.index = results.index.droplevel(1)
results.head()
```

|                   | sale_date  | sales_amount |
| ----------------- | ---------- | ------------ |
| **item_name**     |            |              |
| **Menu Item 1**   | 2022-07-24 | 67.081441    |
| **Menu Item 10**  | 2022-01-02 | 71.869690    |
| **Menu Item 100** | 2022-01-02 | 87.621319    |
| **Menu Item 11**  | 2022-09-11 | 66.620358    |
| **Menu Item 12**  | 2023-01-01 | 72.514490    |

# Summary  

You've completed a tutorial on sales data analysis for a 500-location US restaurant chain. You explored menu engineering, location analysis, and seasonal trends to optimize menu and marketing strategies, gaining practical insights into data-driven business decisions.

### Key Takeaways:
- Merging datasets using `pd.merge()`
- Grouping and aggregating data using `df.groupby()`
- Identifying top and bottom performers using `sort_values()` and `head()`
- Using custom functions and lambda functions for complex aggregations
- Resampling time series data using `pd.resample()` to convert to weekly format
