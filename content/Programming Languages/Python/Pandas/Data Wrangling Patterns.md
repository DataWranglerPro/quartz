
| **Pattern Name**       | **Description**                                                         | **Pattern Structure**                                                                                                                                                                                                                                                        |
| ---------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Herd Pattern**       | Group data, apply aggregate functions                                   | `group = data.groupby(column(s))`  <br>`result = group[column].agg_func()`<br>`or result = group.agg(`<br>    `new_col1 = pd.NamedAgg(column='column_name',aggfunc=agg_func1),`<br>    `new_col2 = pd.NamedAgg(column='column_name',aggfunc=agg_func2),`<br>    `...`<br>`)` |
| **Cherrypick Pattern** | Group data, apply aggregate functions, extract top/bottom N rows        | `group = data.groupby(column(s))`  <br>`result = group.apply(lambda x: x.agg(agg_func).nlargest(n))`                                                                                                                                                                         |
| **Fence Pattern**      | Group data, apply aggregate functions, order results, select top N rows | `group = data[[column(s)]].groupby(column_name)`  <br>`result = group.agg(agg_func).sort_values(by=column_name).head(n)`                                                                                                                                                     |
| **Bin Pattern**        | Divide continuous data into discrete categories                         | `bins = [lower_bound, mid_bound, upper_bound]`  <br>`labels = [label1, label2, label3]`  <br>`binned_data = pd.cut(data[column], bins=bins, labels=labels)`                                                                                                                  |
| **Gather Pattern**     | Apply custom function to each row or column                             | `column_wise_result = df['column'].apply(custom_function)`  <br>`row_wise_result = df.apply(custom_function, axis=1)`                                                                                                                                                        |
| **Mark Pattern**       | Categorize data based on keywords in text column                        | `mapping = {**dict.fromkeys(list_of_keywords1, category1), ...}`  <br>`def categorize(val): ...`  <br>`df[new_column] = df[text_column].apply(categorize)`                                                                                                                   |
| **Map Pattern**        | Map specific values in a column to new categorical values               | `mapping = {**dict.fromkeys([value1, value2, ...], category1), ...}`  <br>`df[new_column] = df[original_column].map(mapping)`                                                                                                                                                |
| **Graze Pattern**      | Group sorted data, apply aggregation function to another column         | `group = data.groupby(column(s))`    <br>`data[new_column] = group[column_to_transform].transform(agg_func)`                                                                                                                                                                 |

# Herd Pattern
Group data by one or more columns and apply an aggregate function(s) to a selected column.

### Pattern Structure:

``` python
# 1. Group data
group = data.groupby(column(s))

# 2. Apply aggregate function to a column
result = group[column].agg_func() 

# 3. Apply aggregate function(s) to a column
result = group.agg(
    new_col1 = pd.NamedAgg(column='column_name',aggfunc=agg_func1),
    new_col2 = pd.NamedAgg(column='column_name',aggfunc=agg_func2),
    ...)
```

### Example Usage:

``` python
import pandas as pd

patient_data = pd.DataFrame({
    'Diagnosis': ['A', 'B', 'A', 'C', 'B', 'A'],
    'Length of Stay': [5, 3, 7, 2, 4, 6]
})

# Get average length of stay by diagnosis
group = patient_data.groupby('Diagnosis')
avg_stay = group['Length of Stay'].mean()
```

``` python
import pandas as pd

patient_data = pd.DataFrame({
    'Diagnosis': ['A', 'B', 'A', 'C', 'B', 'A'],
    'Length of Stay': [5, 3, 7, 2, 4, 6]
})

# Get multiple statistics for length of stay by diagnosis
group = patient_data.groupby('Diagnosis')
stats = group.agg(
    count_diagnosis = pd.NamedAgg(column='Diagnosis', aggfunc='count'),
    min_len_of_stay = pd.NamedAgg(column='Length of Stay', aggfunc='min'),
    amax_len_of_stay = pd.NamedAgg(column='Length of Stay', aggfunc='max')
)
```


# Map Pattern
Map specific values in a column to new categorical values.

### Pattern Structure:

``` python

# the list contains the values that will be mapped to a specific category
mapping = {**dict.fromkeys([value1, value2, ...], category1), 
		   **dict.fromkeys([value3, value4, ...], category2), ...}

# compare each value in a column to the list. If a match is found, return the category
df[new_column] = df[original_column].map(mapping)
```

### Example Usage:

``` python
import pandas as pd

# create dataset
data = {'Item': ['Apple', 'Carrot', 'Banana']}
df = pd.DataFrame(data)

# define the map
mapping = {**dict.fromkeys(['Apple', 'Banana'], 'Fruit'),
		   **dict.fromkeys(['Carrot'], 'Vegetable')}

# map the items to their categories
df['Category'] = df['Item'].map(mapping)
```

