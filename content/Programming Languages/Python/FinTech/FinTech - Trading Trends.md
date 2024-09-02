
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/trading_trends.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

### Description:
Imagine you're a fintech professional working for a leading investment firm. Your task is to analyze trading data to identify market trends and optimize investment strategies.  

### Tasks:
- **Reshape and Pivot:** Reshape the data to create a pivot table that shows the average open_price and close_price for each stock_symbol on a monthly basis. Use the trade_date column to extract the month.
- **Data Merging:** Merge the trading_data with another dataset, stock_info, which contains additional information about each stock. The stock_info dataset has the following columns: stock_symbol, sector, and industry. Merge the two datasets on the stock_symbol column and create a new column, sector_average, which calculates the average close_price for each sector-industry.
- **Feature Engineering:** Create a new column, price_change, which calculates the daily percentage change in close_price for each stock. Then, create another column, trend, which categorizes the price_change into three groups: 'Up' (above 1%), 'Down' (below -1%), and 'Neutral' (between -1% and 1%).

```python
# import libraries
import pandas as pd
import numpy as np
import sys

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
print('Numpy version ' + np.__version__)
```

    Python version 3.11.7 | packaged by Anaconda, Inc. | (main, Dec 15 2023, 18:05:47) [MSC v.1916 64 bit (AMD64)]
    Pandas version 2.2.1
    Numpy version 1.26.4
    

# The Data  

The dataset, trading_data, contains 1,830 rows of trading information for various stocks over a year.  

# Columns:
**stock_symbol:** Unique stock identifier  
**trade_date:** Date of the trade  
**open_price:** Stock price at market open  
**high_price:** Highest stock price of the day  
**low_price	Lowest:** stock price of the day  
**close_price:** Stock price at market close  
**volume:** Number of shares traded  

```python
# set the seed
np.random.seed(0)

# generate trading data
trade_date = pd.date_range('2023-01-01', '2024-01-01', freq='D')
stock_symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'FB']
open_price = np.random.uniform(100, 500, size=(len(trade_date), len(stock_symbols)))
high_price = open_price + np.random.uniform(0, 50, size=(len(trade_date), len(stock_symbols)))
low_price = open_price - np.random.uniform(0, 50, size=(len(trade_date), len(stock_symbols)))
close_price = open_price + np.random.uniform(-20, 20, size=(len(trade_date), len(stock_symbols)))
volume = np.random.randint(10000, 100000, size=(len(trade_date), len(stock_symbols)))

trading_data = pd.DataFrame({
    'trade_date': np.repeat(trade_date, len(stock_symbols)),
    'stock_symbol': np.tile(stock_symbols, len(trade_date)),
    'open_price': open_price.flatten(),
    'high_price': high_price.flatten(),
    'low_price': low_price.flatten(),
    'close_price': close_price.flatten(),
    'volume': volume.flatten()
})

# generate stock info data
stock_info = pd.DataFrame({
    'stock_symbol': stock_symbols,
    'sector': ['Tech', 'Tech', 'Tech', 'Tech', 'Tech'],
    'industry': ['Software', 'Internet', 'Software', 'E-commerce', 'Social Media']
})
```

Let us take a look at the data and the data types.
```python
trading_data.head()
```

|     | trade_date | stock_symbol | open_price | high_price | low_price  | close_price | volume |
| --- | ---------- | ------------ | ---------- | ---------- | ---------- | ----------- | ------ |
| 0   | 2023-01-01 | AAPL         | 319.525402 | 335.210154 | 292.730235 | 331.208465  | 59105  |
| 1   | 2023-01-01 | GOOG         | 386.075747 | 411.696171 | 340.855887 | 392.998029  | 12378  |
| 2   | 2023-01-01 | MSFT         | 341.105350 | 356.190429 | 326.361387 | 338.673429  | 82360  |
| 3   | 2023-01-01 | AMZN         | 317.953273 | 361.044423 | 302.510066 | 318.140688  | 30510  |
| 4   | 2023-01-01 | FB           | 269.461920 | 311.678270 | 238.102758 | 285.304010  | 22898  |

```python
trading_data.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1830 entries, 0 to 1829
    Data columns (total 7 columns):
     #   Column        Non-Null Count  Dtype         
    ---  ------        --------------  -----         
     0   trade_date    1830 non-null   datetime64[ns]
     1   stock_symbol  1830 non-null   object        
     2   open_price    1830 non-null   float64       
     3   high_price    1830 non-null   float64       
     4   low_price     1830 non-null   float64       
     5   close_price   1830 non-null   float64       
     6   volume        1830 non-null   int32         
    dtypes: datetime64[ns](1), float64(4), int32(1), object(1)
    memory usage: 93.1+ KB
    


```python
stock_info.head()
```

|     | stock_symbol | sector | industry     |
| --- | ------------ | ------ | ------------ |
| 0   | AAPL         | Tech   | Software     |
| 1   | GOOG         | Tech   | Internet     |
| 2   | MSFT         | Tech   | Software     |
| 3   | AMZN         | Tech   | E-commerce   |
| 4   | FB           | Tech   | Social Media |


```python
stock_info.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 5 entries, 0 to 4
    Data columns (total 3 columns):
     #   Column        Non-Null Count  Dtype 
    ---  ------        --------------  ----- 
     0   stock_symbol  5 non-null      object
     1   sector        5 non-null      object
     2   industry      5 non-null      object
    dtypes: object(3)
    memory usage: 252.0+ bytes
    

