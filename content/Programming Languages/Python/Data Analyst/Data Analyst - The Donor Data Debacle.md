
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/8ed8016618013ad58840f639302dc424fe2c57a5/content/Assets/notebooks/donor_data_debacle.ipynb), offering an alternative platform for your learning convenience.
> - [Pandas Ninja](https://hedaro.gumroad.com/l/jVeRh): Take your skills to the next level with comprehensive Jupyter Notebook tutorials covering dates, group by, plotting, pivot tables, and more. Includes specialized tutorials for Excel and SQL developers, helping you master data analysis with Pandas.

### Description:

You're a data analyst for a non-profit organization, and you've been tasked with cleaning up a messy dataset of donations. The data is a bit of a disaster, with missing values, duplicates, and inconsistent formatting. Your mission is to use your Pandas skills to wrangle the data into shape.

### Tasks:

- **Clean up the Mess:** Remove duplicates, handle missing values, and ensure data types are correct.
- **Standardize the data:** Normalize the 'Donation Amount' column and convert the `date` column to a standard format.
- **Data quality check:** Identify and correct any inconsistent or invalid data.

``` python
# import libraries
import pandas as pd
import numpy as np
import sys
import re

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
print('Numpy version ' + np.__version__)
```

``` output
Python version 3.11.7 | packaged by Anaconda, Inc. | (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
Pandas version 2.2.1
Numpy version 1.26.4
```

# The Data

The columns below represent information about individual donations, the date they were made, and the campaign that drove the donation. The goal is to clean, transform, and prepare this data for analysis.

Here's a breakdown of what each column in the sample data represents:

- **Donor ID:** A unique identifier for each donor
- **Donation Amount:** The amount donated by each donor ( initially in a mix of numeric and string formats, requiring cleanup)
- **Date:** The date each donation was made
- **Campaign:** The marketing campaign or channel that led to the donation

Important Note about the `Donation Amount` Column:

The logic below will generate a mix of:

- Numeric values (e.g., 10.50, 500.00)
- String values with words (e.g., "10 thousand", "5 dollars and 25 cents")
- String values with currency symbols (e.g., "`$50`", "`$1000`")

Your task will be to clean up this column by converting all values to a standard numeric format, handling the various string formats, and dealing with any potential errors or inconsistencies. Good luck!

``` python
# set the seed
np.random.seed(0)

# synthetic data
data = {
'donor_id': np.random.randint(1, 1000, 10000),
'date': np.random.choice(pd.date_range('2022-01-01', periods=365), 10000),
'campaign': np.random.choice(['Email', 'Social Media', 'Event'], 10000),
'donation_amount': np.random.choice([
	np.random.uniform(10, 1000), # numeric value
	f'{np.random.randint(1, 100)} thousand', # string value (e.g., "10 thousand")
	f'{np.random.randint(1, 10)} dollars and {np.random.randint(1, 100)} cents', # string value (e.g., "5 dollars and 25 cents")
	f'${np.random.randint(1, 100)}', # string value with currency symbol (e.g., "$50")
	], 10000)
}

# create dataframe
df = pd.DataFrame(data)

## introduce some messiness ##

# make the column the wrong datatype
df['donor_id'] = data['donor_id'].astype(str)

# missing values
df.loc[df.index % 3 == 0, 'donation_amount'] = np.nan

# messy is my middle name
df['date'] = data['date'].astype(str)
df.loc[df.index % 5 == 0, 'date'] = 'Invalid Date'

# the marketing manager is not going to be happy :)
df.loc[df.index % 7 == 0, 'campaign'] = 'Unknown'

df
```

|      | donor_id | date                          | campaign     | donation_amount        |
| ---- | -------- | ----------------------------- | ------------ | ---------------------- |
| 0    | 685      | Invalid Date                  | Unknown      | NaN                    |
| 1    | 560      | 2022-03-07T00:00:00.000000000 | Email        | 6 dollars and 98 cents |
| 2    | 630      | 2022-11-08T00:00:00.000000000 | Social Media | 76 thousand            |
| 3    | 193      | 2022-03-25T00:00:00.000000000 | Email        | NaN                    |
| 4    | 836      | 2022-04-07T00:00:00.000000000 | Email        | $81                    |
| ...  | ...      | ...                           | ...          | ...                    |
| 9995 | 426      | Invalid Date                  | Social Media | $81                    |
| 9996 | 891      | 2022-04-18T00:00:00.000000000 | Unknown      | NaN                    |
| 9997 | 778      | 2022-08-24T00:00:00.000000000 | Event        | $81                    |
| 9998 | 974      | 2022-10-07T00:00:00.000000000 | Email        | $81                    |
| 9999 | 74       | 2022-07-09T00:00:00.000000000 | Event        | NaN                    |
10000 rows × 4 columns

Let's start by looking at the datatypes.

As you can expect, Pandas is treating all of the columns as strings. Let the clean up process begin.

``` python
df.info()
```

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 10000 entries, 0 to 9999
Data columns (total 4 columns):
 #   Column           Non-Null Count  Dtype 
`---  ------           --------------  ----- 
 0   donor_id         10000 non-null  object
 1   date             10000 non-null  object
 2   campaign         10000 non-null  object
 3   donation_amount  6666 non-null   object
dtypes: object(4)
memory usage: 312.6+ KB

# Clean up the Mess:

Remove duplicates, handle missing values, and ensure data types are correct.

If we assume that we will not be able to get the correct donation amounts, we might as well remove those rows from the data.

``` python
df = df.dropna()

df.info()
```

<class 'pandas.core.frame.DataFrame'>
Index: 6666 entries, 1 to 9998
Data columns (total 4 columns):
 #   Column           Non-Null Count  Dtype 
`---  ------           --------------  ----- 
 0   donor_id         6666 non-null   object
 1   date             6666 non-null   object
 2   campaign         6666 non-null   object
 3   donation_amount  6666 non-null   object
dtypes: object(4)
memory usage: 260.4+ KB

The marketing manager told us to replace any missing dates with '1970-01-01' so we can identify these and deal with them later.

``` python
# identify the invalid dates
mask = df['date'] == 'Invalid Date'

df[mask].head()
```

|     | donor_id | date         | campaign     | donation_amount        |
| --- | -------- | ------------ | ------------ | ---------------------- |
| 5   | 764      | Invalid Date | Social Media | 77.55500350452421      |
| 10  | 278      | Invalid Date | Event        | 76 thousand            |
| 20  | 487      | Invalid Date | Event        | 77.55500350452421      |
| 25  | 850      | Invalid Date | Email        | 76 thousand            |
| 35  | 710      | Invalid Date | Unknown      | 6 dollars and 98 cents |

Here is where we set the dates to `1970-01-01`.

``` python
df.loc[mask,'date'] = '1970-01-01'

df
```

|      | donor_id | date                          | campaign     | donation_amount        |
| ---- | -------- | ----------------------------- | ------------ | ---------------------- |
| 1    | 560      | 2022-03-07T00:00:00.000000000 | Email        | 6 dollars and 98 cents |
| 2    | 630      | 2022-11-08T00:00:00.000000000 | Social Media | 76 thousand            |
| 4    | 836      | 2022-04-07T00:00:00.000000000 | Email        | $81                    |
| 5    | 764      | 1970-01-01                    | Social Media | 77.55500350452421      |
| 7    | 360      | 2022-10-20T00:00:00.000000000 | Unknown      | 76 thousand            |
| ...  | ...      | ...                           | ...          | ...                    |
| 9992 | 308      | 2022-01-13T00:00:00.000000000 | Email        | 77.55500350452421      |
| 9994 | 694      | 2022-07-21T00:00:00.000000000 | Event        | 6 dollars and 98 cents |
| 9995 | 426      | 1970-01-01                    | Social Media | $81                    |
| 9997 | 778      | 2022-08-24T00:00:00.000000000 | Event        | $81                    |
| 9998 | 974      | 2022-10-07T00:00:00.000000000 | Email        | $81                    |
6666 rows × 4 columns

Although we successfully converted the strings into dates, the date column remains in string format.

``` python
df.info()
```

<class 'pandas.core.frame.DataFrame'>
Index: 6666 entries, 1 to 9998
Data columns (total 4 columns):
 #   Column           Non-Null Count  Dtype 
`---  ------           --------------  ----- 
 0   donor_id         6666 non-null   object
 1   date             6666 non-null   object
 2   campaign         6666 non-null   object
 3   donation_amount  6666 non-null   object
dtypes: object(4)
memory usage: 260.4+ KB

Convert string column to a datetime object.

``` python
# `format='mixed'`, the format will be inferred for each element individually as the 1970 dates do not have the same format as the rest

pd.to_datetime(df['date'], format='mixed')
```

1      2022-03-07
2      2022-11-08
4      2022-04-07
5      1970-01-01
7      2022-10-20
          ...    
9992   2022-01-13
9994   2022-07-21
9995   1970-01-01
9997   2022-08-24
9998   2022-10-07
Name: date, Length: 6666, dtype: datetime64[ns]

This morning, for some reason I can't get these datatypes to behave...... the code below did not work.

``` python
# convert to date object
df.loc[:,'date'] = pd.to_datetime(df['date'], format='mixed')

df.info()
```

<class 'pandas.core.frame.DataFrame'>
Index: 6666 entries, 1 to 9998
Data columns (total 4 columns):
 #   Column           Non-Null Count  Dtype 
`---  ------           --------------  ----- 
 0   donor_id         6666 non-null   object
 1   date             6666 non-null   object
 2   campaign         6666 non-null   object
 3   donation_amount  6666 non-null   object
dtypes: object(4)
memory usage: 260.4+ KB

We can also take care of the Donor ID pretty easily.

This also did not work...

``` python
df.loc[:,'donor_id'] = df.loc[:,'donor_id'].astype(int)

df.info()
```

<class 'pandas.core.frame.DataFrame'>
Index: 6666 entries, 1 to 9998
Data columns (total 4 columns):
 #   Column           Non-Null Count  Dtype 
`---  ------           --------------  ----- 
 0   donor_id         6666 non-null   object
 1   date             6666 non-null   object
 2   campaign         6666 non-null   object
 3   donation_amount  6666 non-null   object
dtypes: object(4)
memory usage: 260.4+ KB

This did the trick for me to get the date types to be represented correctly.

``` python
df = df.convert_dtypes()

df.info()
```

<class 'pandas.core.frame.DataFrame'>
Index: 6666 entries, 1 to 9998
Data columns (total 4 columns):
 #   Column           Non-Null Count  Dtype         
`---  ------           --------------  -----         
 0   donor_id         6666 non-null   Int64         
 1   date             6666 non-null   datetime64[ns]
 2   campaign         6666 non-null   string        
 3   donation_amount  6666 non-null   string        
dtypes: Int64(1), datetime64[ns](1), string(2)
memory usage: 266.9 KB

# Donation Amount Cleanup

- Remove the dollar sign
- Apply a custom function to convert the values to a numeric format

``` python
# remove dollar sign
df.loc[:,'donation_amount'] = df.loc[:,'donation_amount'].apply(lambda x:x.replace("$",""))

df.loc[:,'donation_amount'].head()
```

1    6 dollars and 98 cents
2               76 thousand
4                        81
5         77.55500350452421
7               76 thousand
Name: donation_amount, dtype: string

``` python
def clean_column(value):
	''' identify pattern and clean up
	patterns: "10 thousand", "5 dollars and 25 cents"
	'''
	
	pattern1 = r'\d+ thousand'
	pattern2 = r'\d+ dollars and \d+ cents'
	
	if re.search(pattern1, value):
		# remove all non numeric characters from the string
		return str(int(re.sub(r'[^\d]', '', value)) * 1000)
	
	elif re.search(pattern2, value):
		# remove all non numeric characters from the strings
		dollars = re.sub(r'[^\d]', '', value.split('and')[0])
		cents = re.sub(r'[^\d]', '', value.split('and')[1])
		return dollars + "." + cents
	
	else:
		return value

df.loc[:,'donation_amount'] = df['donation_amount'].apply(clean_column)

df['donation_amount'].head()
```

1                 6.98
2                76000
4                   81
5    77.55500350452421
7                76000
Name: donation_amount, dtype: string

Now let's fix the datatype for the donation amount.

``` python
df['donation_amount'] = df.loc[:,'donation_amount'].astype(float)

df.info()
```

<class 'pandas.core.frame.DataFrame'>
Index: 6666 entries, 1 to 9998
Data columns (total 4 columns):
 #   Column           Non-Null Count  Dtype         
`---  ------           --------------  -----         
 0   donor_id         6666 non-null   Int64         
 1   date             6666 non-null   datetime64[ns]
 2   campaign         6666 non-null   string        
 3   donation_amount  6666 non-null   float64       
dtypes: Int64(1), datetime64[ns](1), float64(1), string(1)
memory usage: 266.9 KB

OK, so we have taken care of a lot here.

- The donor_id column is now in integer format
- The date column is now in the correct format
- The donation_amount column has been successfully cleaned up and converted to the correct numeric format

``` python
# let's take a peek at the data
df.head(20)
```

|     |donor_id|date|campaign|donation_amount|
|---|---|---|---|---|
| 1   |560|2022-03-07|Email|6.980000|
| 2   |630|2022-11-08|Social Media|76000.000000|
| 4   |836|2022-04-07|Email|81.000000|
| 5   |764|1970-01-01|Social Media|77.555004|
| 7   |360|2022-10-20|Unknown|76000.000000|
| 8   |10|2022-06-18|Social Media|81.000000|
| 10  |278|1970-01-01|Event|76000.000000|
| 11  |755|2022-02-02|Event|76000.000000|
| 13  |600|2022-09-21|Social Media|6.980000|
| 14  |71|2022-05-25|Unknown|6.980000|
| 16  |601|2022-12-29|Event|76000.000000|
| 17  |397|2022-01-31|Event|81.000000|
| 19  |706|2022-12-05|Social Media|76000.000000|
| 20  |487|1970-01-01|Event|77.555004|
| 22  |88|2022-07-05|Social Media|6.980000|
| 23  |175|2022-07-24|Email|81.000000|
| 25  |850|1970-01-01|Email|76000.000000|
| 26  |678|2022-06-20|Event|76000.000000|
| 28  |846|2022-05-20|Unknown|77.555004|
| 29  |73|2022-08-31|Email|6.980000|

``` python
df.describe()
```

|       | donor_id   | date                          | donation_amount |
| ----- | ---------- | ----------------------------- | --------------- |
| count | 6666.0     | 6666                          | 6666.000000     |
| mean  | 501.192319 | 2012-01-04 18:13:04.158415872 | 19297.706620    |
| min   | 1.0        | 1970-01-01 00:00:00           | 6.980000        |
| 25%   | 255.0      | 2022-01-25 00:00:00           | 77.555004       |
| 50%   | 499.0      | 2022-05-24 00:00:00           | 77.555004       |
| 75%   | 755.0      | 2022-09-13 00:00:00           | 76000.000000    |
| max   | 999.0      | 2022-12-31 00:00:00           | 76000.000000    |
| std   | 288.740445 | NaN                           | 33034.244560    |

# Data Gaze

I am going to recommend you get this data into Microsoft Excel and do a quick glance. Excel does a much better job at letting you analyze the data on your nice and big monitor.

``` python
df.to_clipboard()
```


# If you find a better way to update datatypes, please share it with me.