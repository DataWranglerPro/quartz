You can also find this code on nbviewer.
- [Lesson 05](https://nbviewer.org/url/bitbucket.org/hrojas/learn-pandas/raw/master/lessons/05%20-%20Lesson.ipynb)

``` python
#!/usr/bin/env python
# coding: utf-8

# Lesson 5

# > We will be taking a brief look at the ***stack*** and ***unstack*** functions. 

# Import libraries
import pandas as pd
import sys

print('Python version ' + sys.version)
print('Pandas version: ' + pd.__version__)

# Our small data set
d = {'one':[1,1],'two':[2,2]}
i = ['a','b']

# Create dataframe
df = pd.DataFrame(data = d, index = i)
df

df.index

# Bring the columns and place them in the index
stack = df.stack()
stack

# The index now includes the column names
stack.index

unstack = df.unstack()
unstack

unstack.index

# We can also flip the column names with the index using the ***T*** (transpose) function.
transpose = df.T
transpose

transpose.index
```


