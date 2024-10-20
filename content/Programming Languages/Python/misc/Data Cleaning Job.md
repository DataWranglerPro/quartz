
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/data_cleaning_job.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

Below is an Elance job I was planning to bid on but I don't think I ever did. I only have some of the data for the full task, so I have not tested it with multiple Excel files.  

# GOAL  
Your task will be to convert the 13 excel files of approximate 386,000 rows into 1 excel file and meeting all of Goals 1A and 1B.
If you are able to complete Goal number 2.  Then please give me a separate quote for this.

### Goal 1A  
Each unique name will have an ID NUMBER.

### Goal 1B  
Merge all NAME fields into a minimum of 2 NAME FIELDS (LAST, FIRST) and a maxiumum of 3 NAME fields (LAST, FIRST, MIDDLE)   

### Goal 2
Obtain current contact data for each ID NUMBER:  Most important contact data is:  A.  Cell Phone  B.  Home Phone  C.  Email address  D.  Face Book ID.   Each of the people in the DB is originally from The Philippines.  Though a portion of them may live in another country.

Logic for programmer:
- ***Goal 1A:***  
    - Each excel file has a unique date. We want to use that date as part of the ID NUMBER in addition to adding a 7 digit number to it
        - For Example, if the excel file is called JUNE2012,   then the ID number will be:  JUNE2012-1000001,  next would be:  JUNE2012-1000002

- ***Goal 1B:***
    - Please open June 2012 Excel file 
    - Columns: LAST, FIRST, ADDITIONAL FIRST, MIDDLE, ADDITIONAL MIDDLE
    - Logic:
        - If ADDITIONAL columns are populated, names should be merged and a -hyphen- put between the names

```python
# import libraries
import pandas as pd
import os
```


```python
# list to hold file names
FileNames = []

# your path will be different, please modify the path below.
path = r'C:\notebooks'

# changes the current working directory to the given path
os.chdir(path)

# find any file that ends with ".xlsx"
for files in os.listdir("."):
    if files.endswith(".xlsx"):
        FileNames.append(files)
 
FileNames
```

    ['June_2012.xlsx']


We are assuming the only columns of interest are the following:  

* Last Name  
* First Name  
* additional First Name
* Middle Name
* additional Middle Name

```python
# create a function to process all of the files.
def GetFile(fnombre):

    # header names
    header_names = ['last_name', 'first_name', 'additional_first_name', 'middle_name', 'additional_middle_name']

    # read xlsx file
    df = pd.read_excel(path + '\\' + fnombre, sheet_name='Sheet1', usecols=[1,2,3,4,5], names=header_names)
    
    # add a column to identify file source
    df['FILE'] = fnombre 
    
    # make the "File" column the index of the df
    return df.set_index(['FILE'])
```


```python
# create a list of dataframes
df_list = [GetFile(fname) for fname in FileNames]
```


```python
# we only have one Excel file for this example
len(df_list)
```

    1


These are the top 5 records we have imported into memory.

```python
df_list[0].head()
```

|                    | last_name | first_name    | additional_first_name | middle_name | additional_middle_name |
| ------------------ | --------- | ------------- | --------------------- | ----------- | ---------------------- |
| **FILE**           |           |               |                       |             |                        |
| **June_2012.xlsx** | ABABA,    | LEO MARTIN    | PALACIO               | NaN         | NaN                    |
| **June_2012.xlsx** | ABABAO,   | JAN CHRISTIAN | TATLONGHARI           | NaN         | NaN                    |
| **June_2012.xlsx** | ABABON,   | PATRICK       | GUARDAQUIVIL          | NaN         | NaN                    |
| **June_2012.xlsx** | ABACLOD,  | MARCINA       | KIASSAO               | NaN         | NaN                    |
| **June_2012.xlsx** | ABACO,    | ELY JANE      | CAMACHO               | NaN         | NaN                    |


```python
# combine all of the dataframes into one
big_df = pd.concat(df_list)
#big_df.head()
```

```python
big_df.describe()
```

