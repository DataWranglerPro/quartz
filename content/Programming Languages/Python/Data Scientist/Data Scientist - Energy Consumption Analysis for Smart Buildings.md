
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/ac5995c65721a23dfd12fa910265b0a35b3b8891/content/Assets/notebooks/energy_consumption_analysis.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

### Description:  

As a data scientist at a facility management company, you're tasked with analyzing energy consumption patterns across different buildings and floors. The dataset contains energy usage data for various devices (lights, ACs, elevators) on each floor of three buildings.  

### Your goal is to:  

- Reshape the data to facilitate analysis by building and device type.  
- Calculate the total energy consumption for each building and device type.  

```python
# import libraries
import pandas as pd
import numpy as np
import sys

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

The generated data simulates energy consumption readings for various devices across different floors in multiple buildings.  

**Here's a breakdown of each column:**  
- **Building:** The name of the building (e.g., "Building 1", "Building 2", "Building 3")  
- **Floor:** The floor number within a building (e.g., "Floor 1", "Floor 2", ..., "Floor 5")  
- **Device:** The type of device consuming energy (e.g., "Lights", "ACs", "Elevators")  
- **Date:** The date of the energy consumption reading (e.g., "2022-01-01", "2022-01-02", ..., "2022-01-10")  
- **Energy_Usage:** The amount of energy consumed by the device on a specific floor in a building on a particular date (a random value between 0 and 100)  


```python
# set the seed
np.random.seed(0)

buildings = ['Building 1', 'Building 2', 'Building 3']
floors = ['Floor {}'.format(i) for i in range(1, 4)]
devices = ['Lights', 'ACs', 'Elevators']
dates = pd.date_range('2022-01-01', '2022-01-10')
energy_usage = np.random.uniform(0, 100, size=(len(buildings) * len(floors) * len(devices) * len(dates)))

data = {
    'Building': np.repeat(buildings, len(floors) * len(devices) * len(dates)),
    'Floor': np.repeat(floors, len(floors) * len(devices) * len(dates)),
    'Device': np.repeat(devices, len(floors) * len(devices) * len(dates)),
    'Date': np.tile(dates, len(buildings) * len(floors) * len(devices)),
    'Energy_Usage': energy_usage
}

