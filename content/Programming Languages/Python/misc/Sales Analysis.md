
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/sales_analysis.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

### Description:
You are a sales analyst for an e-commerce company. You have been tasked with analyzing the sales data to determine which regions and product categories are generating the most revenue. You have a dataset containing information about sales, including the region, product category, and sales amount.

### Tasks:

Using Pandas, write a program to:

- Load the dataset into a pandas DataFrame.
- Group the sales data by region and product category, and calculate the total sales amount for each region and product category.
- Calculate the total sales amount for each region and product category as a percentage of the overall sales amount.
- Print the top 3 regions and product categories with their total sales amount and percentage of overall sales.

**Hint:** You can use the groupby function to group the data by region and product category, and calculate the total sales amount for each group. Then, use the pivot_table function to reshape the data and calculate the percentages.

### Here is the dataset
```
Region,Product Category,Sales Amount
North,Electronics,1000
North,Clothing,800
South,Electronics,1200
South,Electronics,900
East,Clothing,1100
East,Electronics,700
West,Electronics,1000
West,Electronics,900
North,Clothing,600
South,Clothing,1000
```


```python
import pandas as pd
import sys
```

```python
print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
```

    Python version 3.11.7 
    Pandas version 2.2.1
    


```python
df = pd.read_clipboard(sep=",")
df
```

|     | Region | Product Category | Sales Amount |
| --- | ------ | ---------------- | ------------ |
| 0   | North  | Electronics      | 1000         |
| 1   | North  | Clothing         | 800          |
| 2   | South  | Electronics      | 1200         |
| 3   | South  | Electronics      | 900          |
| 4   | East   | Clothing         | 1100         |
| 5   | East   | Electronics      | 700          |
| 6   | West   | Electronics      | 1000         |
| 7   | West   | Electronics      | 900          |
| 8   | North  | Clothing         | 600          |
| 9   | South  | Clothing         | 1000         |

```python
# group the sales data by region and product category
group = df.groupby(['Region','Product Category'])

# total sales of group
group.sum()
```

|                 |                      | Sales Amount |
| --------------- | -------------------- | ------------ |
| **Region**      | **Product Category** |              |
| **East**        | **Clothing**         | 1100         |
| **Electronics** |                      | 700          |
| **North**       | **Clothing**         | 1400         |
| **Electronics** |                      | 1000         |
| **South**       | **Clothing**         | 1000         |
| **Electronics** |                      | 2100         |
| **West**        | **Electronics**      | 1900         |


```python
# flatten the group
agg = group['Sales Amount'].sum().reset_index()
agg
```

|     | Region | Product Category | Sales Amount |
| --- | ------ | ---------------- | ------------ |
| 0   | East   | Clothing         | 1100         |
| 1   | East   | Electronics      | 700          |
| 2   | North  | Clothing         | 1400         |
| 3   | North  | Electronics      | 1000         |
| 4   | South  | Clothing         | 1000         |
| 5   | South  | Electronics      | 2100         |
| 6   | West   | Electronics      | 1900         |


```python
# calculate total sales amount
total_sales = agg['Sales Amount'].sum()

# calculate percentage of total sales for each region and product category
agg['Percentage of Total Sales'] = (agg['Sales Amount'] / total_sales) * 100
agg
```

|     | Region | Product Category | Sales Amount | Percentage of Total Sales |
| --- | ------ | ---------------- | ------------ | ------------------------- |
| 0   | East   | Clothing         | 1100         | 11.956522                 |
| 1   | East   | Electronics      | 700          | 7.608696                  |
| 2   | North  | Clothing         | 1400         | 15.217391                 |
| 3   | North  | Electronics      | 1000         | 10.869565                 |
| 4   | South  | Clothing         | 1000         | 10.869565                 |
| 5   | South  | Electronics      | 2100         | 22.826087                 |
| 6   | West   | Electronics      | 1900         | 20.652174                 |


```python
# get the top 3 regions
agg.sort_values(by='Percentage of Total Sales', ascending=False).head(3)
```

|     | Region | Product Category | Sales Amount | Percentage of Total Sales |
| --- | ------ | ---------------- | ------------ | ------------------------- |
| 5   | South  | Electronics      | 2100         | 22.826087                 |
| 6   | West   | Electronics      | 1900         | 20.652174                 |
| 2   | North  | Clothing         | 1400         | 15.217391                 |


Here is an alternative solution using pivot tables.

```python
# pivot the data to get sales amount by region and product category
pivot = pd.pivot_table(df, values='Sales Amount', index='Region', columns='Product Category', aggfunc='sum')
pivot
```

| Product Category | Clothing | Electronics |
| ---------------- | -------- | ----------- |
| **Region**           |          |             |
| **East**             | 1100.0   | 700.0       |
| **North**            | 1400.0   | 1000.0      |
| **South**            | 1000.0   | 2100.0      |
| **West**             | NaN      | 1900.0      |


```python
# calculate total sales amount
total_sales = df['Sales Amount'].sum()
total_sales
```


    9200



```python
# calculate percentage of total sales for each region and product category
agg = (pivot / total_sales) * 100
agg
```

| Product Category | Clothing  | Electronics |
| ---------------- | --------- | ----------- |
| **Region**           |           |             |
| **East**             | 11.956522 | 7.608696    |
| **North**            | 15.217391 | 10.869565   |
| **South**            | 10.869565 | 22.826087   |
| **West**             | NaN       | 20.652174   |


With the shape of this DataFrame ordering by percentage of total sales is not really possible.

```python
# the stack function lets us reshape the data so we can sort by the percentages
agg.stack().sort_values(ascending=False).head(3)
```


    Region  Product Category
    South   Electronics         22.826087
    West    Electronics         20.652174
    North   Clothing            15.217391
    dtype: float64



# Summary:
Now that you've gone through the tutorial, you've seen how the sales data was analyzed to find the best-selling regions and product categories. The analyst first loaded the data into a Pandas DataFrame and then grouped it by region and product category to calculate total sales for each combination. They then calculated the percentage of total sales for each group, which made it easy to compare performance across different regions and categories. Finally, they sorted the results to identify the top 3 regions and product categories, giving a clear picture of where the company's sales were strongest.

### Key Takeaways:
- **Data Loading:** Use `pd.read_clipboard()` to load data from clipboard into a DataFrame.
- **Data Grouping:** Utilize `df.groupby()` to group data by multiple columns (region and product category).
- **Aggregation:** Apply `sum()` to calculate total sales for each group.
- **Data Reshaping:** Employ `reset_index()` to flatten grouped data and pd.pivot_table() for alternative data representation.
- **Percentage Calculation:** Calculate percentages of total sales using (grouped_sum / total_sales) * 100.
- **Sorting and Ranking:** Use `sort_values()` and `head()` to identify top-performing regions and product categories.
- **Data Transformation:** Apply `stack()` to reshape pivoted data for easier sorting.