|            | last_name | first_name | additional_first_name | middle_name | additional_middle_name |
| ---------- | --------- | ---------- | --------------------- | ----------- | ---------------------- |
| **count**  | 28383     | 28383      | 26496                 | 14768       | 1761                   |
| **unique** | 13873     | 12008      | 11073                 | 8089        | 1058                   |
| **top**    | DE        | MA         | MAE                   | DE          | CRUZ                   |
| **freq**   | 395       | 541        | 626                   | 204         | 108                    |


```python
big_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 28389 entries, June_2012.xlsx to June_2012.xlsx
    Data columns (total 5 columns):
     #   Column                  Non-Null Count  Dtype 
    ---  ------                  --------------  ----- 
     0   last_name               28383 non-null  object
     1   first_name              28383 non-null  object
     2   additional_first_name   26496 non-null  object
     3   middle_name             14768 non-null  object
     4   additional_middle_name  1761 non-null   object
    dtypes: object(5)
    memory usage: 1.3+ MB
    


```python
# create a copy of the raw data
#draft = big_df[['last_name', 'first_name', 'additional_first_name', 'middle_name', 'additional_middle_name']]
draft = big_df
draft.head()
```

|                    | last_name | first_name    | additional_first_name | middle_name | additional_middle_name |
| ------------------ | --------- | ------------- | --------------------- | ----------- | ---------------------- |
| **FILE**           |           |               |                       |             |                        |
| **June_2012.xlsx** | ABABA,    | LEO MARTIN    | PALACIO               | NaN         | NaN                    |
| **June_2012.xlsx** | ABABAO,   | JAN CHRISTIAN | TATLONGHARI           | NaN         | NaN                    |
| **June_2012.xlsx** | ABABON,   | PATRICK       | GUARDAQUIVIL          | NaN         | NaN                    |
| **June_2012.xlsx** | ABACLOD,  | MARCINA       | KIASSAO               | NaN         | NaN                    |
| **June_2012.xlsx** | ABACO,    | ELY JANE      | CAMACHO               | NaN         | NaN                    |


**Condition 1:** Records where "first_name/additional_first_name" are ***not*** null  
**Condition 2:** Records where "middle_name/additional_middle_name" are ***not*** null 

If both conditions are true, combine First/Middle and additional as shown below.

```python
# find records where additional columns are not null
addFN = ~(draft['additional_first_name'].isnull()) 
addMN = ~(draft['additional_middle_name'].isnull()) 

# find records where first_name/middle_name columns are not null
FN = ~(draft['first_name'].isnull())
MN = ~(draft['middle_name'].isnull())

