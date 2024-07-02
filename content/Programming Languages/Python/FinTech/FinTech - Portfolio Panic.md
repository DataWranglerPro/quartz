
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/repayment_mystery.ipynb), offering an alternative platform for your learning convenience.
> - [Pandas Ninja](https://hedaro.gumroad.com/l/jVeRh): Take your skills to the next level with comprehensive Jupyter Notebook tutorials covering dates, group by, plotting, pivot tables, and more. Includes specialized tutorials for Excel and SQL developers, helping you master data analysis with Pandas.

### Description:  
Imagine you're a wealth manager at a prestigious financial firm, responsible for managing a vast portfolio of stocks, bonds, and assets for high-net-worth clients. Your team relies on data analysis to make informed investment decisions, but your current dataset is a mess! You need to wrangle the data to identify trends, optimize performance, and mitigate risk. Can you use your Pandas skills to tame the data beast and save the day?  

### Tasks:  
- **Asset Allocation Analysis:** Identify the top 5 asset classes by total value and calculate their respective weights in the portfolio.
- **Risk Management:** Find the stocks with the highest volatility (highest values in the "Volatility" column) and calculate their average returns.
- **Performance Optimization:** Group the data by sector and calculate the average returns for each sector. Then, identify the top 3 sectors with the highest returns.

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

The dataset represents a portfolio of assets, including stocks, bonds, and other investment vehicles, with information on their sector, value, returns, and volatility. It consists of 1000 rows, with each row representing a single asset and its corresponding attributes.

### Columns:  
- **Asset Class:** The type of asset (Stocks, Bonds, Real Estate, Commodities, Currencies)  
- **Sector:** The industry sector (Technology, Finance, Healthcare, Energy, Consumer Goods)   
- **Stock Symbol:** The stock symbol (AAPL, MSFT, JPM, GOOG, AMZN)  
- **Value:** The current value of the asset  
- **Returns:** The historical returns of the asset  
- **Volatility:** The historical volatility of the asset  

Can you tame the data and help the wealth manager make informed investment decisions?

```python
# set the seed
np.random.seed(0)

# generate the data
data = {
    'Asset Class': np.random.choice(['Stocks', 'Bonds', 'Real Estate', 'Commodities', 'Currencies'], size=1000),
    'Sector': np.random.choice(['Technology', 'Finance', 'Healthcare', 'Energy', 'Consumer Goods'], size=1000),
    'Stock Symbol': np.random.choice(['AAPL', 'MSFT', 'JPM', 'GOOG', 'AMZN'], size=1000),
    'Value': np.random.uniform(1000, 100000, size=1000),
    'Returns': np.random.normal(0.05, 0.1, size=1000),
    'Volatility': np.random.uniform(0.1, 0.5, size=1000)
}

df = pd.DataFrame(data)
df.head()
```

|     | Asset Class | Sector         | Stock Symbol | Value        | Returns   | Volatility |
| --- | ----------- | -------------- | ------------ | ------------ | --------- | ---------- |
| 0   | Currencies  | Energy         | AAPL         | 27148.447388 | 0.080532  | 0.206389   |
| 1   | Stocks      | Technology     | AMZN         | 47770.455686 | 0.152416  | 0.225218   |
| 2   | Commodities | Healthcare     | MSFT         | 81326.560992 | 0.074461  | 0.469665   |
| 3   | Commodities | Consumer Goods | AAPL         | 81746.141057 | -0.027992 | 0.483869   |
| 4   | Commodities | Finance        | MSFT         | 75283.975516 | 0.058908  | 0.139532   |

Let us start by looking at the datatypes and ensure the columns are of the correct type.

```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1000 entries, 0 to 999
    Data columns (total 6 columns):
     #   Column        Non-Null Count  Dtype  
    ---  ------        --------------  -----  
     0   Asset Class   1000 non-null   object 
     1   Sector        1000 non-null   object 
     2   Stock Symbol  1000 non-null   object 
     3   Value         1000 non-null   float64
     4   Returns       1000 non-null   float64
     5   Volatility    1000 non-null   float64
    dtypes: float64(3), object(3)
    memory usage: 47.0+ KB
    

# Asset Allocation Analysis:  

Identify the top 5 asset classes by total value and calculate their respective weights in the portfolio.  

In the first task, "weights" refer to the percentage of the total portfolio value that each asset class represents.  

For example, if the total portfolio value is \$1 million, and the Stocks have a total value of \$400,000, then the weight of the "Stocks" asset class would be 40% (\$400,000 / \$1,000,000).  

So, in this task, you need to calculate the weights for each of the top 5 asset classes by total value, to see how the portfolio is allocated across different asset classes.

```python
# create group object
group = df.groupby('Asset Class')

# add the total value of each asset class and divide it by the total value of the portfolio
group.sum(numeric_only=True)['Value'].div(df['Value'].sum()) * 100
```

    Asset Class
    Bonds          19.516817
    Commodities    22.715469
    Currencies     18.970236
    Real Estate    19.340309
    Stocks         19.457170
    Name: Value, dtype: float64


# Risk Management:  

Find the stocks with the highest volatility (highest values in the "Volatility" column) and calculate their average returns.  

```python
# create group object
group = df.groupby('Stock Symbol')

group.agg(
     avg_volatility=pd.NamedAgg(column="Volatility", aggfunc="mean"),
     avg_returns=pd.NamedAgg(column="Returns", aggfunc="mean")
)
```

|                  | avg_volatility | avg_returns |
| ---------------- | -------------- | ----------- |
| **Stock Symbol** |                |             |
| **AAPL**         | 0.292839       | 0.041167    |
| **AMZN**         | 0.290529       | 0.044325    |
| **GOOG**         | 0.306020       | 0.041320    |
| **JPM**          | 0.302877       | 0.051169    |
| **MSFT**         | 0.289748       | 0.054646    |

I decided to calculate the average volatility for all of the stocks since there are only 5 in this dataset.  

JPMorgan and Google seem to have the most volitility, but in general, all 5 have similar figures.

# Performance Optimization:  

Group the data by sector and calculate the average returns for each sector. Then, identify the top 3 sectors with the highest returns.

```python
# create group object
group = df.groupby('Sector')

# get the average returns and select the top 3
group.mean(numeric_only=True).sort_values(by='Returns', ascending=False)['Returns'].head(3)
```

    Sector
    Healthcare        0.065089
    Consumer Goods    0.054472
    Technology        0.043236
    Name: Returns, dtype: float64


# Summary  

The analysis revealed the 5 asset classes, with weights ranging from 19% to 23%. JPMorgan and Google were identified as the most volatile stocks, with average returns between 4% and 5%. Healthcare, Consumer Goods, and Technology emerged as the top-performing sectors, with returns between 4% and 7%. 

### Key Takeaways:  
- Grouping data by asset class, stock symbol, and sector
- Calculating weights, average volatility, and average returns
- Identifying top asset classes, stocks with high volatility, and top-performing sectors
- Using Pandas functions: groupby, sum, div, agg, mean, sort_values, and head
