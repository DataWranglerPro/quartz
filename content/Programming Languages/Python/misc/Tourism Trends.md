
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/tourism_trends.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

### Description:  
You're a Data Analyst at a tourism board, tasked with analyzing visitor patterns for popular destinations. Your goal is to prepare and transform the data for insights.  

### Tasks:  
- **Task 1: Data Melting**  
Transform the dataset from wide format to long format, pivoting on the 'Quarter' column.
- **Task 2: Visitor Type Categories**  
Create a new column 'Visitor_Category' by mapping 'Destination' to 'Local' (Domestic) or 'Foreign' (International).
- **Task 3: Destination Groups**  
Create a new column 'Region' by grouping destinations into continents:
Asia (Tokyo, Bangkok)
Europe (Paris)
Americas (New York)
Oceania (Sydney)

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

The dataset consists of 10,000 entries, representing tourist visits to popular destinations.  

### Columns:  
- **Destination:** City visited (Paris, Tokyo, New York, Sydney, Bangkok)  
- **Age_Group:** Visitor age range (18-24, 25-34, 35-44, 45-54, 55+)  
- **Q1, Q2, Q3, Q4:** Visitors per quarter  
- **Revenue:** Revenue generated  

```python
# set the seed
np.random.seed(0)

# destination options
destinations = ['Paris', 'Tokyo', 'New York', 'Sydney', 'Bangkok']

# age groups
age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']

# quarter options
quarters = ['Q1', 'Q2', 'Q3', 'Q4']

# generate data
data = {
    'Destination': np.random.choice(destinations, size=10000),
    'Age_Group': np.random.choice(age_groups, size=10000),
    'Q1': np.random.randint(1, 100, size=10000),
    'Q2': np.random.randint(1, 100, size=10000),
    'Q3': np.random.randint(1, 100, size=10000),
    'Q4': np.random.randint(1, 100, size=10000),
    'Revenue': np.random.randint(100, 1000, size=10000)
}

df = pd.DataFrame(data)

df.head()
```

|     | Destination | Age_Group | Q1  | Q2  | Q3  | Q4  | Revenue |
| --- | ----------- | --------- | --- | --- | --- | --- | ------- |
| 0   | Bangkok     | 55+       | 76  | 75  | 85  | 97  | 679     |
| 1   | Paris       | 25-34     | 71  | 92  | 69  | 83  | 900     |
| 2   | Sydney      | 55+       | 51  | 19  | 55  | 12  | 555     |
| 3   | Sydney      | 35-44     | 20  | 40  | 69  | 49  | 213     |
| 4   | Sydney      | 25-34     | 74  | 66  | 68  | 46  | 227     |

Let us take a quick look at the data types.

We can see we have out 10,000 rows, no null values, and only the "Destination" and "Age_Group" columns are of type string.

```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 10000 entries, 0 to 9999
    Data columns (total 7 columns):
     #   Column       Non-Null Count  Dtype 
    ---  ------       --------------  ----- 
     0   Destination  10000 non-null  object
     1   Age_Group    10000 non-null  object
     2   Q1           10000 non-null  int32 
     3   Q2           10000 non-null  int32 
     4   Q3           10000 non-null  int32 
     5   Q4           10000 non-null  int32 
     6   Revenue      10000 non-null  int32 
    dtypes: int32(5), object(2)
    memory usage: 351.7+ KB
    

# Task 1: Data Melting
Transform the dataset from wide format to long format, pivoting on the 'Quarter' column

This task is asking us to transform the Q1, Q2, Q3, Q4 columns into one column we can call "visitors". In order to accomplish this, pandas provides us with a method called `pd.melt()`.

**Parameters:**
- id_vars - all of the columns to leave alone
- value_vars - all of the columns you want to melt/pivot
- var_name - what do you want to call the columns you are pivoting
- value_name - what do the values under the pivoting columns represent.

```python
# columns to keep
keep_cols = ["Destination","Age_Group","Revenue"]

