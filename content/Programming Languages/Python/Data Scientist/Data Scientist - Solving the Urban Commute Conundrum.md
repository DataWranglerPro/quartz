
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/94b9d54b994bfd2b87f7dc4de521cb639b9a7a74/content/Assets/notebooks/urban_commute_conundrum.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

### Description:   
Imagine you're a data scientist working for a city's transportation department, tasked with optimizing public transportation routes to reduce congestion and improve air quality. You have access to a large dataset containing information on bus routes, schedules, and passenger traffic.  

### Tasks:
- **Route Optimization:** Merge two datasets, bus_routes and passenger_traffic, on the route_id column. Then, calculate the average passenger count for each route and identify the top 5 routes with the highest average passenger traffic.
- **Schedule Alignment:** Transform the schedules column in the bus_routes dataset from a string format ("HH:MM-HH:MM") to a datetime format. Then, calculate the total daily operating hours for each route and identify routes with operating hours exceeding 18 hours.
- **Passenger Flow Analysis:** Pivot the passenger_traffic dataset to create a new table showing the total passenger count for each hour of the day, across all routes. Then, identify the peak hour with the highest passenger traffic.

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

The dataset consists of two CSV files:  
- bus_routes.csv: Contains information on bus routes, including route_id, route_name, and schedules.
- passenger_traffic.csv: Contains information on passenger traffic, including route_id, hour, and passenger_count.
### Columns:  
- **route_id:** Unique identifier for each bus route
- **route_name:** Name of each bus route
- **schedules:** String representation of bus schedules ("HH:MM-HH:MM")
- **hour:** Hour of the day (1-24)
- **passenger_count:** Number of passengers on a given route at a given hour

```python
# set the seed
np.random.seed(0)

# generate bus routes dataset
bus_routes = pd.DataFrame({
    'route_id': np.arange(1, 101),
    'route_name': ['Route ' + str(i) for i in np.arange(1, 101)],
    'schedules': ['08:00-18:00' if i % 2 == 0 else '09:00-20:00' for i in np.arange(1, 101)]
})

# generate passenger traffic dataset
passenger_traffic = pd.DataFrame({
    'route_id': np.repeat(np.arange(1, 101), 24),
    'hour': np.tile(np.arange(1, 25), 100),
    'passenger_count': np.random.randint(10, 100, size=2400)
})

# export to CSV
bus_routes.to_csv('bus_routes.csv', index=False)
passenger_traffic.to_csv('passenger_traffic.csv', index=False)
```

# Read CSV files  

We will also take a look at the column data types and verify they are correct.  

**Note:** We will convert the "schedules" column from string to datetime in the Schedule Alignment task.

```python
df_bus_routes = pd.read_csv('bus_routes.csv')
df_bus_routes.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 100 entries, 0 to 99
    Data columns (total 3 columns):
     #   Column      Non-Null Count  Dtype 
    ---  ------      --------------  ----- 
     0   route_id    100 non-null    int64 
     1   route_name  100 non-null    object
     2   schedules   100 non-null    object
    dtypes: int64(1), object(2)
    memory usage: 2.5+ KB

```python
df_passenger_traffic = pd.read_csv('passenger_traffic.csv')
df_passenger_traffic.info()
```
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 2400 entries, 0 to 2399
    Data columns (total 3 columns):
     #   Column           Non-Null Count  Dtype
    ---  ------           --------------  -----
     0   route_id         2400 non-null   int64
     1   hour             2400 non-null   int64
     2   passenger_count  2400 non-null   int64
    dtypes: int64(3)
    memory usage: 56.4 KB
    
# Route Optimization  

Merge two datasets, bus_routes and passenger_traffic, on the route_id column. Then, calculate the average passenger count for each route and identify the top 5 routes with the highest average passenger traffic.

```python
merged = df_bus_routes.merge(df_passenger_traffic, on='route_id')
merged.head()
```

|     | route_id | route_name | schedules   | hour | passenger_count |
| --- | -------- | ---------- | ----------- | ---- | --------------- |
| 0   | 1        | Route 1    | 09:00-20:00 | 1    | 54              |
| 1   | 1        | Route 1    | 09:00-20:00 | 2    | 57              |
| 2   | 1        | Route 1    | 09:00-20:00 | 3    | 74              |
| 3   | 1        | Route 1    | 09:00-20:00 | 4    | 77              |
| 4   | 1        | Route 1    | 09:00-20:00 | 5    | 77              |


```python
# create group object
group = merged.groupby('route_name')

