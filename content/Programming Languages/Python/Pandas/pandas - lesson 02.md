You can also find this code on nbviewer.
- [Lesson 02](https://nbviewer.org/url/bitbucket.org/hrojas/learn-pandas/raw/master/lessons/02%20-%20Lesson.ipynb)

``` python
#!/usr/bin/env python
# coding: utf-8

# # Lesson 2

# **Create Data** - We begin by creating our own data set for analysis. This prevents the end user reading this tutorial from having to download any files to replicate the results below. We will export this data set to a text file so that you can get some experience pulling data from a text file.  

# **Get Data** - We will learn how to read in the text file containing the baby names. The data consist of baby names born in the year 1880.  

# **Prepare Data** - Here we will simply take a look at the data and make sure it is clean. By clean I mean we will take a look inside the contents of the text file and look for any anomality’s. These can include missing data, inconsistencies in the data, or any other data that seems out of place. If any are found we will then have to make decisions on what to do with these records.  

# **Analyze Data** - We will simply find the most popular name in a specific year.  

# **Present Data** - Through tabular data and a graph, clearly show the end user what is the most popular name in a specific year.  
 
# ***NOTE:  
# Make sure you have looked through all previous lessons as the knowledge learned in previous lessons will be needed for this exercise.***  
     

# > ***Numpy*** will be used to help generate the sample data set. Importing the libraries is the first step we will take in the lesson.

# Import all libraries needed for the tutorial
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number

# Enable inline plotting
get_ipython().run_line_magic('matplotlib', 'inline')

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)
print('Numpy version ' + np.__version__)

# Create Data  
 
# The data set will consist of 1,000 baby names and the number of births recorded for that year (1880). We will also add plenty of duplicates so you will see the same baby name more than once. You can think of the multiple entries per name simply being different hospitals around the country reporting the number of births per baby name. So if two hospitals reported the baby name "Bob", the data will have two values for the name Bob. We will start by creating the random set of baby names. 

# The inital set of baby names
names = ['Bob','Jessica','Mary','John','Mel']

# To make a random list of 1,000 baby names using the five above we will do the following:  
 
# * Generate a random number between 0 and 4  
 
# To do this we will be using the functions ***seed***, ***randint***, ***len***, ***range***, and ***zip***.   

# This will ensure the random samples below can be reproduced. 
# This means the random samples will always be identical.
get_ipython().run_line_magic('pinfo', 'np.random.seed')
get_ipython().run_line_magic('pinfo', 'np.random.randint')
get_ipython().run_line_magic('pinfo', 'len')
get_ipython().run_line_magic('pinfo', 'range')
get_ipython().run_line_magic('pinfo', 'zip')

# **seed(500)** - Create seed
 
# **randint(low=0,high=len(names))** - Generate a random integer between zero and the length of the list "names".    
 
# **names[n]** - Select the name where its index is equal to n.  
 
# **for i in range(n)** - Loop until i is equal to n, i.e. 1,2,3,....n.  
 
# **random_names** = Select a random name from the name list and do this n times.  
np.random.seed(500)
random_names = [names[np.random.randint(low=0,high=len(names))] for i in range(1000)]

# Print first 10 records
random_names[:10]

# Generate a random numbers between 0 and 1000    

# The number of births per name for the year 1880
births = [np.random.randint(low=0,high=1000) for i in range(1000)]
births[:10]

# Merge the ***names*** and the ***births*** data set using the ***zip*** function.
BabyDataSet = list(zip(random_names,births))
BabyDataSet[:10]

# We are basically done creating the data set. We now will use the ***pandas*** library to export this data set into a csv file. 
 
# ***df*** will be a ***DataFrame*** object. You can think of this object holding the contents of the BabyDataSet in a format similar to a sql table or an excel spreadsheet. Lets take a look below at the contents inside ***df***.
df = pd.DataFrame(data = BabyDataSet, columns=['Names', 'Births'])
df[:10]

# * Export the dataframe to a ***text*** file. We can name the file ***births1880.txt***. The function ***to_csv*** will be used to export. The file will be saved in the same location of the notebook unless specified otherwise.
get_ipython().run_line_magic('pinfo', 'df.to_csv')

# The only parameters we will use is ***index*** and ***header***. Setting these parameters to False will prevent the index and header names from being exported. Change the values of these parameters to get a better understanding of their use.
df.to_csv('births1880.txt',index=False,header=False)

# Get Data

# To pull in the text file, we will use the pandas function *read_csv*. Let us take a look at this function and what inputs it takes.
get_ipython().run_line_magic('pinfo', 'pd.read_csv')

# Even though this functions has many parameters, we will simply pass it the location of the text file.  
 
# Location = C:\Users\TYPE_USER_NAME\.xy\startups\births1880.txt  
 
# ***Note:*** Depending on where you save your notebooks, you may need to modify the location above. 
Location = r'C:\notebooks\pandas\births1880.txt'
df = pd.read_csv(Location)

# Notice the ***r*** before the string. Since the slashes are special characters, prefixing the string with a ***r*** will escape the whole string. 
df.info()

# Info says:  
 
# * There are ***999*** records in the data set  
# * There is a column named ***Mary*** with 999 values  
# * There is a column named ***968*** with 999 values  
# * Out of the ***two*** columns, one is ***numeric***, the other is ***non numeric***  

# To actually see the contents of the dataframe we can use the ***head()*** function which by default will return the first five records. You can also pass in a number n to return the top n records of the dataframe. 
df.head()

# This brings us to our first problem of the exercise. The ***read_csv*** function treated the first record in the text file as the header names. This is obviously not correct since the text file did not provide us with header names.  
 
# To correct this we will pass the ***header*** parameter to the *read_csv* function and set it to ***None*** (means null in python).
df = pd.read_csv(Location, header=None)
df.info()

# Info now says:  
# * There are ***1000*** records in the data set  
# * There is a column named ***0*** with 1000 values  
# * There is a column named ***1*** with 1000 values  
# * Out of the ***two*** columns, one is ***numeric***, the other is ***non numeric***  
 
# Now lets take a look at the last five records of the dataframe
df.tail()

# If we wanted to give the columns specific names, we would have to pass another paramter called ***names***. We can also omit the *header* parameter.
df = pd.read_csv(Location, names=['Names','Births'])
df.head(5)

# You can think of the numbers [0,1,2,3,4,...] as the row numbers in an Excel file. In pandas these are part of the ***index*** of the dataframe. You can think of the index as the primary key of a sql table with the exception that an index is allowed to have duplicates.  
 
# ***[Names, Births]*** can be though of as column headers similar to the ones found in an Excel spreadsheet or sql database.

# Delete the txt file now that we are done using it.
import os
os.remove(Location)

# Prepare Data

# The data we have consists of baby names and the number of births in the year 1880. We already know that we have 1,000 records and none of the records are missing (non-null values). We can verify the "Names" column still only has five unique names.  
 
# We can use the ***unique*** property of the dataframe to find all the unique records of the "Names" column.

# Method 1:
df['Names'].unique()

# If you actually want to print the unique values:
for x in df['Names'].unique():
    print(x)

# Method 2:
print(df['Names'].describe())

# Since we have multiple values per baby name, we need to aggregate this data so we only have a baby name appear once. This means the 1,000 rows will need to become 5. We can accomplish this by using the ***groupby*** function. 
get_ipython().run_line_magic('pinfo', 'df.groupby')

# Create a groupby object
name = df.groupby('Names')

# Apply the sum function to the groupby object
df = name.sum()
df

# Analyze Data

# To find the most popular name or the baby name with the higest birth rate, we can do one of the following.  
 
# * Sort the dataframe and select the top row
# * Use the ***max()*** attribute to find the maximum value

# Method 1:
Sorted = df.sort_values(['Births'], ascending=False)
Sorted.head(1)

# Method 2:
df['Births'].max()

# Present Data

# Here we can plot the ***Births*** column and label the graph to show the end user the highest point on the graph. In conjunction with the table, the end user has a clear picture that **Bob** is the most popular baby name in the data set. 

# Create graph
df['Births'].plot.bar()

print("The most popular name")
df.sort_values(by='Births', ascending=False)
```


