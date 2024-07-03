
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/using_data_to_optimize_logistics.ipynb), offering an alternative platform for your learning convenience.
> - [Pandas Ninja](https://hedaro.gumroad.com/l/jVeRh): Take your skills to the next level with comprehensive Jupyter Notebook tutorials covering dates, group by, plotting, pivot tables, and more. Includes specialized tutorials for Excel and SQL developers, helping you master data analysis with Pandas.

### Description:   
Your friend is a data analyst for a large online education platform. She needs your help to analyze student performance data and identify trends in student engagement. She provides you with a dataset containing student scores, ages, and study hours.  

### Tasks:  
- **Score Binning:** Use `pd.cut` to bin student scores into three categories: low (0-40), medium (41-70), and high (71-100). Calculate the count of students in each bin.
- **Age Quantiles:** Use `pd.qcut` to divide students into four age groups based on quantiles (25th, 50th, 75th percentiles). Calculate the average score for each age group.
- **Study Hour Categories:** Use `pd.cut` to categorize study hours into three groups: low (0-5 hours), medium (6-10 hours), and high (11+ hours). Calculate the average score for each study hour category.

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

This dataset represents a sample of student performance and engagement metrics, providing a snapshot of their academic progress and learning habits.  

### Columns:  
- **Score:** The student's score on a test (0-100)
- **Age:** The student's age (18-30)
- **Study Hours:** The number of hours the student studied (0-20)

```python
# set the seed
np.random.seed(0)

data = {
    'Score': np.random.uniform(0, 100, size=1000),
    'Age': np.random.randint(18, 30, size=1000),
    'Study Hours': np.random.uniform(0, 20, size=1000)
}

df = pd.DataFrame(data)
df.head()
```

|     | Score     | Age | Study Hours |
| --- | --------- | --- | ----------- |
| 0   | 54.881350 | 19  | 19.013202   |
| 1   | 71.518937 | 24  | 12.036051   |
| 2   | 60.276338 | 28  | 16.291702   |
| 3   | 54.488318 | 23  | 19.747667   |
| 4   | 42.365480 | 22  | 15.749032   |

# Score Binning:  

Use `pd.cut` to bin student scores into three categories and calculate the count of students in each bin.  
- low (0-40)
- medium (41-70)
- high (71-100) 

`pd.cut` is a Pandas function that allows you to bin or categorize numeric data into intervals or categories. It's useful when you want to group continuous data into discrete categories.  

### How it works:  
You pass in a series (a column of data) and specify the bins (intervals) you want to use. `pd.cut` returns a new series with the bin labels assigned to each value.  

### When to use it:
- When you want to group continuous data into categories (e.g., age groups, score ranges) 
- When you want to simplify complex data into more manageable chunks  
- When you want to create a new feature based on existing numerical data

### Simple example:  
Suppose we have a series of exam scores:  
``` Python
scores = pd.Series([80, 70, 90, 60, 75])
```

We can use `pd.cut` to bin the scores into three categories: low (0-70), medium (71-90), and high (91-100)  
``` python
bins = [0, 70, 90, 100]  
labels = ['low', 'medium', 'high']  
binned_scores = pd.cut(scores, bins=bins, labels=labels)  
print(binned_scores)  
```

**Output:** 
``` python
0    medium
1       low
2    medium
3       low
4    medium
dtype: category
Categories (3, object): ['low' < 'medium' < 'high']
```

**Bin Ranges:**  
(0 - 70] -> low  
(70 - 90] -> medium  
(90 - 100] -> high  


Let us go over the output above:  
- The first data point is 80, this number falls under the medium category (70-90]
- The second data point is 70, this number falls under the low category (0-70]
- The third data point is 90, this number falls under the medium category (70-90]
- The fourth data point is 60, this number falls under the low category (0-70]
- The fifth data point is 75, this number falls under the medium category (70-90]

```python
# create bins for the low (0-40), medium (41-70), and high (71-100) categories
bins = [0, 40, 70, 100]  

# labels for the three categories
labels = ['low', 'medium', 'high']  

# bin it up!
binned_scores = pd.cut(df['Score'], bins=bins, labels=labels)

# here we get a frequency count of the categories
binned_scores.value_counts()
```

    Score
    low       415
    medium    294
    high      291
    Name: count, dtype: int64



Here is a handy loop to visualize the bins.

```python
# print the bin ranges
print("\nBin Ranges:")
for i in range(len(bins)-1):
    print(f"({bins[i]} - {bins[i+1]}] -> {labels[i]}")
```
    
    Bin Ranges:
    (0 - 40] -> low
    (40 - 70] -> medium
    (70 - 100] -> high
    

<h3 align="middle">pd.cut versus pd.qcut</h3> 

<h5 align="middle">In the next task we will be using pd.qcut, to avoid confusion with pd.cut, below is a table comparing the two methods.</h5> 

| **Feature**           | **pd.cut**               | **pd.qcut**                      |
| --------------------- | ------------------------ | -------------------------------- |
| **Bin Edges**         | Fixed, user-specified    | Dynamic, based on quantiles      |
| **Bin Specification** | Manual, explicit         | Automatic, based on quantiles    |
| **Number of Bins**    | User-specified           | User-specified (q parameter)     |
| **Bin Size**          | Variable                 | Equal-sized buckets              |
| **Use Case**          | Specific bin edges known | Equal-sized buckets desired      |
| **Quantiles**         | Not directly related     | Directly related, uses quantiles |

# Age Quantiles:  

Use `pd.qcut` to divide students into four age groups based on quantiles (25th, 50th, 75th percentiles). Calculate the average score for each age group.  

```python
# bin into 4 groups
binned_ages = pd.qcut(df['Age'], q=4, labels=['0-25%', '26%-50%', '51%-75%', '76%+'], retbins=True)

# add it to the dataframe
df['binned_ages'] = binned_ages[0]

# create group object
group = df.groupby('binned_ages', observed=True)

# calculate the average score for the group
group.mean(numeric_only=True)['Score']
```

    binned_ages
    0-25%      48.435515
    26%-50%    52.325292
    51%-75%    48.789424
    76%+       49.102480
    Name: Score, dtype: float64


We can see the bin ranges used.

```python
binned_ages[1]
```

    array([18., 21., 24., 27., 29.])


Below are a couple ways to get the quantiles, just in case you are curious.

```python
df['Age'].describe()
```

    count    1000.000000
    mean       23.748000
    std         3.497818
    min        18.000000
    25%        21.000000
    50%        24.000000
    75%        27.000000
    max        29.000000
    Name: Age, dtype: float64


```python
df['Age'].quantile([0.25, 0.5, 0.75])
```

    0.25    21.0
    0.50    24.0
    0.75    27.0
    Name: Age, dtype: float64


# Study Hour Categories:  

Use `pd.cut` to categorize study hours into three groups: low (0-5 hours), medium (6-10 hours), and high (11+ hours). Calculate the average score for each study hour category.  

---
Let us talk about the `df.groupby` parameter named observed.  

I needed to add the observed parameter and set it to True to avoid a Pandas warning I was getting. Now the question is, why was I getting this warning? I have used the `df.groupby` method many times, but don't recall seeing this warning before.  

```FutureWarning: The default of observed=False is deprecated and will be changed to True in a future version of pandas. Pass observed=False to retain current behavior or observed=True to adopt the future default and silence this warning.```

I was getting this warning because I was grouping by the column named binned_ages, which has a datatype of category.

Categoricals have a special property called "observed" which determines whether the categories should be considered as part of the data's index.  

When you group data using a Categorical column, Pandas uses the categories as the grouping keys. If the categories are not already part of the data's index, Pandas will create a new index based on the categories. This is where the "observed" parameter comes in.  

- If **observed=False** (the current default), Pandas will treat the categories as "unobserved" variables, meaning they won't be considered part of the data's index. This is useful when you want to group data based on a Categorical column without modifying the original index.
- If **observed=True**, Pandas will treat the categories as part of the data's index, which can affect the behavior of certain operations, like merging or joining dataframes.

So, the warning is only relevant when you're grouping data using a Categorical column, because that's when the "observed" parameter has a significant impact on the behavior of the groupby operation. If you're grouping data using non-Categorical columns (e.g., numerical or string columns), the "observed" parameter doesn't have any effect, and the warning is not applicable. 

```python
# create bins
bins = [0, 5, 10, 20]  

# labels for the three categories
labels = ['low', 'medium', 'high']  

# bin it up!
binned_hours = pd.cut(df['Study Hours'], bins=bins, labels=labels)

# add it to the dataframe
df['binned_hours'] = binned_hours

# create group object
group = df.groupby('binned_hours', observed=True)

# calculate the average score for the group
group.mean(numeric_only=True)['Score']
```

    binned_hours
    low       48.110535
    medium    49.040285
    high      50.585352
    Name: Score, dtype: float64

### Summary:  
The tutorial analyzed student performance data to identify trends in engagement, covering score binning, age quantiles, and study hour categories. It demonstrated the use of Pandas functions pd.cut and pd.qcut for categorizing and binning data, and calculating average scores.

### You learned:
- How to bin data into categories using pd.cut
- How to divide data into quantiles using pd.qcut
- How to group data and calculate average scores for each group
- The difference between pd.cut and pd.qcut
- How to use the observed parameter in df.groupby when working with Categorical columns
