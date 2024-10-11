
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/movie_madness.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

**Description:** 
You are a data analyst for a movie streaming service. You have been tasked with analyzing a dataset of movie ratings to determine which genres are the most popular among users.  

The dataset contains the following columns:
- **user_id:** Unique identifier for each user
- **movie_id:** Unique identifier for each movie
- **rating:** Rating given by the user to the movie (on a scale of 1-5)
- **genre:** Genre of the movie (e.g. Action, Comedy, Drama, etc.)

**Your task is to:**  
- Load the dataset into a Pandas DataFrame
- Group the data by genre and calculate the average rating for each genre
- Sort the results in descending order by average rating

**Data:**  
You can use the following sample data to get started:  
```
user_id,movie_id,rating,genre
1,101,4,Action
1,102,3,Comedy
2,101,5,Action
2,103,4,Drama
3,102,2,Comedy
3,104,5,Action
```

```python
# import libraries
import pandas as pd
import sys

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
```

    Python version 3.11.7 | packaged by Anaconda, Inc. | (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
    Pandas version 2.2.1
    

```python
# let's try to copy the data using the clipboard
df = pd.read_clipboard(sep=",")
df
```

|     | user_id | movie_id | rating | genre  |
| --- | ------- | -------- | ------ | ------ |
| 0   | 1       | 101      | 4      | Action |
| 1   | 1       | 102      | 3      | Comedy |
| 2   | 2       | 101      | 5      | Action |
| 3   | 2       | 103      | 4      | Drama  |
| 4   | 3       | 102      | 2      | Comedy |
| 5   | 3       | 104      | 5      | Action |

```python
# check the data types
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 6 entries, 0 to 5
    Data columns (total 4 columns):
     #   Column    Non-Null Count  Dtype 
    ---  ------    --------------  ----- 
     0   user_id   6 non-null      int64 
     1   movie_id  6 non-null      int64 
     2   rating    6 non-null      int64 
     3   genre     6 non-null      object
    dtypes: int64(3), object(1)
    memory usage: 324.0+ bytes
    


```python
# create groupby object
group = df.groupby('genre')

# calculate average rating
avg = group['rating'].mean()
avg
```

    genre
    Action    4.666667
    Comedy    2.500000
    Drama     4.000000
    Name: rating, dtype: float64


I decided to place it all in one line. Yes, it is a bit ugly.

Here is what I did:  
- I decided to merge the Series that contains the average ratings with the original dataframe via the column named genre
- I renamed the Series so the column names were clear
- I finally sorted the values descending 

```python
df.set_index('genre').merge(avg.rename('average_rating'), on='genre').sort_values('average_rating', ascending=False)
```

|        | user_id | movie_id | rating | average_rating |
| ------ | ------- | -------- | ------ | -------------- |
| genre  |         |          |        |                |
| Action | 1       | 101      | 4      | 4.666667       |
| Action | 2       | 101      | 5      | 4.666667       |
| Action | 3       | 104      | 5      | 4.666667       |
| Drama  | 2       | 103      | 4      | 4.000000       |
| Comedy | 1       | 102      | 3      | 2.500000       |
| Comedy | 3       | 102      | 2      | 2.500000       |

If all you needed to see was the averages...

```python
avg.sort_values(ascending=False)
```

    genre
    Action    4.666667
    Drama     4.000000
    Comedy    2.500000
    Name: rating, dtype: float64


# Summary:
This tutorial guided you through the analysis of a movie ratings dataset using Pandas. It covered loading data, grouping by genre, calculating average ratings, merging data, and sorting results.

### Key Takeaways:
- How to load data from a clipboard into a Pandas DataFrame using `pd.read_clipboard()`
- Understanding data types using `df.info()`
- Grouping data by a column (genre) using `df.groupby()`
- Calculating the average rating for each group using `group['rating'].mean()`
- Merging data from a Series into the original DataFrame using `df.merge()` or `df.set_index().merge()`
- Renaming columns using `rename()`
- Sorting data in descending order using `sort_values()`