# average passenger traffic
avg_pass_traffic = group['passenger_count'].mean()
avg_pass_traffic.head()
```

    route_name
    Route 1      67.750000
    Route 10     50.875000
    Route 100    57.625000
    Route 11     52.833333
    Route 12     50.208333
    Name: passenger_count, dtype: float64



```python
# identify the top 5 routes
avg_pass_traffic.sort_values(ascending=False).head(5)
```

    route_name
    Route 1     67.750000
    Route 77    64.416667
    Route 66    63.250000
    Route 24    62.666667
    Route 45    61.541667
    Name: passenger_count, dtype: float64


# Schedule Alignment  

Transform the schedules column in the bus_routes dataset from a string format ("HH:MM-HH:MM") to a datetime format. Then, calculate the total daily operating hours for each route and identify routes with operating hours exceeding 18 hours.

```python
df_bus_routes.head()
```

|     | route_id | route_name | schedules   |
| --- | -------- | ---------- | ----------- |
| 0   | 1        | Route 1    | 09:00-20:00 |
| 1   | 2        | Route 2    | 08:00-18:00 |
| 2   | 3        | Route 3    | 09:00-20:00 |
| 3   | 4        | Route 4    | 08:00-18:00 |
| 4   | 5        | Route 5    | 09:00-20:00 |


Since we have two dates in one column, we will have to split the "schedules" column into two columns.  

The `expand=True` parameter lets us split an existing column into two new ones.

```python
# split the string into start and end times
df_bus_routes[["start_time", "end_time"]] = df_bus_routes["schedules"].str.split("-", expand=True)

df_bus_routes.head()
```

|     | route_id | route_name | schedules   | start_time | end_time |
| --- | -------- | ---------- | ----------- | ---------- | -------- |
| 0   | 1        | Route 1    | 09:00-20:00 | 09:00      | 20:00    |
| 1   | 2        | Route 2    | 08:00-18:00 | 08:00      | 18:00    |
| 2   | 3        | Route 3    | 09:00-20:00 | 09:00      | 20:00    |
| 3   | 4        | Route 4    | 08:00-18:00 | 08:00      | 18:00    |
| 4   | 5        | Route 5    | 09:00-20:00 | 09:00      | 20:00    |

We now can make use of `pd.to_datetime` to convert the strings into dates. The only potential issue is that the dates default to 1900.

```python
df_bus_routes["new_start_time"] = pd.to_datetime(df_bus_routes['start_time'], format="%H:%M")
df_bus_routes["new_end_time"] = pd.to_datetime(df_bus_routes['end_time'], format="%H:%M")
df_bus_routes.head()
```

|     | route_id | route_name | schedules   | start_time | end_time | new_start_time      | new_end_time        |
| --- | -------- | ---------- | ----------- | ---------- | -------- | ------------------- | ------------------- |
| 0   | 1        | Route 1    | 09:00-20:00 | 09:00      | 20:00    | 1900-01-01 09:00:00 | 1900-01-01 20:00:00 |
| 1   | 2        | Route 2    | 08:00-18:00 | 08:00      | 18:00    | 1900-01-01 08:00:00 | 1900-01-01 18:00:00 |
| 2   | 3        | Route 3    | 09:00-20:00 | 09:00      | 20:00    | 1900-01-01 09:00:00 | 1900-01-01 20:00:00 |
| 3   | 4        | Route 4    | 08:00-18:00 | 08:00      | 18:00    | 1900-01-01 08:00:00 | 1900-01-01 18:00:00 |
| 4   | 5        | Route 5    | 09:00-20:00 | 09:00      | 20:00    | 1900-01-01 09:00:00 | 1900-01-01 20:00:00 |


Here is how I was able to change the default date of 1900 to 2024. It was not that pretty.

```python
# calculate the number of days since 1900
origin_days = (pd.to_datetime('2024-01-01') - pd.to_datetime('1900-01-01')).days

# we move our dates to 2024
df_bus_routes["new_start_time"] = df_bus_routes["new_start_time"] + pd.Timedelta(days=origin_days)
df_bus_routes["new_end_time"] = df_bus_routes["new_end_time"] + pd.Timedelta(days=origin_days)
df_bus_routes.head()
```

|     | route_id | route_name | schedules   | start_time | end_time | new_start_time      | new_end_time        |
| --- | -------- | ---------- | ----------- | ---------- | -------- | ------------------- | ------------------- |
| 0   | 1        | Route 1    | 09:00-20:00 | 09:00      | 20:00    | 2024-01-01 09:00:00 | 2024-01-01 20:00:00 |
| 1   | 2        | Route 2    | 08:00-18:00 | 08:00      | 18:00    | 2024-01-01 08:00:00 | 2024-01-01 18:00:00 |
| 2   | 3        | Route 3    | 09:00-20:00 | 09:00      | 20:00    | 2024-01-01 09:00:00 | 2024-01-01 20:00:00 |
| 3   | 4        | Route 4    | 08:00-18:00 | 08:00      | 18:00    | 2024-01-01 08:00:00 | 2024-01-01 18:00:00 |
| 4   | 5        | Route 5    | 09:00-20:00 | 09:00      | 20:00    | 2024-01-01 09:00:00 | 2024-01-01 20:00:00 |


Now that we have our date objects looking good, we can finally calculate the hours between the two new columns.

I could not figure out why the index was being placed in my group object. This is the reason you see the code `reset_index` below.

```python
# create group object
group = df_bus_routes.groupby('route_name')

