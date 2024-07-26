
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/05c8f4c8349030d0b13dca82d29535ad884e5f81/content/Assets/notebooks/How_to_Create_a_Pandas_DataFrame.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

The most important data structure is the ***Pandas DataFrame*** (notice the Camel Case, more on this later). It will also be one of the most commonly used terms when dealing with this library. At a high level, we as analysts, as developers, need to get our data inside a dataframe.

> It is when we get our data inside this data structure that we will be able to harness the power of Pandas

The steps below are meant to be for someone relatively **new to the Pandas world**. It shows you a few ways to quickly create dataframes. Get your coffee ready.

``` python
# import libraries
import pandas as pd
import sys
```

I like to start by sharing the version of Python and the relevant libraries I will be using for this tutorial. We know that different versions of the same library may behave differently. So to avoid issues realted to different library or Python versions, I make it very clear what I used in this notebook. So instead of banging your head for hours, you could test to see if a different version of Pandas or Python is causing issues for you.

``` python
print('Python: ' + sys.version.split('|')[0])
print('Pandas: ' + pd.__version__)
```

``` output
Python: 3.11.7 
Pandas: 2.2.1
```

## Python Lists

_**Python lists**_ are very commonly used. They are essentially arrays that can hold any kind of data. We can put strings or numbers inside lists. Let's make a simple one and see how they work.

We start by reading a variable named _**d**_. Now lists start and end with brackets. If you see brackets, most likely you are dealing with a list. Inside our list, we placed 4 numbers. Pretty easy.

``` python
d = [0,1,2,3]
d
```

``` output
[0, 1, 2, 3]
```

We can be extra sure by asking Python what kind of object is the variable d. We can also get the length of the list.

``` python
print(type(d))
print(len(d))
```

``` output
<class 'list'>
4
```

So how do we get this list into a dataframe? Like I mentioned earlier, if you cannot get your data into a dataframe, then there isn't much Pandas can do for you.

We start by creating a variable named _**df**_. In many examples, df is a very common way to name your variables that hold a dataframe.

> And if you haven't figured it out, df is short for dataframe.

==**IMPORTANT:**== Note that the _**DataFrame**_ method is camel case. Knowing this may save you some frustration.

The key parameter is called _**data**_ and this is where you are going to place the list we created a few seconds ago. After this is done, all you have to do is print the dataframe.

``` python
df = pd.DataFrame(data=d)
df
```

|       |   0 |
| :---- | --: |
| **0** |   0 |
| **1** |   1 |
| **2** |   2 |
| **3** |   3 |

## Labeling DataFrame Columns

Did you notice an issue we have with our dataframe? Yes, the column name is zero. We only have one column. The other column with no column name is not really a column. This is called the index. It is similar to the row numbers in an Excel file. It is also similar to identity columns in a database table. One thing to keep in mind is that this column does not have to be unique. This won't come into play in this lesson, but just sharing for awareness.

> Every dataframe will come with an index

The dataframe method has a _**columns**_ parameter and this is the trick to getting your columns named.

As you can see below, not only does the HTML table look much nicer, but it will make your readers of your future notebooks very happy. I like to pass a Python list to the columns parameter. If you have more than one column, you can create a list of multiple column names.

``` python
df = pd.DataFrame(data=d, columns=['Revenue'])
df
```

|       | Revenue |
| :---- | ------: |
| **0** |       0 |
| **1** |       1 |
| **2** |       2 |
| **3** |       3 |
## Python Dictionary

The _**Python dictionary**_ is another commonly used object. It is not as common as the Python list, but you will see it a lot. The advantage of using a dictionary is that it lets us label our columns ahead of time. This means we can skip the step of setting the columns parameter in Pandas.

If you see curly brackets, then you may be looking at a Python dictionary. After the initial curly bracket, you pass in a string. This string will represent the column name of your dataframe. Then we use a colon and then I like to pass a list. See how lists are everywhere? We finish things up by closing the parenthesis.

``` python
d = {'Revenue':[5,6,7]}
d
```

``` output
{'Revenue': [5, 6, 7]}
```

For the paranoid like myself. We can check the type and size as shown below. Note that we did not get three for the length as we were not counting the list but the dictionary. We only have one column so the length is one. Get it?

``` python
print(type(d))
print(len(d))
```

``` output
<class 'dict'>
1
```

## Dict to Dataframe

Luckily most of the steps to get a dict into a dataframe we have already done. It is actually even easier since we are going to ignore the columns parameter. Pandas is smart enough to know the column names are already provided in the Python dictionary.

I didn't mention it before, but _**pd**_ is the alias for the Pandas library. This alias is allowing us to reach into the Pandas library and gives us access to all the methods and functions Pandas has to offer.

``` python
df = pd.DataFrame(d)
df
```

|       | Revenue |
| :---- | ------: |
| **0** |       5 |
| **1** |       6 |
| **2** |       7 |

What about dictionaries with multiple columns? Can we do that? Yes and yes! All we have to do is separate each element in the dictionary. Remember to follow the same format. Name of column, then colon, then a Python list.

``` python
d = {'Revenue':[5,6,7],
     'Cost':[5.0,6.1,7.2]}
d
```

``` output
{'Revenue': [5, 6, 7], 'Cost': [5.0, 6.1, 7.2]}
```

Did you notice that? When I started creating dataframes, I noticed an odd default behavior with the ordering of the columns. The order I placed columns in the Python dictionary did not always match with the dataframe column order. This was a bit annoying but it's something you are going to have to work with.

The good news is that if you have Python version 3.6+ and Pandas version >= 0.23.0 this will all be fixed. Below taken from the Pandas website:

> Until Python 3.6, dicts in Python had no formally defined ordering. For Python version 3.6 and later, dicts are ordered by insertion order, see PEP 468. Pandas will use the dict’s insertion order, when creating a Series or DataFrame from a dict and you’re using Python version 3.6 or higher.

``` python
pd.DataFrame(d)
```

|       | Revenue | Cost |
| :---- | ------: | ---- |
| **0** |       5 | 5.0  |
| **1** |       6 | 6.1  |
| **2** |       7 | 7.2  |

  
A work around is to use the columns parameter and force your columns to be ordered a certain way. I know I mentioned we did not need to use the columns parameter with dictionaries but I guess I lied. If order matters to you then you might as well use it.

``` python
pd.DataFrame(d, columns=['Revenue','Cost'])
```

|       | Revenue | Cost |
| :---- | ------: | ---- |
| **0** |       5 | 5.0  |
| **1** |       6 | 6.1  |
| **2** |       7 | 7.2  |

