You can also find this code on nbviewer.
- [Lesson 08](https://nbviewer.org/url/bitbucket.org/hrojas/learn-pandas/raw/master/lessons/08%20-%20Lesson.ipynb)

``` python
#!/usr/bin/env python
# coding: utf-8

# Lesson 8

# > How to pull data from a microsoft sql database

# Import libraries
import pandas as pd
import sys
from sqlalchemy import create_engine, MetaData, Table, select, engine

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)

# Version 1  
 
# In this section we use the ***sqlalchemy*** library to grab data from a sql database. Make sure to use your own ***ServerName***, ***Database***, ***TableName***.

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

# Select the contents in the dataframe.
df.head()

df.dtypes

# Convert to specific data types. The code below will have to be modified to match your table.

# Version 2
import pandas.io.sql
import pyodbc

# Parameters
server = 'DAVID-THINK'
db = 'BizIntel'

# Create the connection
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + DB['servername'] + ';DATABASE=' + DB['database'] + ';Trusted_Connection=yes')

# query db
sql = """

SELECT top 5 *
FROM data

"""
df = pandas.io.sql.read_sql(sql, conn)
df.head()

# Version 3
from sqlalchemy import create_engine

# Parameters
ServerName = "DAVID-THINK"
Database = "BizIntel"
Driver = "driver=SQL Server Native Client 11.0"

# Create the connection
engine = create_engine('mssql+pyodbc://' + ServerName + '/' + Database + "?" + Driver)

df = pd.read_sql_query("SELECT top 5 * FROM data", engine)
df
```