df = pd.DataFrame(data)
df
```

|     | Building   | Floor   | Device    | Date       | Energy_Usage |
| --- | ---------- | ------- | --------- | ---------- | ------------ |
| 0   | Building 1 | Floor 1 | Lights    | 2022-01-01 | 54.881350    |
| 1   | Building 1 | Floor 1 | Lights    | 2022-01-02 | 71.518937    |
| 2   | Building 1 | Floor 1 | Lights    | 2022-01-03 | 60.276338    |
| 3   | Building 1 | Floor 1 | Lights    | 2022-01-04 | 54.488318    |
| 4   | Building 1 | Floor 1 | Lights    | 2022-01-05 | 42.365480    |
| ... | ...        | ...     | ...       | ...        | ...          |
| 265 | Building 3 | Floor 3 | Elevators | 2022-01-06 | 78.515291    |
| 266 | Building 3 | Floor 3 | Elevators | 2022-01-07 | 28.173011    |
| 267 | Building 3 | Floor 3 | Elevators | 2022-01-08 | 58.641017    |
| 268 | Building 3 | Floor 3 | Elevators | 2022-01-09 | 6.395527     |
| 269 | Building 3 | Floor 3 | Elevators | 2022-01-10 | 48.562760    |

270 rows × 5 columns

# Reshape the Data  

This section shows various ways to reshape the data for analysis.  

### Using groupby and sum

The code below groups the data by four columns: Building, Floor, Device, and Date. The GroupBy function creates a GroupBy object that contains the grouped data. The sum method is then applied to calculate the sum of the energy consumption values for each group.

```python
df.groupby(['Building', 'Floor', 'Device', 'Date']).sum()
```

|                |             |               |            | Energy_Usage |
| -------------- | ----------- | ------------- | ---------- | ------------ |
| **Building**   | **Floor**   | **Device**    | **Date**   |              |
| **Building 1** | **Floor 1** | **Lights**    | 2022-01-01 | 496.682940   |
|                |             |               | 2022-01-02 | 468.639934   |
|                |             |               | 2022-01-03 | 547.168084   |
|                |             |               | 2022-01-04 | 441.721382   |
|                |             |               | 2022-01-05 | 300.984595   |
|                |             |               | 2022-01-06 | 349.582977   |
|                |             |               | 2022-01-07 | 370.379375   |
|                |             |               | 2022-01-08 | 397.945201   |
|                |             |               | 2022-01-09 | 569.918664   |
|                |             |               | 2022-01-10 | 410.219459   |
| **Building 2** | **Floor 2** | **ACs**       | 2022-01-01 | 505.124086   |
|                |             |               | 2022-01-02 | 445.748871   |
|                |             |               | 2022-01-03 | 417.843884   |
|                |             |               | 2022-01-04 | 531.061226   |
|                |             |               | 2022-01-05 | 504.501020   |
|                |             |               | 2022-01-06 | 498.474526   |
|                |             |               | 2022-01-07 | 391.778812   |
|                |             |               | 2022-01-08 | 490.505067   |
|                |             |               | 2022-01-09 | 580.186339   |
|                |             |               | 2022-01-10 | 364.295473   |
| **Building 3** | **Floor 3** | **Elevators** | 2022-01-01 | 420.827066   |
|                |             |               | 2022-01-02 | 398.878300   |
|                |             |               | 2022-01-03 | 389.512838   |
|                |             |               | 2022-01-04 | 425.916186   |
|                |             |               | 2022-01-05 | 440.269651   |
|                |             |               | 2022-01-06 | 457.216523   |
|                |             |               | 2022-01-07 | 422.345950   |
|                |             |               | 2022-01-08 | 371.467637   |
|                |             |               | 2022-01-09 | 430.878622   |
|                |             |               | 2022-01-10 | 505.755293   |

### Using pivot_table  

This line of code uses the pivot_table function to reshape the data. It sets the index as a combination of Building and Floor, and the columns as the different Device types. The values parameter specifies that the energy consumption values should be used, and the aggfunc parameter is set to 'count' to count the number of observations for each device type.

```python
df.pivot_table(index=['Building', 'Floor'], columns='Device', values='Energy_Usage', aggfunc='count')
```

|            | Device  | ACs  | Elevators | Lights |
| ---------- | ------- | ---- | --------- | ------ |
| Building   | Floor   |      |           |        |
| Building 1 | Floor 1 | NaN  | NaN       | 90.0   |
| Building 2 | Floor 2 | 90.0 | NaN       | NaN    |
| Building 3 | Floor 3 | NaN  | 90.0      | NaN    |


Similar to the previous cell, this code uses pivot_table to reshape the data. It sets the index as the Date column, and the columns as the different Device types. The values parameter specifies that the energy consumption values should be used, and the aggfunc parameter is set to 'sum' to calculate the total energy consumption for each device type on each date.

```python
df.pivot_table(index=['Date'], columns='Device', values='Energy_Usage', aggfunc='sum')
```

| Device     | ACs        | Elevators  | Lights     |
| ---------- | ---------- | ---------- | ---------- |
| Date       |            |            |            |
| 2022-01-01 | 505.124086 | 420.827066 | 496.682940 |
| 2022-01-02 | 445.748871 | 398.878300 | 468.639934 |
| 2022-01-03 | 417.843884 | 389.512838 | 547.168084 |
| 2022-01-04 | 531.061226 | 425.916186 | 441.721382 |
| 2022-01-05 | 504.501020 | 440.269651 | 300.984595 |
| 2022-01-06 | 498.474526 | 457.216523 | 349.582977 |
| 2022-01-07 | 391.778812 | 422.345950 | 370.379375 |
| 2022-01-08 | 490.505067 | 371.467637 | 397.945201 |
| 2022-01-09 | 580.186339 | 430.878622 | 569.918664 |
| 2022-01-10 | 364.295473 | 505.755293 | 410.219459 |

## What other ways can you come up with to reshape the data?