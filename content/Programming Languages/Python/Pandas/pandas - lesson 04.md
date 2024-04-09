You can also find this code on nbviewer.
- [Lesson 04](https://nbviewer.org/url/bitbucket.org/hrojas/learn-pandas/raw/master/lessons/04%20-%20Lesson.ipynb)

``` python
#!/usr/bin/env python
# coding: utf-8

# Lesson 4

# In this lesson were going to go back to the basics. We will be working with a small data set so that you can easily understand what I am trying to explain. We will be adding columns, deleting columns, and slicing the data many different ways. Enjoy!

# Import libraries
import pandas as pd
import sys

print('Python version ' + sys.version)
print('Pandas version: ' + pd.__version__)

# Our small data set
d = [0,1,2,3,4,5,6,7,8,9]

# Create dataframe
df = pd.DataFrame(d)
df

# Lets change the name of the column
df.columns = ['Rev']
df

# Lets add a column
df['NewCol'] = 5
df

# Lets modify our new column
df['NewCol'] = df['NewCol'] + 1
df

# We can delete columns
del df['NewCol']
df

# Lets add a couple of columns
df['test'] = 3
df['col'] = df['Rev']
df

# If we wanted, we could change the name of the index
i = ['a','b','c','d','e','f','g','h','i','j']
df.index = i
df

# We can now start to select pieces of the dataframe using ***loc***.
df.loc['a']

# df.loc[inclusive:inclusive]
df.loc['a':'d']

# df.iloc[inclusive:exclusive]
# Note: .iloc is strictly integer position based. It is available from [version 0.11.0] (http://pandas.pydata.org/pandas-docs/stable/whatsnew.html#v0-11-0-april-22-2013) 
df.iloc[0:3]

# We can also select using the column name.
df['Rev']

df[['Rev', 'test']]

# df.ix[rows,columns]
# replaces the deprecated ix function
#df.ix[0:3,'Rev']
df.loc[df.index[0:3],'Rev']

# replaces the deprecated ix function
#df.ix[5:,'col']
df.loc[df.index[5:],'col']

# replaces the deprecated ix function
#df.ix[:3,['col', 'test']]
df.loc[df.index[:3],['col', 'test']]

# There is also some handy function to select the top and bottom records of a dataframe.

# Select top N number of records (default = 5)
df.head()

# Select bottom N number of records (default = 5)
df.tail()
```


