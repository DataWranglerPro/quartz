You can also find this code on nbviewer.
- [Lesson 06](https://nbviewer.org/url/bitbucket.org/hrojas/learn-pandas/raw/master/lessons/06%20-%20Lesson.ipynb)

``` python
#!/usr/bin/env python
# coding: utf-8

# Lesson 6

# > Lets take a look at the ***groupby*** function.

# Import libraries
import pandas as pd
import sys

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)

# Our small data set
d = {'one':[1,1,1,1,1],
     'two':[2,2,2,2,2],
     'letter':['a','a','b','b','c']}

# Create dataframe
df = pd.DataFrame(d)
df

# Create group object
one = df.groupby('letter')

# Apply sum function
one.sum()

letterone = df.groupby(['letter','one']).sum()
letterone

letterone.index

# You may want to ***not*** have the columns you are grouping by become your index, this can be easily achieved as shown below.
letterone = df.groupby(['letter','one'], as_index=False).sum()
letterone

letterone.index
```


