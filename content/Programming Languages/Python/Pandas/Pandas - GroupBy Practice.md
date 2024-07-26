
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/Group%20By%20Practice.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

Let's practice Pandas using the **Group By** function.

# Import Libraries

``` python
import pandas as pd
import sys

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
```

``` output
Python version 3.11.7 | packaged by Anaconda, Inc. | (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
Pandas version 2.2.1
```

# The Data
---

Here is the csv data if you want to follow along:

``` csv
Date,Symbol,Volume
1/1/2013,A,0
1/2/2013,A,200
1/3/2013,A,1200
1/4/2013,A,1001
1/5/2013,A,1300
1/6/2013,A,1350
3/8/2013,B,500
3/9/2013,B,1150
3/10/2013,B,1180
3/11/2013,B,2000
1/5/2013,C,56600
1/6/2013,C,45000
1/7/2013,C,200
5/20/2013,E,1300
5/21/2013,E,1700
5/22/2013,E,900
5/23/2013,E,2100
5/24/2013,E,8000
5/25/2013,E,12000
5/26/2013,E,1900
5/27/2013,E,1000
5/28/2013,E,1900

```

# Read CSV file

For those who are following along, note that the code below will most likely return an error for you (the file Test_9_17_Python.csv is not on your computer).

Here are two options for you:

- Use the `raw = pd.read_clipboard(sep=',')` method
- Manually create the csv and save it in the same location as this notebook

As you can see we are working with daily trading volume for various stocks over a period of time, from January 1, 2013, to May 28, 2013.

Here are the stock Symbols: A, B, C, and E

``` python
raw = pd.read_csv('Test_9_17_Python.csv')
raw.head()
```

|     | Date     | Symbol | Volume |
| --- | -------- | ------ | ------ |
| 0   | 1/1/2013 | A      | 0      |
| 1   | 1/2/2013 | A      | 200    |
| 2   | 1/3/2013 | A      | 1200   |
| 3   | 1/4/2013 | A      | 1001   |
| 4   | 1/5/2013 | A      | 1300   |

At times I like to make a copy of the original dataframe just in case I have to go back to the original data. Yes, we can just recreate the data, but at times I rather have it handy.

> The copy() function allows you to create a truly independent copy of the data, so changes to the new object won't affect the original

``` python
df = raw.copy()
```

# Fix Date Column

Whenever you import data from basically anywhere, please please check your data types. You want to make sure the data in the correct format before you begin to work with it.

As you can see below, the Date column, which represents our dates, came in as a string. We need to fix this.

``` python
df.info()
```

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 22 entries, 0 to 21
Data columns (total 3 columns):
 #   Column  Non-Null Count  Dtype 
\---  ------  --------------  ----- 
 0   Date    22 non-null     object
 1   Symbol  22 non-null     object
 2   Volume  22 non-null     int64 
dtypes: int64(1), object(2)
memory usage: 660.0+ bytes

#### Pandas to the rescue!

We can automagically convert our dates that are currently represented as strings and converted to datetime objects. Note that it's not always this easy and expect to battle date strings in the future.

``` python
df['Date'] = pd.to_datetime(df['Date'])
```

We now have all our columns looking good.

- Our dates are datetime objects
- The symbols are strings
- The trading volume are integers

``` python
df.dtypes
```

Date      datetime64[ns]
Symbol            object
Volume             int64
dtype: object

# Add a New Column

Let's randomly assign a buy or sell flag to each row in this dataset. This will give us more data to work with and show off some of Pandas GroupBy capabilities.

``` python
# here are our buy and sell options
pool = ['buy','sell']

# create our data in the correct length
# Since we have 2 items in the dataset, I just multiplied half of the dataset by the list. Can you think of a better solution?
pool = pool*int(len(df)/2)

# how many strings did we just create?
print('We created ' + str(len(pool)) + ' strings')

pool
```

``` output 
We created 22 strings

['buy',
 'sell',
 'buy',
 'sell',
 'buy',
 'sell',
 'buy',
 'sell',
 'buy',
 'sell',
 'buy',
 'sell',
 'buy',
 'sell',
 'buy',
 'sell',
 'buy',
 'sell',
 'buy',
 'sell',
 'buy',
 'sell']
```


``` python
# add the new column
df['flag'] = pool

# print top 5 rows
df.head()
```

