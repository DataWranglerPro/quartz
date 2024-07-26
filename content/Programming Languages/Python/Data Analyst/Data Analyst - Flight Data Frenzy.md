
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/flight_data_frenzy.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

### Description:

As a Data Analyst at a busy airline, you're tasked with preparing a crucial dataset for analysis. However, the data is plagued by missing values, inconsistent formatting, and errors. Use Pandas to clean, transform, and prepare the dataset for takeoff, ensuring accurate insights to optimize flight operations.

### Tasks:

- **Missing Value Mayhem:** Identify and handle missing values in the 'DepartureTime' column, deciding whether to impute (replace missing values with an estimated value) or drop them.
- **Route Formatting Frenzy:** Standardize the 'Route' column, converting it to a consistent format (e.g., 'NYC-LAX' instead of 'New York to Los Angeles').
- **Duplicate Flight Chaos:** Remove duplicate flights while ensuring that crucial information isn't lost.

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

# The Data

The dataset contains information about flights operated by an airline. It includes details such as flight ID, departure time, route, number of passengers, and crew members.

### Columns:

- **FlightID:** A unique identifier for each flight
- **DepartureTime:** The scheduled departure time of each flight
- **Route:** The route of each flight, represented as a string (e.g., 'NYC-LAX' or 'New York to Los Angeles')
- **Passengers:** The number of passengers on each flight
- **Crew:** The number of crew members on each flight

``` python
# set the seed
np.random.seed(0)

flights = pd.DataFrame({
'FlightID': range(1000),
'DepartureTime': np.random.choice(['2024-01-01 10:00', '2024-01-15 12:30', '2024-02-01 09:00'], size=1000),
'Route': np.random.choice(['NYC-LAX', 'LAX-CHI', 'CHI-NYC', 'NYC-MIA', 'MIA-LAX', 'New York to Los Angeles'], size=1000),
'Passengers': np.random.randint(100, 200, size=1000),
'Crew': np.random.randint(5, 10, size=1000)

# introduce missing values
flights.loc[flights.index[::5], 'DepartureTime'] = np.nan

# introduce duplicates
dupes = pd.DataFrame(flights.iloc[:50])
flights = pd.concat([flights, dupes])

# introduce formatting issues
flights['Route'] = flights['Route'].apply(lambda x: x.replace('-', ' to '))

flights.head()
})
```

|     |FlightID|DepartureTime|Route|Passengers|Crew|
|---|---|---|---|---|---|
| 0   |0|NaN|LAX to CHI|141|5|
| 1   |1|2024-01-15 12:30|LAX to CHI|123|5|
| 2   |2|2024-01-01 10:00|New York to Los Angeles|152|5|
| 3   |3|2024-01-15 12:30|LAX to CHI|123|9|
| 4   |4|2024-01-15 12:30|MIA to LAX|172|8|

Let's start by looking at the datatypes.

Here are a few observations:

- Departure time has null values and after they get removed we need to make sure this column gets recognized as a date object.
- We can also see the additional 50 duplicates we added to the original dataframe.

``` python
flights.info()
```

<class 'pandas.core.frame.DataFrame'>
Index: 1050 entries, 0 to 49
Data columns (total 5 columns):
 #   Column         Non-Null Count  Dtype 
