You can also find this code on nbviewer.
- [Lesson 10](https://nbviewer.org/url/bitbucket.org/hrojas/learn-pandas/raw/master/lessons/10%20-%20Lesson.ipynb)

``` python
#!/usr/bin/env python
# coding: utf-8

# # Lesson 10

# * From DataFrame to Excel  
# * From Excel to DataFrame  
# * From DataFrame to JSON  
# * From JSON to DataFrame  

import pandas as pd
import sys

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)

# From DataFrame to Excel

# Create DataFrame
d = [1,2,3,4,5,6,7,8,9]
df = pd.DataFrame(d, columns = ['Number'])
df

# Export to Excel
df.to_excel('Datafiles/Lesson10.xlsx', sheet_name = 'testing', index = False)
print('Done')

# From Excel to DataFrame

# Path to excel file
# Your path will be different, please modify the path below.
location = r'Datafiles/Lesson10.xlsx'

# Parse the excel file
df = pd.read_excel(location, 0)
df.head()

df.dtypes

df.tail()

# From DataFrame to JSON
df.to_json('Datafiles/Lesson10.json')
print('Done')

# From JSON to DataFrame

# Your path will be different, please modify the path below.
jsonloc = r'Datafiles/Lesson10.json'

# read json file
df2 = pd.read_json(jsonloc)
df2

df2.dtypes
```