# if both conditions above are true, combine First/Middle and additional
draft.loc[addFN & FN, 'first_name'] = draft.loc[addFN, :].apply(lambda x: x['first_name'] + '-' + x['additional_first_name'], axis=1)
draft.loc[addMN & MN, 'middle_name'] = draft.loc[addMN, :].apply(lambda x: x['middle_name'] + '-' + x['additional_middle_name'], axis=1)
```

Take a peek at the data to make sure it looks ok.

```python
draft[addFN].head()
```

|                    | last_name | first_name                | additional_first_name | middle_name | additional_middle_name |
| ------------------ | --------- | ------------------------- | --------------------- | ----------- | ---------------------- |
| **FILE**           |           |                           |                       |             |                        |
| **June_2012.xlsx** | ABABA,    | LEO MARTIN-PALACIO        | PALACIO               | NaN         | NaN                    |
| **June_2012.xlsx** | ABABAO,   | JAN CHRISTIAN-TATLONGHARI | TATLONGHARI           | NaN         | NaN                    |
| **June_2012.xlsx** | ABABON,   | PATRICK-GUARDAQUIVIL      | GUARDAQUIVIL          | NaN         | NaN                    |
| **June_2012.xlsx** | ABACLOD,  | MARCINA-KIASSAO           | KIASSAO               | NaN         | NaN                    |
| **June_2012.xlsx** | ABACO,    | ELY JANE-CAMACHO          | CAMACHO               | NaN         | NaN                    |

```python
draft[addMN].head()
```

|                    | last_name | first_name   | additional_first_name | middle_name     | additional_middle_name |
| ------------------ | --------- | ------------ | --------------------- | --------------- | ---------------------- |
| **FILE**           |           |              |                       |                 |                        |
| **June_2012.xlsx** | ABAD,     | JOHN-MARTIN  | MARTIN                | DE-LEON         | LEON                   |
| **June_2012.xlsx** | ABAD,     | SHEENA-LOU   | LOU                   | STA-TERESA      | TERESA                 |
| **June_2012.xlsx** | ABADAY,   | ZENAIDA-LYNN | LYNN                  | IVY-LAID        | LAID                   |
| **June_2012.xlsx** | ABALOS,   | MA-ELENA     | ELENA                 | KATHLEEN-DENILA | DENILA                 |
| **June_2012.xlsx** | ABAÑO,    | MA-DIOFELA   | DIOFELA               | GRIZEL-BITARA   | BITARA                 |


If "middle_name" has any missing values, fill those in using column "additional_middle_name".

```python
# Fill in missing values for Middle Name from addional column
draft.loc[:,'middle_name'] = draft.loc[:,'middle_name'].combine_first(draft.loc[:,'additional_middle_name'])
draft.head()    
```

|                    | last_name | first_name                | additional_first_name | middle_name | additional_middle_name |
| ------------------ | --------- | ------------------------- | --------------------- | ----------- | ---------------------- |
| **FILE**           |           |                           |                       |             |                        |
| **June_2012.xlsx** | ABABA,    | LEO MARTIN-PALACIO        | PALACIO               | NaN         | NaN                    |
| **June_2012.xlsx** | ABABAO,   | JAN CHRISTIAN-TATLONGHARI | TATLONGHARI           | NaN         | NaN                    |
| **June_2012.xlsx** | ABABON,   | PATRICK-GUARDAQUIVIL      | GUARDAQUIVIL          | NaN         | NaN                    |
| **June_2012.xlsx** | ABACLOD,  | MARCINA-KIASSAO           | KIASSAO               | NaN         | NaN                    |
| **June_2012.xlsx** | ABACO,    | ELY JANE-CAMACHO          | CAMACHO               | NaN         | NaN                    |


```python
# check for null values in middle name but we have data in the column additional_niddle_name
draft[(draft['middle_name'].isnull()) & ~(draft['additional_middle_name'].isnull())].tail()
```

|          | last_name | first_name | additional_first_name | middle_name | additional_middle_name |
| -------- | --------- | ---------- | --------------------- | ----------- | ---------------------- |
| **FILE** |           |            |                       |             |                        |
|          |           |            |                       |             |                        |


Sort the records by (Last Name, First Name, Middle Name).

```python
# make everything upper case
draft.loc[:,'last_name'] = draft.loc[:,'last_name'].str.upper()
draft.loc[:,'first_name'] = draft.loc[:,'first_name'].str.upper()
draft.loc[:,'middle_name'] = draft.loc[:,'middle_name'].str.upper()