`---  ------         --------------  ----- 
 0   FlightID       1050 non-null   int64 
 1   DepartureTime  840 non-null    object
 2   Route          1050 non-null   object
 3   Passengers     1050 non-null   int32 
 4   Crew           1050 non-null   int32 
dtypes: int32(2), int64(1), object(2)
memory usage: 41.0+ KB

# Duplicates

We can take care of this issue at the beginning.

``` python
# identify the dupes
flights[flights.duplicated()].head()
```

|     | FlightID | DepartureTime    | Route                   | Passengers | Crew |
| --- | -------- | ---------------- | ----------------------- | ---------- | ---- |
| 0   | 0        | NaN              | LAX to CHI              | 141        | 5    |
| 1   | 1        | 2024-01-15 12:30 | LAX to CHI              | 123        | 5    |
| 2   | 2        | 2024-01-01 10:00 | New York to Los Angeles | 152        | 5    |
| 3   | 3        | 2024-01-15 12:30 | LAX to CHI              | 123        | 9    |
| 4   | 4        | 2024-01-15 12:30 | MIA to LAX              | 172        | 8    |

Let me show you one of the duplicates.

``` python
flights[flights['FlightID'] == 0]
```

|     | FlightID | DepartureTime | Route      | Passengers | Crew |
| --- | -------- | ------------- | ---------- | ---------- | ---- |
| 0   | 0        | NaN           | LAX to CHI | 141        | 5    |
| 0   | 0        | NaN           | LAX to CHI | 141        | 5    |

Here is how you can see all of them at once.

``` python
flights.loc[flights.duplicated().index,:]
```

|     | FlightID | DepartureTime    | Route                   | Passengers | Crew |
| --- | -------- | ---------------- | ----------------------- | ---------- | ---- |
| 0   | 0        | NaN              | LAX to CHI              | 141        | 5    |
| 0   | 0        | NaN              | LAX to CHI              | 141        | 5    |
| 1   | 1        | 2024-01-15 12:30 | LAX to CHI              | 123        | 5    |
| 1   | 1        | 2024-01-15 12:30 | LAX to CHI              | 123        | 5    |
| 2   | 2        | 2024-01-01 10:00 | New York to Los Angeles | 152        | 5    |
| ... | ...      | ...              | ...                     | ...        | ...  |
| 47  | 47       | 2024-01-15 12:30 | MIA to LAX              | 157        | 7    |
| 48  | 48       | 2024-02-01 09:00 | New York to Los Angeles | 168        | 8    |
| 48  | 48       | 2024-02-01 09:00 | New York to Los Angeles | 168        | 8    |
| 49  | 49       | 2024-01-01 10:00 | NYC to MIA              | 145        | 5    |
| 49  | 49       | 2024-01-01 10:00 | NYC to MIA              | 145        | 5    |
1150 rows × 5 columns

``` python
# drop duplicates
flights = flights.drop_duplicates()
```

# Missing Value Mayhem:

Identify and handle missing values in the 'DepartureTime' column, deciding whether to impute (replace missing values with an estimated value) or drop them.

This one is a bit tricky since we are working with synthetic data. Let's see if we can make a guess on what the correct departure time for the ones that have missing values.

We can see from the `describe()` method that there are only 3 dates.

``` python
flights['DepartureTime'].describe()
```

count                  800
unique                   3
top       2024-01-15 12:30
freq                   275
Name: DepartureTime, dtype: object

The three dates are:

- January 1st
- January 15th
- February 1st

``` python
flights['DepartureTime'].unique()
```

array([nan, '2024-01-15 12:30', '2024-01-01 10:00', '2024-02-01 09:00'],
      dtype=object)

The flight times do not seem to be related to the flight id value. Let's move on for the moment and clean up the Route column.

``` python
flights.head(10)
```

|     | FlightID | DepartureTime    | Route                   | Passengers | Crew |
| --- | -------- | ---------------- | ----------------------- | ---------- | ---- |
| 0   | 0        | NaN              | LAX to CHI              | 141        | 5    |
| 1   | 1        | 2024-01-15 12:30 | LAX to CHI              | 123        | 5    |
| 2   | 2        | 2024-01-01 10:00 | New York to Los Angeles | 152        | 5    |
| 3   | 3        | 2024-01-15 12:30 | LAX to CHI              | 123        | 9    |
| 4   | 4        | 2024-01-15 12:30 | MIA to LAX              | 172        | 8    |
| 5   | 5        | NaN              | New York to Los Angeles | 141        | 6    |
| 6   | 6        | 2024-01-01 10:00 | MIA to LAX              | 160        | 7    |
| 7   | 7        | 2024-02-01 09:00 | MIA to LAX              | 147        | 7    |
| 8   | 8        | 2024-01-01 10:00 | CHI to NYC              | 115        | 5    |
| 9   | 9        | 2024-01-01 10:00 | NYC to MIA              | 136        | 6    |

# Route Formatting Frenzy:

Standardize the 'Route' column, converting it to a consistent format (e.g., 'NYC-LAX' instead of 'New York to Los Angeles').

We will have to create a custom function that clean the data for us.

``` python
def clean_column(value):
	''' identify pattern and clean up
	'''
	value = value.replace('New York', 'NYC')
	value = value.replace('Los Angeles', 'LAX')
	value = value.replace(' to ', '-')
	return value