|     | Date     | Symbol | Volume | flag |
| --- | -------- | ------ | ------ | ---- |
| 0   | 1/1/2013 | A      | 0      | buy  |
| 1   | 1/2/2013 | A      | 200    | sell |
| 2   | 1/3/2013 | A      | 1200   | buy  |
| 3   | 1/4/2013 | A      | 1001   | sell |
| 4   | 1/5/2013 | A      | 1300   | buy  |

# Group by one column

At a high level, the **GroupBy** method will:

- Group your data by one or more columns
- And then perform some action on each group (like calculate the sum, mean, etc.)

In the example below, we are grouping by the column named **Symbol** and then adding all the values found in the **Volume** column for that group.

**As a side note:** If my dataframe has non numeric columns, in this case it's the **flag** column, I have been adding the `numeric_only=True` code to avoid the Pandas warning message. It's kind of annoying.

``` python
# create group object
group = df.groupby('Symbol')

# perform a sum function on the group
group.sum(numeric_only=True)
```

| Symbol | Volume |
| ------ | ------ |
| A      | 5051   |
| B      | 4830   |
| C      | 101800 |
| E      | 30800  |

# Let's do a Deep Dive

When you use the groupby function in Pandas, you are grouping your data by one or more columns. These columns are called the "grouping columns" or "index columns".

In our example above we grouped by the column **Symbol**:

> `group = df.groupby('Symbol')`

- The "Symbol" column becomes the grouping column

When you apply a function to this grouped DataFrame using **apply**, the function is currently applied to both the grouping columns and the data columns.

- in this case, the grouping column is "Symbol"
- in this case, the data column is "Volume"

However, in future versions of Pandas, the grouping columns will be excluded from the operation by default. This means that the function will only be applied to the data columns ("Volume" in this example), and not to the grouping column named "Symbol".

This change is being made to prevent unexpected behavior and to make the apply function more predictable. If you want to include the grouping columns in the operation, you will need to explicitly select them or pass include_groups=True.


``` python
def suma(group):
    ''' perform a sum on the group '''
    return group.sum(numeric_only=True)

group.apply(suma, include_groups=False)
```

| Symbol | Volume |
| ------ | ------ |
| A      | 5051   |
| B      | 4830   |
| C      | 101800 |
| E      | 30800  |

Let's mess around with the **transform** method. Unlike the previous example, transform allows us to keep the original shape of our dataframe.

To avoid any issues with the non-numeric flag column, I excluded it while creating the group object. Yes, I cheated a bit here.

``` python
# create group object
group = df[['Symbol','Volume']].groupby('Symbol')

def suma(group):
    ''' perform a sum on the group '''
    return group.sum(numeric_only=True)

# create a new column
df['addition'] = group.transform(suma)['Volume']
df.head(10)
```

|     | Date      | Symbol | Volume | flag | addition |
| --- | --------- | ------ | ------ | ---- | -------- |
| 0   | 1/1/2013  | A      | 0      | buy  | 5051     |
| 1   | 1/2/2013  | A      | 200    | sell | 5051     |
| 2   | 1/3/2013  | A      | 1200   | buy  | 5051     |
| 3   | 1/4/2013  | A      | 1001   | sell | 5051     |
| 4   | 1/5/2013  | A      | 1300   | buy  | 5051     |
| 5   | 1/6/2013  | A      | 1350   | sell | 5051     |
| 6   | 3/8/2013  | B      | 500    | buy  | 4830     |
| 7   | 3/9/2013  | B      | 1150   | sell | 4830     |
| 8   | 3/10/2013 | B      | 1180   | buy  | 4830     |
| 9   | 3/11/2013 | B      | 2000   | sell | 4830     |


Here we get fancy!

The function below named **test** will do the following:

- filter rows where **flag** is equal to "sell"
- filter rows where **Volume** is greater than 1000

So we only return the rows that meet the two conditions above.


``` python
group = df.groupby('Symbol')

def test(group):
    mask1 = group.apply(lambda x: x.iloc[2]=='sell' and x.iloc[1]>1000, axis=1)
    return group[mask1]

group.apply(test, include_groups=False)
```