# Reshape and Pivot

Reshape the data to create a pivot table that shows the average open_price and close_price for each stock_symbol on a monthly basis. Use the trade_date column to extract the month.

In order to extract the year and month from a date object, we can make use of the `to_period()` method as shown below.

```python
trading_data['trade_date'].dt.to_period('M')
```

    0       2023-01
    1       2023-01
    2       2023-01
    3       2023-01
    4       2023-01
             ...   
    1825    2024-01
    1826    2024-01
    1827    2024-01
    1828    2024-01
    1829    2024-01
    Name: trade_date, Length: 1830, dtype: period[M]


```python
# reshape the data via pivot_table
pivot = trading_data.pivot_table(index=trading_data['trade_date'].dt.to_period('M'), columns='stock_symbol', values=['open_price','close_price'], aggfunc='mean')
pivot.head()
```

| stock_symbol   | AAPL       | AMZN       | FB         | GOOG       | MSFT       | AAPL       | AMZN       | FB         | GOOG       | MSFT       |
| -------------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| **trade_date** |            |            |            |            |            |            |            |            |            |            |
| **2023-01**    | 296.842894 | 340.198596 | 280.793326 | 292.595610 | 308.192058 | 298.096047 | 338.740435 | 277.524525 | 294.751026 | 303.295615 |
| **2023-02**    | 310.812102 | 296.270349 | 299.107653 | 294.990639 | 290.411256 | 309.474246 | 294.099067 | 301.515984 | 295.286629 | 292.067761 |
| **2023-03**    | 280.517658 | 305.165263 | 306.077719 | 305.371521 | 257.166686 | 281.888576 | 305.294154 | 310.372706 | 305.474469 | 256.246475 |
| **2023-04**    | 262.306455 | 316.037693 | 340.514381 | 286.895555 | 311.488378 | 264.836217 | 316.830908 | 345.158919 | 285.310857 | 309.797786 |
| **2023-05**    | 272.245808 | 275.654902 | 305.448578 | 304.926896 | 283.436121 | 273.720308 | 276.731507 | 302.508553 | 308.299429 | 284.021319 |


# Data Merging

Merge the trading_data with another dataset, stock_info, which contains additional information about each stock. The stock_info dataset has the following columns: stock_symbol, sector, and industry. Merge the two datasets on the stock_symbol column and create a new column, sector_average, which calculates the average close_price for each sector-industry.

```python
# merge the two dataframes
df = trading_data.merge(stock_info, on='stock_symbol')
df.head()
```

|     | trade_date | stock_symbol | open_price | high_price | low_price  | close_price | volume | sector | industry     |
| --- | ---------- | ------------ | ---------- | ---------- | ---------- | ----------- | ------ | ------ | ------------ |
| 0   | 2023-01-01 | AAPL         | 319.525402 | 335.210154 | 292.730235 | 331.208465  | 59105  | Tech   | Software     |
| 1   | 2023-01-01 | GOOG         | 386.075747 | 411.696171 | 340.855887 | 392.998029  | 12378  | Tech   | Internet     |
| 2   | 2023-01-01 | MSFT         | 341.105350 | 356.190429 | 326.361387 | 338.673429  | 82360  | Tech   | Software     |
| 3   | 2023-01-01 | AMZN         | 317.953273 | 361.044423 | 302.510066 | 318.140688  | 30510  | Tech   | E-commerce   |
| 4   | 2023-01-01 | FB           | 269.461920 | 311.678270 | 238.102758 | 285.304010  | 22898  | Tech   | Social Media |


Notice that I used `transform` in order to add the group averages back to the original dataframe.

```python
# create group object
group = df.groupby(['sector','industry'])

# calculate the average close_price for each sector
df['sector_average'] = group['close_price'].transform('mean')
df.head()
```