# calculate the hours between the two column
result = group.apply(lambda x: (x['new_end_time'] - x['new_start_time']).dt.seconds/3600, include_groups=False)

# drop the original index
result = result.reset_index(level=1, drop=True)

# sort descending
result.sort_values(ascending=False).head()
```


    route_name
    Route 1     11.0
    Route 7     11.0
    Route 45    11.0
    Route 47    11.0
    Route 49    11.0
    dtype: float64


The task requested us to calculate the "routes with operating hours exceeding 18 hours", but as you can see from the results above, none of the routes go past 11 hours.

# Passenger Flow Analysis: 

Pivot the passenger_traffic dataset to create a new table showing the total passenger count for each hour of the day, across all routes. Then, identify the peak hour with the highest passenger traffic.

```python
pivot_table = df_passenger_traffic.pivot_table(values='passenger_count', index='hour', columns='route_id', aggfunc='sum', margins=True)

pivot_table.tail()
```

| route_id | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   | ... | 92   | 93   | 94   | 95   | 96   | 97   | 98   | 99   | 100  | All    |
| -------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | --- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ------ |
| **hour** |      |      |      |      |      |      |      |      |      |      |     |      |      |      |      |      |      |      |      |      |        |
| **21**   | 91   | 42   | 67   | 89   | 33   | 42   | 24   | 66   | 42   | 33   | ... | 80   | 68   | 69   | 46   | 24   | 65   | 43   | 48   | 33   | 5064   |
| **22**   | 47   | 41   | 45   | 23   | 69   | 64   | 14   | 34   | 21   | 13   | ... | 99   | 90   | 46   | 69   | 46   | 84   | 28   | 58   | 72   | 6028   |
| **23**   | 35   | 84   | 21   | 95   | 12   | 10   | 77   | 89   | 94   | 56   | ... | 85   | 38   | 54   | 44   | 14   | 41   | 16   | 70   | 58   | 5506   |
| **24**   | 87   | 33   | 56   | 58   | 72   | 48   | 21   | 51   | 20   | 60   | ... | 27   | 19   | 95   | 80   | 57   | 93   | 12   | 16   | 69   | 5040   |
| **All**  | 1626 | 1342 | 1086 | 1341 | 1208 | 1269 | 1183 | 1468 | 1383 | 1221 | ... | 1356 | 1414 | 1034 | 1098 | 1087 | 1218 | 1267 | 1236 | 1383 | 130554 |

5 rows × 101 columns


Here are the steps to get the most popular hour:  
- Remove the row margin named "All"
- Select the column margin named "All"
- Order the row desceding and select the top value 

```python
# remove the "All" row
remove_all_row = pivot_table.index.drop('All')

# find the most popular hour
pivot_table.loc[remove_all_row,'All'].sort_values(ascending=False).head(1)
```


    hour
    22    6028
    Name: All, dtype: int64


Here are the steps to get the most popular route:  
- Remove the column named "All"
- Select the row margin named "All"
- Order the row desceding and select the top value 

```python
# remove the "All" row
remove_all_column = pivot_table.columns.drop('All')

# find the most popular hour
pivot_table.loc['All', remove_all_column].sort_values(ascending=False).head(1)
```

    route_id
    1    1626
    Name: All, dtype: int64


# Summary:  
The tutorial demonstrated how to use Pandas to analyze a dataset containing information on bus routes, schedules, and passenger traffic. It covered three tasks: route optimization, schedule alignment, and passenger flow analysis.  

### Key Takeaways:
- You learned how to merge datasets on a common column and calculate average values for each group.
- You discovered how to identify top-performing groups based on calculated averages.
- You learned how to transform string data into datetime format for easier analysis.
- You understood how to calculate time differences.
- You learned how to pivot data to create new tables with aggregated values.

### Pandas Functions Used:  
- merge
- groupby
- mean
- sort_values
- str.split
- pd.to_datetime
- pivot_table
- reset_index
- apply
- dt.seconds
- drop