|            |     | Date       | Volume | flag | addition |
| ---------- | --- | ---------- | ------ | ---- | -------- |
| **Symbol** |     |            |        |      |          |
| A          | 3   | 2013-01-04 | 1001   | sell | 5051     |
|            | 5   | 2013-01-06 | 1350   | sell | 5051     |
| B          | 7   | 2013-03-09 | 1150   | sell | 4830     |
|            | 9   | 2013-03-11 | 2000   | sell | 4830     |
| C          | 11  | 2013-01-06 | 45000  | sell | 101800   |
| E          | 13  | 2013-05-20 | 1300   | sell | 30800    |
|            | 17  | 2013-05-24 | 8000   | sell | 30800    |
|            | 19  | 2013-05-26 | 1900   | sell | 30800    |
|            | 21  | 2013-05-28 | 1900   | sell | 30800    |

# Group by two columns

The examples below show you how to group by multiple columns.

We are not going to go through new material, we are just grouping by 2 columns. You got this!

``` python
# create group object, remember to pass a list when grouping by multiple columns
group = df.groupby(['Symbol', 'flag'])

# perform a sum function on the group
group.sum(numeric_only=True)
```

|            |          | Volume | addition |
| ---------- | -------- | ------ | -------- |
| **Symbol** | **flag** |        |          |
| A          | buy      | 2500   | 15153    |
|            | sell     | 2551   | 15153    |
| B          | buy      | 1680   | 9660     |
|            | sell     | 3150   | 9660     |
| C          | buy      | 56800  | 203600   |
|            | sell     | 45000  | 101800   |
| E          | buy      | 16800  | 123200   |
|            | sell     | 14000  | 154000   |


``` python
# apply a function to the multi column group
def suma(group):
    return group['Volume'].sum(numeric_only=True)

group.apply(suma, include_groups=False)
```


``` output
Symbol  flag
A       buy      2500
        sell     2551
B       buy      1680
        sell     3150
C       buy     56800
        sell    45000
E       buy     16800
        sell    14000
dtype: int64
```


``` python
# use transform
group = df[['Symbol','Volume','flag']].groupby(['Symbol', 'flag'])

def suma(group):
    return group.sum(numeric_only=True)

df['addition'] = group.transform(suma)['Volume']
df.head()
```


|     | Date       | Symbol | Volume | flag | addition |
| --- | ---------- | ------ | ------ | ---- | -------- |
| 0   | 2013-01-01 | A      | 0      | buy  | 2500     |
| 1   | 2013-01-02 | A      | 200    | sell | 2551     |
| 2   | 2013-01-03 | A      | 1200   | buy  | 2500     |
| 3   | 2013-01-04 | A      | 1001   | sell | 2551     |
| 4   | 2013-01-05 | A      | 1300   | buy  | 2500     |


``` python
# filter away
group = df.groupby(['Symbol', 'flag'])

def test(group):
    mask1 = group.apply(lambda x: x.iloc[1]>1000, axis=1)
    return group[mask1]

group.apply(test)
```


|            |          |     | Date       | Volume | addition |
| ---------- | -------- | --- | ---------- | ------ | -------- |
| **Symbol** | **flag** |     |            |        |          |
| A          | buy      | 2   | 2013-01-03 | 1200   | 2500     |
|            |          | 4   | 2013-01-05 | 1300   | 2500     |
|            | sell     | 3   | 2013-01-04 | 1001   | 2551     |
|            |          | 5   | 2013-01-06 | 1350   | 2551     |
| B          | buy      | 8   | 2013-03-10 | 1180   | 1680     |
|            | sell     | 7   | 2013-03-09 | 1150   | 3150     |
|            |          | 9   | 2013-03-11 | 2000   | 3150     |
| C          | buy      | 10  | 2013-01-05 | 56600  | 56800    |
|            | sell     | 11  | 2013-01-06 | 45000  | 45000    |
| E          | buy      | 14  | 2013-05-21 | 1700   | 16800    |
|            |          | 16  | 2013-05-23 | 2100   | 16800    |
|            |          | 18  | 2013-05-25 | 12000  | 16800    |
|            | sell     | 13  | 2013-05-20 | 1300   | 14000    |
|            |          | 17  | 2013-05-24 | 8000   | 14000    |
|            |          | 19  | 2013-05-26 | 1900   | 14000    |
|            |          | 21  | 2013-05-28 | 1900   | 14000    |
