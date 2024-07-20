
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/e-commerce_insights.ipynb), offering an alternative platform for your learning convenience.
> - [Pandas Ninja](https://hedaro.gumroad.com/l/jVeRh): Take your skills to the next level with comprehensive Jupyter Notebook tutorials covering dates, group by, plotting, pivot tables, and more. Includes specialized tutorials for Excel and SQL developers, helping you master data analysis with Pandas.

### Description:  
Imagine you're a data analyst for a popular travel company that offers customized vacation packages. Your boss wants you to prepare the data for analysis, but it's a bit of a mess. Your task is to use Pandas to clean, transform, and prepare the data for analysis.  

### Tasks:  
- **Data Standardization:** Standardize the 'Location' column in the customers dataset by converting all values to title case and replacing any missing values with a custom category (e.g., 'Unknown'). Additionally, extract the first name and last name from the 'Customer Name' column and create two new columns.
- **Data Feature Engineering:** Create two new columns in the travel_history dataset: Trip Length (in nights) and Spend Per Night. Calculate Trip Length by using a random integer between 3 and 14 (representing the number of nights stayed), and calculate Spend Per Night by dividing Spend by Trip Length.
- **Data Merging:** Merge the customers, travel_history, and packages datasets into a single dataset, using appropriate join types and handling any data inconsistencies.

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

The data is related to a travel company and includes information about customer demographics, travel preferences, and package offerings.  

### Columns:  
**Customers Table**
- **Customer ID (int):** Unique identifier for each customer
- **Customer Name (str):** Full name of customer
- **Age (int):** Customer age
- **Location (str):** Customer location (Urban/Rural)
- **Travel Frequency (int):** Number of times the customer has traveled with the company (1-5)

**Travel History Table**  
- **Customer ID (int):** Foreign key referencing the Customer ID in the Customers table
- **Package Type (str):** Type of package booked (Adventure/Relaxation/Culture)
- **Destination (str):** Destination of the trip (Beach/City/Nature)
- **Spend (int):** Total amount spent on the trip (500-5000)

**Packages Table**
- **Package ID (int):** Unique identifier for each package
- **Package Type (str):** Type of package (Adventure/Relaxation/Culture)
- **Accommodation (str):** Type of accommodation offered (Budget/Mid-range/Luxury)
- **Activities (str):** Type of activities offered (Sightseeing/Adventure/Relaxation)
- **Transportation (str):** Type of transportation offered (Car/Bus/Train)

```python
# set the seed
np.random.seed(0)

# Generate customer data
customers = pd.DataFrame({
    'Customer ID': range(1, 1001),
    'Age': np.random.randint(25, 65, size=1000),
    'Location': np.random.choice(['urban', 'rural', None], size=1000, p=[0.7, 0.2, 0.1]),
    'Travel Frequency': np.random.randint(1, 5, size=1000)
})

# Generate travel history data
travel_history = pd.DataFrame({
    'Customer ID': np.random.choice(customers['Customer ID'], size=5000, replace=True),
    'Package Type': np.random.choice(['Adventure', 'Relaxation', 'Culture'], size=5000, p=[0.4, 0.3, 0.3]),
    'Destination': np.random.choice(['Beach', 'City', 'Nature'], size=5000, p=[0.5, 0.3, 0.2]),
    'Spend': np.random.randint(500, 5000, size=5000)
})

# Generate package data
packages = pd.DataFrame({
    'Package ID': range(1, 51),
    'Package Type': np.random.choice(['Adventure', 'Relaxation', 'Culture'], size=50, p=[0.4, 0.3, 0.3]),
    'Accommodation': np.random.choice(['Budget', 'Mid-range', 'Luxury'], size=50, p=[0.4, 0.3, 0.3]),
    'Activities': np.random.choice(['Sightseeing', 'Adventure', 'Relaxation'], size=50, p=[0.4, 0.3, 0.3]),
    'Transportation': np.random.choice(['Car', 'Bus', 'Train'], size=50, p=[0.4, 0.3, 0.3])
})

# create a 'Customer Name' column to include first name and last name
customers['Customer Name'] = customers['Customer ID'].apply(lambda x: f'{np.random.choice(["John", "Jane", "Bob", "Alice"])}_{np.random.choice(["Doe", "Smith", "Johnson", "Williams"])}_{x}')

```

# Data Standardization:  

- Standardize the 'Location' column in the customers dataset by converting all values to title case and replacing any missing values with a custom category (e.g., 'Unknown').
- Extract the first name and last name from the 'Customer Name' column and create two new columns.

Let us take a look at the data types for the customers dataframe.

```python
customers.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1000 entries, 0 to 999
    Data columns (total 5 columns):
     #   Column            Non-Null Count  Dtype 
    ---  ------            --------------  ----- 
     0   Customer ID       1000 non-null   int64 
     1   Age               1000 non-null   int32 
     2   Location          885 non-null    object
     3   Travel Frequency  1000 non-null   int32 
     4   Customer Name     1000 non-null   object
    dtypes: int32(2), int64(1), object(2)
    memory usage: 31.4+ KB
    

I am going to first replace the missing values with the string "Unknown".

```python
# identify missing values
missing = customers["Location"].isnull()

# replace missing values
customers.loc[missing, "Location"] = 'Unknown'

customers.Location.unique()
```

    array(['rural', 'urban', 'Unknown'], dtype=object)



Now, to make the first letter of each string uppercase, we can simply use the method named `capitalize()`

```python
customers['Location'] = customers.Location.str.capitalize()
customers.Location.unique()
```

    array(['Rural', 'Urban', 'Unknown'], dtype=object)


The next task is to create two new columns.  
- First Name
- Last Name

Since the names are all seperated by an underscore, we can simply split the string by that character and extract the first and last name.

```python
customers['First Name'] = customers['Customer Name'].apply(lambda x: x.split('_')[0])
customers['Last Name'] = customers['Customer Name'].apply(lambda x: x.split('_')[1])

customers.head()
```

|     | Customer ID | Package Type | Destination | Spend | Trip Length |
| --- | ----------- | ------------ | ----------- | ----- | ----------- |
| 0   | 400         | Relaxation   | Beach       | 3403  | 11          |
| 1   | 957         | Culture      | Beach       | 3250  | 7           |
| 2   | 385         | Relaxation   | City        | 616   | 3           |
| 3   | 168         | Adventure    | City        | 2098  | 6           |
| 4   | 550         | Relaxation   | Beach       | 4859  | 3           |

# Data Feature Engineering:  

Create two new columns in the travel_history dataset: Trip Length (in nights) and Spend Per Night. Calculate Trip Length by using a random integer between 3 and 14 (representing the number of nights stayed), and calculate Spend Per Night by dividing Spend by Trip Length.

```python
# note I used 5,000 since that is how many rows we have in this dataframe
travel_history['Trip Length'] = np.random.randint(3, 15, size=5000)
travel_history.head()
```

|     | Customer ID | Package Type | Destination | Spend | Trip Length |
| --- | ----------- | ------------ | ----------- | ----- | ----------- |
| 0   | 400         | Relaxation   | Beach       | 3403  | 11          |
| 1   | 957         | Culture      | Beach       | 3250  | 7           |
| 2   | 385         | Relaxation   | City        | 616   | 3           |
| 3   | 168         | Adventure    | City        | 2098  | 6           |
| 4   | 550         | Relaxation   | Beach       | 4859  | 3           |

```python
travel_history['Spend Per Night'] = travel_history['Spend'].div(travel_history['Trip Length'])
travel_history.head()
```

|     | Customer ID | Package Type | Destination | Spend | Trip Length | Spend Per Night |
| --- | ----------- | ------------ | ----------- | ----- | ----------- | --------------- |
| 0   | 400         | Relaxation   | Beach       | 3403  | 11          | 309.363636      |
| 1   | 957         | Culture      | Beach       | 3250  | 7           | 464.285714      |
| 2   | 385         | Relaxation   | City        | 616   | 3           | 205.333333      |
| 3   | 168         | Adventure    | City        | 2098  | 6           | 349.666667      |
| 4   | 550         | Relaxation   | Beach       | 4859  | 3           | 1619.666667     |

# Data Merging:  

Merge the customers, travel_history, and packages datasets into a single dataset, using appropriate join types and handling any data inconsistencies.  

Items to consider:  
- Find out if there are Customer IDs that do not match between the customers and the travel_history dataframes
- Find out if there are Package Types that do not match between the travel_history and the packages dataframes
- Since Package Type is of type String, you need to make sure capitalization is identical between the two datasets and look out for extra spaces in the string values

```python
customers.merge(travel_history, left_on='Customer ID', right_on='Customer ID').merge(packages, left_on='Package Type', right_on='Package Type')
```

|       | Customer ID | Age | Location | Travel Frequency | Customer Name     | First Name | Last Name | Package Type | Destination | Spend | Trip Length | Spend Per Night | Package ID | Accommodation | Activities  | Transportation |
| ----- | ----------- | --- | -------- | ---------------- | ----------------- | ---------- | --------- | ------------ | ----------- | ----- | ----------- | --------------- | ---------- | ------------- | ----------- | -------------- |
| 0     | 1           | 25  | Rural    | 2                | John_Doe_1        | John       | Doe       | Adventure    | Beach       | 3236  | 4           | 809.0           | 2          | Budget        | Adventure   | Train          |
| 1     | 1           | 25  | Rural    | 2                | John_Doe_1        | John       | Doe       | Adventure    | Beach       | 3236  | 4           | 809.0           | 3          | Mid-range     | Relaxation  | Train          |
| 2     | 1           | 25  | Rural    | 2                | John_Doe_1        | John       | Doe       | Adventure    | Beach       | 3236  | 4           | 809.0           | 7          | Luxury        | Relaxation  | Car            |
| 3     | 1           | 25  | Rural    | 2                | John_Doe_1        | John       | Doe       | Adventure    | Beach       | 3236  | 4           | 809.0           | 9          | Luxury        | Sightseeing | Bus            |
| 4     | 1           | 25  | Rural    | 2                | John_Doe_1        | John       | Doe       | Adventure    | Beach       | 3236  | 4           | 809.0           | 13         | Budget        | Adventure   | Bus            |
| ...   | ...         | ... | ...      | ...              | ...               | ...        | ...       | ...          | ...         | ...   | ...         | ...             | ...        | ...           | ...         | ...            |
| 86739 | 1000        | 43  | Urban    | 2                | Jane_Johnson_1000 | Jane       | Johnson   | Adventure    | Nature      | 2233  | 11          | 203.0           | 45         | Luxury        | Relaxation  | Car            |
| 86740 | 1000        | 43  | Urban    | 2                | Jane_Johnson_1000 | Jane       | Johnson   | Adventure    | Nature      | 2233  | 11          | 203.0           | 47         | Luxury        | Adventure   | Car            |
| 86741 | 1000        | 43  | Urban    | 2                | Jane_Johnson_1000 | Jane       | Johnson   | Adventure    | Nature      | 2233  | 11          | 203.0           | 48         | Budget        | Sightseeing | Car            |
| 86742 | 1000        | 43  | Urban    | 2                | Jane_Johnson_1000 | Jane       | Johnson   | Adventure    | Nature      | 2233  | 11          | 203.0           | 49         | Mid-range     | Sightseeing | Car            |
| 86743 | 1000        | 43  | Urban    | 2                | Jane_Johnson_1000 | Jane       | Johnson   | Adventure    | Nature      | 2233  | 11          | 203.0           | 50         | Budget        | Adventure   | Car            |

86744 rows × 16 columns

# Summary  

This tutorial demonstrates how to use Pandas to clean, transform, and prepare travel data for analysis by standardizing data formats, creating new features through calculations, and merging datasets. By following these steps, you'll learn how to handle common data preparation tasks and create a unified dataset ready for analysis.

### Key Takeaways:  

**Data Standardization:**  
- Replace missing values with a custom category (e.g., 'Unknown')
- Convert column values to title case using the `capitalize()` method
- Extract first and last names from a single column using the `split()` method

**Data Feature Engineering:**  
- Create new columns using random integers and calculations
- Use the `np.random.randint()` function to generate random integers

**Data Merging:**  
- Use the `merge()` function to combine datasets
- Ensure matching Customer IDs and Package Types between datasets
- Handle data inconsistencies and capitalization issues
