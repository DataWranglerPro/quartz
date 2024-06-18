
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/d53f63a9c211688e03ee449f588aa11ed1d0fa70/content/Assets/notebooks/How_to_Sort_in_Pandas.ipynb), offering an alternative platform for your learning convenience.
> - [Pandas Ninja](https://hedaro.gumroad.com/l/jVeRh): Take your skills to the next level with comprehensive Jupyter Notebook tutorials covering dates, group by, plotting, pivot tables, and more. Includes specialized tutorials for Excel and SQL developers, helping you master data analysis with Pandas.


This Notebook will cover all the techniques to quickly _**sort your dataframe in Pandas**_. Whether you are looking to sort one or multiple columns. Or whether you are looking to order your data in an _**ascending**_ or _**descending**_ fashion, I have you covered.

Let's start by importing our libraries.

``` python
import pandas as pd
import sys
```

Below is the version of Python and Pandas I am currently on.

``` python
print('Python: ' + sys.version.split('|')[0])
print('Pandas: ' + pd.__version__)
```

``` output
Python: 3.11.7 
Pandas: 2.2.1
```

Let's get a dataframe up and running. We will be using a Python dictionary to generate some dummy data for this lesson. If you are new to the Pandas world and are not yet comfortable with dataframes, please take a look at my post, [how to create a dataframe](https://hedaro.com/Programming-Languages/Python/Pandas/Pandas---Create-DataFrame) before you continue this lesson.

After we print the dataframe, we will get two columns. The Rev columns are short for Revenue. So we have essentially two sets of revenue numbers.

``` python
df = pd.DataFrame({'Rev':[234,345,7,345,3],
                   'Rev2':[345,67,3,88,4]})

df
```


|     |Rev|Rev2|
|---|---|---|
| 0   |234|345|
| 1   |345|67|
| 2   |7|3|
| 3   |345|88|
| 4   |3|4|

## Pandas Sort by Column

If you are familiar with Pandas, you will notice the dataframe method called _**sort**_ is no longer available. I believe sort was deprecated back on Pandas version 0.17 and was replaced with _**sort_values**_.

sort_values requires you to pass in the _**by**_ parameter. This parameter is used to tell Pandas by which column(s) do you want to order by.

> The good news is that we can pass in a single string or a list of strings that represent column names.

If you wanted to _**sort by the Rev column**_, you would simply pass in a string named 'Rev' as shown below. If you look at the index of the dataframe, you will notice it has changed. Instead of showing 0, 1, 2, 3, and 4, it shows a different order. And if you haven't picked up the pattern, the data has been sorted ascending (lowest to largest).

``` python
df.sort_values('Rev')
```

|     | Rev | Rev2 |
| --- | --- | ---- |
| 4   | 3   | 4    |
| 2   | 7   | 3    |
| 0   | 234 | 345  |
| 1   | 345 | 67   |
| 3   | 345 | 88   |

Pandas sorts your data ascending by default. But we can use the parameter called _**ascending**_ to order the data from largest to smallest or descending.

- ascending = _**True**_ = smallest to largest
- ascending = _**False**_ = largest to smallest

``` python
df.sort_values('Rev', ascending = False)
```

|     | Rev | Rev2 |
| --- | --- | ---- |
| 1   | 345 | 67   |
| 3   | 345 | 88   |
| 0   | 234 | 345  |
| 2   | 7   | 3    |
| 4   | 3   | 4    |

A cool trick you are also able to do is set the ascending parameter to equal a boolean value. We can use zeros and ones instead of True or False.

- ascending = _**1**_ = smallest to largest
- ascending = _**0**_ = largest to smallest

It may not make much difference to use 0/1 vs True/False but I just wanted to make you aware of the possibility.

``` python
df.sort_values('Rev', ascending = 1)
```

|     | Rev | Rev2 |
| --- | --- | ---- |
| 4   | 3   | 4    |
| 2   | 7   | 3    |
| 0   | 234 | 345  |
| 1   | 345 | 67   |
| 3   | 345 | 88   |

## Sorting with Multiple Columns

We can apply the same technique we have been going over but instead of passing in a string, we will need to pass in a Python list.

Let's start with the same example as above but let's pass in the single string as a list. Did you see a difference? No, there wasn't.

``` python
df.sort_values(['Rev'])
```

|     | Rev | Rev2 |
| --- | --- | ---- |
| 4   | 3   | 4    |
| 2   | 7   | 3    |
| 0   | 234 | 345  |
| 1   | 345 | 67   |
| 3   | 345 | 88   |

This means we can _**pass in multiple columns**_ and Pandas will sort by the first and then sort by the second. Yes, I know that adding the second columns didn't really do much for us. But fear not, Pandas really is sorting both columns. The next example will clear things up.

``` python
df.sort_values(['Rev', 'Rev2'], ascending=[False,False])
```

|     | Rev | Rev2 |
| --- | --- | ---- |
| 3   | 345 | 88   |
| 1   | 345 | 67   |
| 0   | 234 | 345  |
| 2   | 7   | 3    |
| 4   | 3   | 4    |

Notice that the first column as a value that is repeated twice. Yes, it is the value 345. The example above has the second column (Rev2) with values 88 and then 67. Pandas is sorting this column descending.

If we change the sort order on Rev2, you will get different results. We see that we now have 67 followed by 88.

> If the first column (Rev) only had unique numbers, then ordering by the second column would be useless

But since the value 345 was there twice. It really didn't matter the order they were placed by Pandas since they are equivalent. So when we changed the sort order for Rev2, we saw a change. Bam! Did you get it? I didn't lose you, right?

``` python
df.sort_values(['Rev', 'Rev2'], ascending=[False,True])
```

|     | Rev | Rev2 |
| --- | --- | ---- |
| 1   | 345 | 67   |
| 3   | 345 | 88   |
| 0   | 234 | 345  |
| 2   | 7   | 3    |
| 4   | 3   | 4    |

## Sorting on a Different Axis

Let's say we have a dataframe shaped in a slightly different way. We can achieve this by transposing our current dataframe. A dataframe shaped like the one below will not work like the example we just went over.

> df.T.sort_values('Rev', ascending = 1) _**<< This code will fail <<**_

The reason this will not work is because there is no longer a column called Rev. The columns are now 0, 1, 2, 3, and 4.

``` python
df.T
```

|          | 0   | 1   | 2   | 3   | 4   |
| -------- | --- | --- | --- | --- | --- |
| **Rev**  | 234 | 345 | 7   | 345 | 3   |
| **Rev2** | 345 | 67  | 3   | 88  | 4   |

As you have imagined, Pandas has a solution for us. And the saving grace is the parameter called _**axis**_. by setting this parameter to 1, Pandas will sort based on the row names instead of the column names.

The code below is sorting the data ascending (small to large) but it is sorting the numbers from left to right. Earlier in this lesson we were sorting the data vertically. Remember?

``` python
df.T.sort_values('Rev', ascending = 1, axis=1)
```

|          | 4   | 2   | 0   | 1   | 3   |
| -------- | --- | --- | --- | --- | --- |
| **Rev**  | 3   | 7   | 234 | 345 | 345 |
| **Rev2** | 4   | 3   | 345 | 67  | 88  |

## Pandas Sort Series

There was also an _**order**_ method I used to use but this has also been deprecated and we can simply use _**sort_values**_ instead. In an older version of Pandas order was used for a Pandas _**series**_ since sort only worked for a dataframe. but like I mentioned, sort_values will work for both a dataframe and a series object.

Don't forget to share this post if you know someone who might enjoy the read.















