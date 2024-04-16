You can also find this code on nbviewer.
- [Lesson 11](https://nbviewer.org/url/bitbucket.org/hrojas/learn-pandas/raw/master/lessons/11%20-%20Lesson.ipynb)

``` python
#!/usr/bin/env python
# coding: utf-8

# # Lesson 11

# > Grab data from multiple excel files and merge them into a single dataframe.
import pandas as pd
import matplotlib
import os
import sys
get_ipython().run_line_magic('matplotlib', 'inline')

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)

# Create 3 excel files

# Create DataFrame
d = {'Channel':[1], 'Number':[255]}
df = pd.DataFrame(d)
df

# Export to Excel
df.to_excel('Datafiles/test1.xlsx', sheet_name = 'test1', index = False)
df.to_excel('Datafiles/test2.xlsx', sheet_name = 'test2', index = False)
df.to_excel('Datafiles/test3.xlsx', sheet_name = 'test3', index = False)
print('Done')

# Place all three Excel files into a DataFrame
# Get a list of file names but make sure there are no other excel files present in the folder.

# List to hold file names
FileNames = []

# Your path will be different, please modify the path below.
os.chdir(r"Datafiles/")

# Find any file that ends with ".xlsx"
for files in os.listdir("."):
    if files.endswith(".xlsx") and files in ['test1.xlsx', 'test2.xlsx', 'test3.xlsx']:
        FileNames.append(files)
        
FileNames

# Create a function to process all of the excel files.
def GetFile(fnombre):

    # Path to excel file
    # Your path will be different, please modify the path below.
    location = r'../DataFiles/' + fnombre
    
    # Parse the excel file
    # 0 = first sheet
    df = pd.read_excel(location, 0)
    
    # Tag record to file name
    df['File'] = fnombre
    
    # Make the "File" column the index of the df
    return df.set_index(['File'])

# Go through each file name, create a dataframe, and add it to a list.  
 
# i.e.  
# df_list = [df, df, df]

# Create a list of dataframes
df_list = [GetFile(fname) for fname in FileNames]
df_list

# Combine all of the dataframes into one
big_df = pd.concat(df_list)
big_df

big_df.dtypes

# Plot it!
big_df['Channel'].plot.bar();
```


