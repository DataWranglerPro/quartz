You can also find this code on nbviewer.
- [Lesson 03](https://nbviewer.org/url/bitbucket.org/hrojas/learn-pandas/raw/master/lessons/03%20-%20Lesson.ipynb)

``` python
#!/usr/bin/env python
# coding: utf-8

# Lesson 3

# **Get Data** - Our data set will consist of an Excel file containing customer counts per date. We will learn how to read in the excel file for processing.  

# **Prepare Data** - The data is an irregular time series having duplicate dates. We will be challenged in compressing the data and coming up with next years forecasted customer count.  

# **Analyze Data** - We use graphs to visualize trends and spot outliers. Some built in computational tools will be used to calculate next years forecasted customer count.  

# **Present Data** - The results will be plotted.  
 
# ***NOTE:
# Make sure you have looked through all previous lessons, as the knowledge learned in previous lessons will be
# needed for this exercise.***

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import matplotlib

get_ipython().run_line_magic('matplotlib', 'inline')

print('Python version ' + sys.version)
print('Pandas version: ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)
print('Numpy version ' + np.__version__)

# > We will be creating our own test data for analysis.

# set seed
np.random.seed(111)

# Function to generate test data
def create_data_set(Number=1):
    ''' generates test data '''
    Output = []
    
    for i in range(Number):
        
        # Create a weekly (mondays) date range
        rng = pd.date_range(start='1/1/2009', end='12/31/2012', freq='W-MON')
        
        # Create random data
        data = np.random.randint(low=25,high=1000,size=len(rng))
        
        # Status pool
        status = [1,2,3]
        
        # Make a random list of statuses
        random_status = [status[np.random.randint(low=0,high=len(status))] for i in range(len(rng))]
        
        # State pool
        states = ['GA','FL','fl','NY','NJ','TX']
        
        # Make a random list of states 
        random_states = [states[np.random.randint(low=0,high=len(states))] for i in range(len(rng))]
    
        Output.extend(zip(random_states, random_status, data, rng))
        
    return Output


# Now that we have a function to generate our test data, lets create some data and stick it into a dataframe.
dataset = create_data_set(4)
df = pd.DataFrame(data=dataset, columns=['state','status','customer_count','status_date'])
df.info()

df.head()

# We are now going to save this dataframe into an Excel file, to then bring it back to a dataframe. We simply do this to show you how to read and write to Excel files.  
 
# We do not write the index values of the dataframe to the Excel file, since they are not meant to be part of our initial test data set.

# Save results to excel
df.to_excel('Lesson3.xlsx', index=False)
print('Done')

# Grab Data from Excel  
 
# We will be using the ***read_excel*** function to read in data from an Excel file. The function allows you to read in specfic tabs by name or location.
get_ipython().run_line_magic('pinfo', 'pd.read_excel')

# **Note: The location on the Excel file will be in the same folder as the notebook, unless specified otherwise.**

# Location of file
Location = r'C:\notebooks\pandas\Lesson3.xlsx'

# Parse a specific sheet
df = pd.read_excel(Location, 0, index_col='status_date')
df.dtypes

df.index

df.head()

# Prepare Data  
 
# This section attempts to clean up the data for analysis.  
# 1. Make sure the state column is all in upper case  
# 2. Only select records where the account status is equal to "1"  
# 3. Merge (NJ and NY) to NY in the state column  
# 4. Remove any outliers (any odd results in the data set)
 
# Lets take a quick look on how some of the ***state*** values are upper case and some are lower case
df['state'].unique()

# To convert all the state values to upper case we will use the ***upper()*** function and the dataframe's ***apply*** attribute. The ***lambda*** function simply will apply the upper function to each value in the *state* column.

# Clean state column, convert to upper case
df['state'] = df.state.apply(lambda x: x.upper())

df['state'].unique()

# Only grab where status == 1
mask = df['status'] == 1
df = df[mask]

# To turn the ***NJ*** states to ***NY*** we simply...  
 
# ***[df.state == 'NJ']*** - Find all records in the *state* column where they are equal to *NJ*.  
# ***df.state[df.state == 'NJ'] = 'NY'*** - For all records in the *state* column where they are equal to *NJ*, replace them with *NY*.

# Convert NJ to NY
mask = df.state == 'NJ'
df['state'][mask] = 'NY'

# Now we can see we have a much cleaner data set to work with.
df['state'].unique()

# At this point we may want to graph the data to check for any outliers or inconsistencies in the data. We will be using the ***plot()*** attribute of the dataframe.  
 
# As you can see from the graph below it is not very conclusive and is probably a sign that we need to perform some more data preparation.
df['customer_count'].plot(figsize=(15,5));

# If we take a look at the data, we begin to realize that there are multiple values for the same state, status_date, and status combination. It is possible that this means the data you are working with is dirty/bad/inaccurate, but we will assume otherwise. We can assume this data set is a subset of a bigger data set and if we simply add the values in the ***customer_count*** column per state, status_date, and status we will get the ***Total Customer Count*** per day.  
sortdf = df[df['state']=='NY'].sort_index(axis=0)
sortdf.head(10)

# Our task is now to create a new dataframe that compresses the data so we have daily customer counts per state and status_date. We can ignore the status column since all the values in this column are of value *1*. To accomplish this we will use the dataframe's functions ***groupby*** and ***sum()***.  
 
# Note that we had to use **reset_index** . If we did not, we would not have been able to group by both the state and the status_date since the groupby function expects only columns as inputs. The **reset_index** function will bring the index ***status_date*** back to a column in the dataframe. 

# Group by State and StatusDate
Daily = df.reset_index().groupby(['state','status_date']).sum()
Daily.head()

# The ***state*** and ***status_date*** columns are automatically placed in the index of the ***Daily*** dataframe. You can think of the ***index*** as the primary key of a database table but without the constraint of having unique values. Columns located in the index as you will see shortly, allow us to easily select, plot, and perform calculations on the data.  
 
# Below we delete the ***status*** column since it was all originally equal to one and the sum of this column has no meaning.
del Daily['status']
Daily.head()

# What is the index of the dataframe
Daily.index

# Select the state index
Daily.index.levels[0]

# Select the status_date index
Daily.index.levels[1]

# Lets now plot the data per state.  
 
# As you can see by breaking the graph up by the ***state*** column we have a much clearer picture on how the data looks like. Can you spot any outliers?
Daily.loc['FL'].plot()
Daily.loc['GA'].plot()
Daily.loc['NY'].plot()
Daily.loc['TX'].plot();

# We can also just plot the data on a specific date, like ***2012***. We can now clearly see that the data for these states is all over the place. since the data consist of weekly customer counts, the variability of the data seems suspect. For this tutorial we will assume bad data and proceed. 
Daily.loc['FL']['2012':].plot()
Daily.loc['GA']['2012':].plot()
Daily.loc['NY']['2012':].plot()
Daily.loc['TX']['2012':].plot();

# We will assume that per month the customer count should remain relatively steady. Any data outside a specific range in that month will be removed from the data set. The final result should have smooth graphs with no spikes.  
 
# ***StateYearMonth*** - Here we group by state, Year of status_date, and Month of status_date.  
# ***Daily['Outlier']*** - A boolean (True or False) value letting us know if the value in the customer_count column is ouside the acceptable range.  
 
# We will be using the attribute ***transform*** instead of ***apply***. The reason is that transform will keep the shape(# of rows and columns) of the dataframe the same and apply will not. By looking at the previous graphs, we can realize they are not resembling a gaussian distribution, this means we cannot use summary statistics like the mean and stDev. We use percentiles instead. Note that we run the risk of eliminating good data.

# Calculate Outliers
StateYearMonth = Daily.groupby([Daily.index.get_level_values(0), Daily.index.get_level_values(1).year, Daily.index.get_level_values(1).month])
Daily['lower'] = StateYearMonth['customer_count'].transform( lambda x: x.quantile(q=.25) - (1.5*x.quantile(q=.75)-x.quantile(q=.25)) )
Daily['upper'] = StateYearMonth['customer_count'].transform( lambda x: x.quantile(q=.75) + (1.5*x.quantile(q=.75)-x.quantile(q=.25)) )
Daily['outlier'] = (Daily['customer_count'] < Daily['lower']) | (Daily['customer_count'] > Daily['upper']) 

# Remove Outliers
Daily = Daily[Daily['outlier'] == False]

# The dataframe named ***Daily*** will hold customer counts that have been aggregated per day. The original data (df) has multiple records per day.  We are left with a data set that is indexed by both the state and the status_date. The Outlier column should be equal to ***False*** signifying that the record is not an outlier.
Daily.head()

# We create a separate dataframe named ***ALL*** which groups the Daily dataframe by status_date. We are essentially getting rid of the ***state*** column. The ***Max*** column represents the maximum customer count per month. The ***Max*** column is used to smooth out the graph.

# Combine all markets

# Get the max customer count by Date
ALL = pd.DataFrame(Daily['customer_count'].groupby(Daily.index.get_level_values(1)).sum())
ALL.columns = ['customer_count'] # rename column

# Group by Year and Month
YearMonth = ALL.groupby([lambda x: x.year, lambda x: x.month])

# What is the max customer count per Year and Month
ALL['max'] = YearMonth['customer_count'].transform(lambda x: x.max())
ALL.head()

# As you can see from the ***ALL*** dataframe above, in the month of January 2009, the maximum customer count was 901. If we had used ***apply***, we would have got a dataframe with (Year and Month) as the index and just the *Max* column with the value of 901. 

# ----------------------------------  
# There is also an interest to gauge if the current customer counts were reaching certain goals the company had established. The task here is to visually show if the current customer counts are meeting the goals listed below. We will call the goals ***BHAG*** (Big Hairy Annual Goal).  
# 
# * 12/31/2011 - 1,000 customers  
# * 12/31/2012 - 2,000 customers  
# * 12/31/2013 - 3,000 customers  
# 
# We will be using the **date_range** function to create our dates.  
# 
# ***Definition:*** date_range(start=None, end=None, periods=None, freq='D', tz=None, normalize=False, name=None, closed=None)  
# ***Docstring:*** Return a fixed frequency datetime index, with day (calendar) as the default frequency  
# 
# By choosing the frequency to be ***A*** or annual we will be able to get the three target dates from above.
get_ipython().run_line_magic('pinfo', 'pd.date_range')

# Create the BHAG dataframe
data = [1000,2000,3000]
idx = pd.date_range(start='12/31/2011', end='12/31/2013', freq='A')
BHAG = pd.DataFrame(data, index=idx, columns=['BHAG'])
BHAG

# Combining dataframes as we have learned in previous lesson is made simple using the ***concat*** function. Remember when we choose ***axis = 0*** we are appending row wise.

# Combine the BHAG and the ALL data set 
combined = pd.concat([ALL,BHAG], axis=0)
combined = combined.sort_index(axis=0)
combined.tail()

fig, axes = plt.subplots(figsize=(12, 7))

combined['BHAG'].fillna(method='pad').plot(color='green', label='BHAG')
combined['max'].plot(color='blue', label='All Markets')
plt.legend(loc='best');

# There was also a need to forecast next year's customer count and we can do this in a couple of simple steps. We will first group the ***combined*** dataframe by ***Year*** and place the maximum customer count for that year. This will give us one row per Year.   

# Group by Year and then get the max value per year
Year = combined.groupby(lambda x: x.year).max()
Year

# Add a column representing the percent change per year
Year['yr_pct_change'] = Year['max'].pct_change(periods=1)
Year

# To get next year's end customer count we will assume our current growth rate remains constant. We then will increase this years customer count by that amount and that will be our forecast for next year. 
(1 + Year.loc[2012,'yr_pct_change']) * Year.loc[2012,'max']

# Present Data  
 
# Create individual Graphs per state.  

# First Graph
ALL['max'].plot(figsize=(10, 5), title='ALL Markets')

# Last four Graphs
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 10))
fig.subplots_adjust(hspace=1.0) ## Create space between plots

Daily.loc['FL']['customer_count']['2012':].fillna(method='pad').plot(ax=axes[0,0])
Daily.loc['GA']['customer_count']['2012':].fillna(method='pad').plot(ax=axes[0,1]) 
Daily.loc['TX']['customer_count']['2012':].fillna(method='pad').plot(ax=axes[1,0]) 
Daily.loc['NY']['customer_count']['2012':].fillna(method='pad').plot(ax=axes[1,1]) 

# Add titles
axes[0,0].set_title('Florida')
axes[0,1].set_title('Georgia')
axes[1,0].set_title('Texas')
axes[1,1].set_title('North East');
```