# sort the records
draft = draft.sort_values(by=['last_name', 'first_name', 'middle_name'])
draft.head()
```

|                | last_name | first_name                | additional_first_name | middle_name | additional_middle_name |
| -------------- | --------- | ------------------------- | --------------------- | ----------- | ---------------------- |
| **FILE**           |           |                           |                       |             |                        |
| **June_2012.xlsx** | ABABA,    | LEO MARTIN-PALACIO        | PALACIO               | NaN         | NaN                    |
| **June_2012.xlsx** | ABABAO,   | JAN CHRISTIAN-TATLONGHARI | TATLONGHARI           | NaN         | NaN                    |
| **June_2012.xlsx** | ABABON,   | PATRICK-GUARDAQUIVIL      | GUARDAQUIVIL          | NaN         | NaN                    |
| **June_2012.xlsx** | ABACLOD,  | MARCINA-KIASSAO           | KIASSAO               | NaN         | NaN                    |
| **June_2012.xlsx** | ABACO,    | ELY JANE-CAMACHO          | CAMACHO               | NaN         | NaN                    |


Find ***null*** records...then delete them.

```python
# find any null columns
afn = (draft['additional_first_name'].isnull()) 
amn = (draft['additional_middle_name'].isnull()) 
mn = (draft['middle_name'].isnull())
fn = (draft['first_name'].isnull())
ln = (draft['last_name'].isnull())
draft[afn & amn & mn & fn & ln]
```

|                    | last_name | first_name | additional_first_name | middle_name | additional_middle_name |
| ------------------ | --------- | ---------- | --------------------- | ----------- | ---------------------- |
| **FILE**           |           |            |                       |             |                        |
| **June_2012.xlsx** | NaN       | NaN        | NaN                   | NaN         | NaN                    |
| **June_2012.xlsx** | NaN       | NaN        | NaN                   | NaN         | NaN                    |
| **June_2012.xlsx** | NaN       | NaN        | NaN                   | NaN         | NaN                    |
| **June_2012.xlsx** | NaN       | NaN        | NaN                   | NaN         | NaN                    |
| **June_2012.xlsx** | NaN       | NaN        | NaN                   | NaN         | NaN                    |
| **June_2012.xlsx** | NaN       | NaN        | NaN                   | NaN         | NaN                    |

```python
# drop any null rows
draft = draft.dropna(axis=0,how='all',subset=['last_name', 'first_name', 'additional_first_name', 'middle_name', 'additional_middle_name'])
```

Create ID column and show the final results.

```python
# this creates identity column
draft['id'] = draft.loc[:,'last_name'].rank(method='first') + 1000000

# get rid of decimals
draft['id'] = draft.loc[:,'id'].apply(lambda x: str(round(x, 1)).split('.')[0])

# create prefix
draft['prefix'] = [x[:-4] + '-' for x in draft.index.values]

# combine
draft['id'] = draft['prefix'] + draft['id'] 

draft.head()
```

|                    | last_name | first_name                | additional_first_name | middle_name | additional_middle_name | id                 | prefix      |
| ------------------ | --------- | ------------------------- | --------------------- | ----------- | ---------------------- | ------------------ | ----------- |
| **FILE**           |           |                           |                       |             |                        |                    |             |
| **June_2012.xlsx** | ABABA,    | LEO MARTIN-PALACIO        | PALACIO               | NaN         | NaN                    | June_2012.-1000001 | June_2012.- |
| **June_2012.xlsx** | ABABAO,   | JAN CHRISTIAN-TATLONGHARI | TATLONGHARI           | NaN         | NaN                    | June_2012.-1000002 | June_2012.- |
| **June_2012.xlsx** | ABABON,   | PATRICK-GUARDAQUIVIL      | GUARDAQUIVIL          | NaN         | NaN                    | June_2012.-1000003 | June_2012.- |
| **June_2012.xlsx** | ABACLOD,  | MARCINA-KIASSAO           | KIASSAO               | NaN         | NaN                    | June_2012.-1000004 | June_2012.- |
| **June_2012.xlsx** | ABACO,    | ELY JANE-CAMACHO          | CAMACHO               | NaN         | NaN                    | June_2012.-1000005 | June_2012.- |


```python
# final results
draft[['id', 'last_name', 'first_name', 'middle_name']].head()
```

|                    | id                 | last_name | first_name                | middle_name |
| ------------------ | ------------------ | --------- | ------------------------- | ----------- |
| **FILE**           |                    |           |                           |             |
| **June_2012.xlsx** | June_2012.-1000001 | ABABA,    | LEO MARTIN-PALACIO        | NaN         |
| **June_2012.xlsx** | June_2012.-1000002 | ABABAO,   | JAN CHRISTIAN-TATLONGHARI | NaN         |
| **June_2012.xlsx** | June_2012.-1000003 | ABABON,   | PATRICK-GUARDAQUIVIL      | NaN         |
| **June_2012.xlsx** | June_2012.-1000004 | ABACLOD,  | MARCINA-KIASSAO           | NaN         |
| **June_2012.xlsx** | June_2012.-1000005 | ABACO,    | ELY JANE-CAMACHO          | NaN         |











