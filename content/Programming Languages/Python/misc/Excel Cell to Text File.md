
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/ExcelCell_To_TextFile.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

**Description:** At work, I had an employee who was avoiding a data task. He needed to Export a couple of columns into an Excel file. This is normally not that difficult, but he told me he needed help writing a script. He wanted every cell in the column to be exported into an individual text file. He started doing this manually (copy/paste) and realized this was going to take many hours. I think he had about 300+ files to create.

```python
# import libraries
import pandas as pd
import sys

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
```

    Python version 3.11.7 | packaged by Anaconda, Inc. | (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
    Pandas version 2.2.1
    

### Sample Excel File  

Here are the contents of the Excel file I will use to show you how to solve it using Pandas.

**ID**  
1  
2  
3  
4  
5  

```python
# import sample excel file
df = pd.read_excel('sample.xlsx')
df
```

|     | ID  |
| --- | --- |
| 0   | 1   |
| 1   | 2   |
| 2   | 3   |
| 3   | 4   |
| 4   | 5   |

Let's verify the datatypes are correct by using **info()**  

> As shown below we can see the column named "ID" is of integer type.

```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 5 entries, 0 to 4
    Data columns (total 1 columns):
     #   Column  Non-Null Count  Dtype
    ---  ------  --------------  -----
     0   ID      5 non-null      int64
    dtypes: int64(1)
    memory usage: 172.0 bytes
    

---
The goal of the loop below is to export every row in the DataFrame into an individual text file.  

I normally only try to use Pandas methods, but the index of the DataFrame kept ending up in the text file and I only wanted the value of the row in each of the text files. This is why I am using plain Python to handle the file writing piece. 

```python
# loop through the df
for index, row in df.iterrows():
    # grab the value of the row
    value = row.values.item()

    # save the value into a text file
    with open(f'row_{index}.txt', 'w') as f:
        f.write(str(value))
```

# Summary:
The tutorial demonstrated how to export each cell in an Excel column into individual text files using Python's Pandas library. I provided you a step-by-step guide on importing an Excel file, verifying data types, and using a loop to write each cell value into a separate text file.

### Key Takeaways:  
- Import Excel file into a Pandas DataFrame `pd.read_excel("sample.xlsx")`
- Verify data types using `df.info()`
- Use `df.iterrows()` to iterate through each row in the DataFrame
- Use `row.values.item()` to extract the value of each row (excluding index)
- Use Python's with `open()` function to write each value into a separate text file
- Use f-strings to dynamically name text files `f"row_{index}.txt"`













