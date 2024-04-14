You can also find this code on nbviewer.
- [Lesson 09](https://nbviewer.org/url/bitbucket.org/hrojas/learn-pandas/raw/master/lessons/09%20-%20Lesson.ipynb)

``` python
#!/usr/bin/env python
# coding: utf-8

# Lesson 9

# > Export data from a microdost sql database to cvs, excel, and txt.

# Import libraries
import pandas as pd
import sys
from sqlalchemy import create_engine, MetaData, Table, select

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)

# Grab Data from SQL  
 
# In this section we use the ***sqlalchemy*** library to grab data from a sql database. Note that the parameter section will need to be modified.

# Parameters
TableName = "data"

DB = {
    'drivername': 'mssql+pyodbc',
    'servername': 'DAVID-THINK',
    #'port': '5432',
    #'username': 'lynn',
    #'password': '',
    'database': 'BizIntel',
    'driver': 'SQL Server Native Client 11.0',
    'trusted_connection': 'yes',  
    'legacy_schema_aliasing': False
}

# Create the connection
engine = create_engine(DB['drivername'] + '://' + DB['servername'] + '/' + DB['database'] + '?' + 'driver=' + DB['driver'] + ';' + 'trusted_connection=' + DB['trusted_connection'], legacy_schema_aliasing=DB['legacy_schema_aliasing'])
conn = engine.connect()

# Required for querying tables
metadata = MetaData(conn)

# Table to query
tbl = Table(TableName, metadata, autoload=True, schema="dbo")
#tbl.create(checkfirst=True)

# Select all
sql = tbl.select()

# run sql code
result = conn.execute(sql)

# Insert to a dataframe
df = pd.DataFrame(data=list(result), columns=result.keys())

# Close connection
conn.close()

print('Done')

# All the files below will be saved to the same folder the notebook resides in.

# Export to CSV
df.to_csv('DimDate.csv', index=False)
print('Done')

# Export to EXCEL
df.to_excel('DimDate.xls', index=False)
print('Done')

# Export to TXT
df.to_csv('DimDate.txt', index=False)
print('Done')
```