flights.loc[:,'Route'] = flights['Route'].apply(clean_column)
flights['Route'].unique()
```

array(['LAX-CHI', 'NYC-LAX', 'MIA-LAX', 'CHI-NYC', 'NYC-MIA'],
      dtype=object)

Now let's go back to the missing departure time rows. Let's see if we can find a pattern between routes and departure times.

``` python
group = flights.groupby(['Route','DepartureTime'])
grp1 = group.count()['FlightID'].rename('Flights')

grp1
```

Route    DepartureTime   
CHI-NYC  2024-01-01 10:00    34
         2024-01-15 12:30    54
         2024-02-01 09:00    51
LAX-CHI  2024-01-01 10:00    43
         2024-01-15 12:30    42
         2024-02-01 09:00    41
MIA-LAX  2024-01-01 10:00    42
         2024-01-15 12:30    35
         2024-02-01 09:00    44
NYC-LAX  2024-01-01 10:00    92
         2024-01-15 12:30    89
         2024-02-01 09:00    82
NYC-MIA  2024-01-01 10:00    50
         2024-01-15 12:30    55
         2024-02-01 09:00    46
Name: Flights, dtype: int64

Here are the missing flights for all the routes.

``` python
missing = flights['DepartureTime'].isna()
group = flights[missing].groupby('Route')

grp2 = group.count()['FlightID'].rename('FlightsMissing')
grp2
```

Route
CHI-NYC    27
LAX-CHI    41
MIA-LAX    35
NYC-LAX    63
NYC-MIA    34
Name: FlightsMissing, dtype: int64

Looking at the data below, I am not really seeing a pattern we can use to fill in the missing departure times.

``` python
pd.merge(grp1, grp2, left_index=True, right_index=True)
```

|         |                  | Flights | FlightsMissing |
| ------- | ---------------- | ------- | -------------- |
| Route   | DepartureTime    |         |                |
| CHI-NYC | 2024-01-01 10:00 | 34      | 27             |
|         | 2024-01-15 12:30 | 54      | 27             |
|         | 2024-02-01 09:00 | 51      | 27             |
| LAX-CHI | 2024-01-01 10:00 | 43      | 41             |
|         | 2024-01-15 12:30 | 42      | 41             |
|         | 2024-02-01 09:00 | 41      | 41             |
| MIA-LAX | 2024-01-01 10:00 | 42      | 35             |
|         | 2024-01-15 12:30 | 35      | 35             |
|         | 2024-02-01 09:00 | 44      | 35             |
| NYC-LAX | 2024-01-01 10:00 | 92      | 63             |
|         | 2024-01-15 12:30 | 89      | 63             |
|         | 2024-02-01 09:00 | 82      | 63             |
| NYC-MIA | 2024-01-01 10:00 | 50      | 34             |
|         | 2024-01-15 12:30 | 55      | 34             |
|         | 2024-02-01 09:00 | 46      | 34             |

# Conclusion

In this tutorial, we tackled the task of cleaning and preparing a dataset for analysis as a Data Analyst at a busy airline. We identified and addressed several issues, including:

- Analyzed missing values in the 'DepartureTime' column
- Standardized the formatting in the 'Route' column
- Removed duplicate flights

By the end of this tutorial, we successfully removed duplicates, standardized the 'Route' column, and explored the missing values in the 'DepartureTime' column, although we didn't find a clear pattern to impute the missing values.

### Can you find a pattern and fill in the missing Departure Times?