new_df = pd.melt(df, id_vars=keep_cols, var_name="Quarter", value_name="Visitors")
new_df.head()
```

|     | Destination | Age_Group | Revenue | Quarter | Visitors |
| --- | ----------- | --------- | ------- | ------- | -------- |
| 0   | Bangkok     | 55+       | 679     | Q1      | 76       |
| 1   | Paris       | 25-34     | 900     | Q1      | 71       |
| 2   | Sydney      | 55+       | 555     | Q1      | 51       |
| 3   | Sydney      | 35-44     | 213     | Q1      | 20       |
| 4   | Sydney      | 25-34     | 227     | Q1      | 74       |

# Task 2: Visitor Type Categories
Create a new column 'Visitor_Category' by mapping 'Destination' to 'Local' (Domestic) or 'Foreign' (International).

I will first define what countries are Domestic or International.

- **Domestic** = 'New York'
- **International** = 'Paris', 'Tokyo', 'Sydney', 'Bangkok'

```python
# map the values
mapping = {**dict.fromkeys(['Paris', 'Tokyo', 'Sydney', 'Bangkok'], 'International'), 
           **dict.fromkeys(['New York'], 'Domestic')}

# apply the map to the Destination column
new_df['Visitor_Category'] = new_df['Destination'].map(mapping)
new_df.head(8)
```

|     | Destination | Age_Group | Revenue | Quarter | Visitors | Visitor_Category |
| --- | ----------- | --------- | ------- | ------- | -------- | ---------------- |
| 0   | Bangkok     | 55+       | 679     | Q1      | 76       | International    |
| 1   | Paris       | 25-34     | 900     | Q1      | 71       | International    |
| 2   | Sydney      | 55+       | 555     | Q1      | 51       | International    |
| 3   | Sydney      | 35-44     | 213     | Q1      | 20       | International    |
| 4   | Sydney      | 25-34     | 227     | Q1      | 74       | International    |
| 5   | Tokyo       | 45-54     | 438     | Q1      | 52       | International    |
| 6   | Sydney      | 55+       | 921     | Q1      | 60       | International    |
| 7   | New York    | 18-24     | 354     | Q1      | 98       | Domestic         |

# Task 3: Destination Groups  
Create a new column 'Region' by grouping destinations into continents: 
- Asia (Tokyo, Bangkok)
- Europe (Paris)
- Americas (New York)
- Oceania (Sydney)

We can use the same strategy from Task #2. 

```python
# map the values
mapping = {**dict.fromkeys(['Tokyo', 'Bangkok'], 'Asia'), 
           **dict.fromkeys(['Paris'], 'Europe'),
           **dict.fromkeys(['New York'], 'Americas'),
           **dict.fromkeys(['Sydney'], 'Oceania')}

# apply the map to the Destination column
new_df['Region'] = new_df['Destination'].map(mapping)
new_df.head()
```

|     | Destination | Age_Group | Revenue | Quarter | Visitors | Visitor_Category | Region  |
| --- | ----------- | --------- | ------- | ------- | -------- | ---------------- | ------- |
| 0   | Bangkok     | 55+       | 679     | Q1      | 76       | International    | Asia    |
| 1   | Paris       | 25-34     | 900     | Q1      | 71       | International    | Europe  |
| 2   | Sydney      | 55+       | 555     | Q1      | 51       | International    | Oceania |
| 3   | Sydney      | 35-44     | 213     | Q1      | 20       | International    | Oceania |
| 4   | Sydney      | 25-34     | 227     | Q1      | 74       | International    | Oceania |


# Summary  
You just went through a Pandas tutorial that walked you through data analysis of tourism trends. It covered transforming data from wide to long format, creating visitor categories like Domestic and International, and grouping destinations by continent like Asia, Europe, Americas, and Oceania. The tutorial used Pandas functions like `pd.melt()` and `map()` to get the job done, giving you insights into tourist visit patterns.

### Key Takeaways  
- Data transformation using `pd.melt()`.
- Creating new columns using mapping.
- Data categorization using the `map()` function.