|     | trade_date | stock_symbol | open_price | high_price | low_price  | close_price | volume | sector | industry     | sector_average |
| --- | ---------- | ------------ | ---------- | ---------- | ---------- | ----------- | ------ | ------ | ------------ | -------------- |
| 0   | 2023-01-01 | AAPL         | 319.525402 | 335.210154 | 292.730235 | 331.208465  | 59105  | Tech   | Software     | 292.958217     |
| 1   | 2023-01-01 | GOOG         | 386.075747 | 411.696171 | 340.855887 | 392.998029  | 12378  | Tech   | Internet     | 298.679561     |
| 2   | 2023-01-01 | MSFT         | 341.105350 | 356.190429 | 326.361387 | 338.673429  | 82360  | Tech   | Software     | 292.958217     |
| 3   | 2023-01-01 | AMZN         | 317.953273 | 361.044423 | 302.510066 | 318.140688  | 30510  | Tech   | E-commerce   | 305.923249     |
| 4   | 2023-01-01 | FB           | 269.461920 | 311.678270 | 238.102758 | 285.304010  | 22898  | Tech   | Social Media | 317.740507     |


If you want to make sure the new column named "sector_average" has the correct number, you can do a quick check using the table below.

```python
group['close_price'].mean()
```

    sector  industry    
    Tech    E-commerce      305.923249
            Internet        298.679561
            Social Media    317.740507
            Software        292.958217
    Name: close_price, dtype: float64


# Feature Engineering

Create a new column, price_change, which calculates the daily percentage change in close_price for each stock. Then, create another column, trend, which categorizes the price_change into three groups: 'Up' (above 1%), 'Down' (below -1%), and 'Neutral' (between -1% and 1%).

```python
# sort the data
sorted_df = trading_data.sort_values(by=['stock_symbol','trade_date'])

# create group object
group = sorted_df.groupby('stock_symbol')

# calculate the price_change for the column close_price
sorted_df['pct_change'] = group['close_price'].transform(lambda x: x.pct_change())
sorted_df.head()
```

|     | trade_date | stock_symbol | open_price | high_price | low_price  | close_price | volume | pct_change |
| --- | ---------- | ------------ | ---------- | ---------- | ---------- | ----------- | ------ | ---------- |
| 0   | 2023-01-01 | AAPL         | 319.525402 | 335.210154 | 292.730235 | 331.208465  | 59105  | NaN        |
| 5   | 2023-01-02 | AAPL         | 358.357645 | 374.130903 | 333.098067 | 373.464608  | 11176  | 0.127582   |
| 10  | 2023-01-03 | AAPL         | 416.690015 | 451.576435 | 377.748453 | 409.149364  | 99861  | 0.095551   |
| 15  | 2023-01-04 | AAPL         | 134.851720 | 173.809416 | 93.355852  | 141.976877  | 96561  | -0.652995  |
| 20  | 2023-01-05 | AAPL         | 491.447337 | 497.050931 | 489.991647 | 471.466975  | 11666  | 2.320731   |


The bins for 'Up' (above 1%), 'Down' (below -1%), and 'Neutral' (between -1% and 1%) would be:
- Down: (-∞, -0.01]
- Neutral: (-0.01, 0.01]
- Up: (0.01, ∞)

```python
bins = [-float('inf'), -0.01, 0.01, float('inf')]
labels = ['Down', 'Neutral', 'Up']

# create the new column named "trend"
sorted_df['trend'] = pd.cut(sorted_df['pct_change'], bins=bins, labels=labels)
sorted_df.head()
```

|     | trade_date | stock_symbol | open_price | high_price | low_price  | close_price | volume | pct_change | trend |
| --- | ---------- | ------------ | ---------- | ---------- | ---------- | ----------- | ------ | ---------- | ----- |
| 0   | 2023-01-01 | AAPL         | 319.525402 | 335.210154 | 292.730235 | 331.208465  | 59105  | NaN        | NaN   |
| 5   | 2023-01-02 | AAPL         | 358.357645 | 374.130903 | 333.098067 | 373.464608  | 11176  | 0.127582   | Up    |
| 10  | 2023-01-03 | AAPL         | 416.690015 | 451.576435 | 377.748453 | 409.149364  | 99861  | 0.095551   | Up    |
| 15  | 2023-01-04 | AAPL         | 134.851720 | 173.809416 | 93.355852  | 141.976877  | 96561  | -0.652995  | Down  |
| 20  | 2023-01-05 | AAPL         | 491.447337 | 497.050931 | 489.991647 | 471.466975  | 11666  | 2.320731   | Up    |

# Summary:  

The tutorial demonstrated how to analyze trading data using Pandas. It covered reshaping and pivoting data, merging datasets, and feature engineering. 

### Key Takeaways:  
- How to reshape and pivot data using `pivot_table` and `dt.to_period`.
- How to merge datasets using `merge` and create new columns using `transform`.
- How to calculate daily percentage changes using `pct_change` and categorize changes using `pd.cut`.
- How to use `groupby` to calculate group averages and add them back to the original dataframe.
- How to sort data by multiple columns using `sort_values`.
- How to use `bins` and `labels` to categorize data into groups.
