
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/analyzing_student_performance.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

**Description:** You are a data analyst at a school, and you need to analyze the performance of students in a mathematics exam. The school has provided you with a dataset containing the scores of 50 students in three subjects: Algebra, Geometry, and Calculus. 

**Your task is to:**
- Load the dataset into a Pandas DataFrame
- Calculate the average score for each subject
- Identify the top 5 students with the highest overall score (average of all three subjects)
- Create a new column to indicate whether each student passed or failed the exam (passing score is 80 or higher)

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

The dataset contains information about the performance of 50 students in a mathematics exam, covering three subjects: Algebra, Geometry, and Calculus. 

### Columns:
- **Student_ID:** A unique identifier for each student (integer).  
- **Algebra:** The student's score in Algebra (integer).  
- **Geometry:** The student's score in Geometry (integer).  
- **Calculus:** The student's score in Calculus (integer).  

```
Student_ID	Algebra	Geometry	Calculus
1	85	90	78
2	92	88	95
3	78	75	82
4	95	92	89
5	88	85	92
6	76	78	85
7	89	91	96
8	83	80	88
9	90	95	92
10	81	83	86
11	86	89	93
12	93	96	91
13	84	82	89
14	91	94	97
15	79	81	87
16	87	86	90
17	94	97	95
18	82	84	91
19	96	98	99
20	80	79	83
21	98	99	100
22	75	77	81
23	92	93	98
24	89	92	95
25	77	76	80
26	95	96	98
27	81	82	87
28	90	91	94
29	78	80	84
30	97	99	100
31	84	86	90
32	91	94	97
33	76	78	82
34	88	90	93
35	82	84	89
36	96	98	100
37	85	87	92
38	79	81	86
39	93	95	98
40	80	82	85
41	87	89	94
42	94	96	99
43	83	85	91
44	92	94	97
45	77	79	83
46	90	92	95
47	86	88	93
48	98	100	100
49	81	83	88
50	95	97	99
```


```python
df = pd.read_clipboard()
df
```

|     | Student_ID | Algebra | Geometry | Calculus |
| --- | ---------- | ------- | -------- | -------- |
| 0   | 1          | 85      | 90       | 78       |
| 1   | 2          | 92      | 88       | 95       |
| 2   | 3          | 78      | 75       | 82       |
| 3   | 4          | 95      | 92       | 89       |
| 4   | 5          | 88      | 85       | 92       |
| 5   | 6          | 76      | 78       | 85       |
| 6   | 7          | 89      | 91       | 96       |
| 7   | 8          | 83      | 80       | 88       |
| 8   | 9          | 90      | 95       | 92       |
| 9   | 10         | 81      | 83       | 86       |
| 10  | 11         | 86      | 89       | 93       |
| 11  | 12         | 93      | 96       | 91       |
| 12  | 13         | 84      | 82       | 89       |
| 13  | 14         | 91      | 94       | 97       |
| 14  | 15         | 79      | 81       | 87       |
| 15  | 16         | 87      | 86       | 90       |
| 16  | 17         | 94      | 97       | 95       |
| 17  | 18         | 82      | 84       | 91       |
| 18  | 19         | 96      | 98       | 99       |
| 19  | 20         | 80      | 79       | 83       |
| 20  | 21         | 98      | 99       | 100      |
| 21  | 22         | 75      | 77       | 81       |
| 22  | 23         | 92      | 93       | 98       |
| 23  | 24         | 89      | 92       | 95       |
| 24  | 25         | 77      | 76       | 80       |
| 25  | 26         | 95      | 96       | 98       |
| 26  | 27         | 81      | 82       | 87       |
| 27  | 28         | 90      | 91       | 94       |
| 28  | 29         | 78      | 80       | 84       |
| 29  | 30         | 97      | 99       | 100      |
| 30  | 31         | 84      | 86       | 90       |
| 31  | 32         | 91      | 94       | 97       |
| 32  | 33         | 76      | 78       | 82       |
| 33  | 34         | 88      | 90       | 93       |
| 34  | 35         | 82      | 84       | 89       |
| 35  | 36         | 96      | 98       | 100      |
| 36  | 37         | 85      | 87       | 92       |
| 37  | 38         | 79      | 81       | 86       |
| 38  | 39         | 93      | 95       | 98       |
| 39  | 40         | 80      | 82       | 85       |
| 40  | 41         | 87      | 89       | 94       |
| 41  | 42         | 94      | 96       | 99       |
| 42  | 43         | 83      | 85       | 91       |
| 43  | 44         | 92      | 94       | 97       |
| 44  | 45         | 77      | 79       | 83       |
| 45  | 46         | 90      | 92       | 95       |
| 46  | 47         | 86      | 88       | 93       |
| 47  | 48         | 98      | 100      | 100      |
| 48  | 49         | 81      | 83       | 88       |
| 49  | 50         | 95      | 97       | 99       |

```python
# make sure data types look good
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 50 entries, 0 to 49
    Data columns (total 4 columns):
     #   Column      Non-Null Count  Dtype
    ---  ------      --------------  -----
     0   Student_ID  50 non-null     int64
     1   Algebra     50 non-null     int64
     2   Geometry    50 non-null     int64
     3   Calculus    50 non-null     int64
    dtypes: int64(4)
    memory usage: 1.7 KB
    


```python
# calculate the average score for each subject
df['median'] = df[['Algebra', 'Geometry', 'Calculus']].median(axis=1) # I usually choose the median over the average

# identify the top 5 students with the highest overall score (average of all three subjects)
df.sort_values(by='median', ascending=False).head()
```

|     | Student_ID | Algebra | Geometry | Calculus | median |
| --- | ---------- | ------- | -------- | -------- | ------ |
| 47  | 48         | 98      | 100      | 100      | 100.0  |
| 29  | 30         | 97      | 99       | 100      | 99.0   |
| 20  | 21         | 98      | 99       | 100      | 99.0   |
| 18  | 19         | 96      | 98       | 99       | 98.0   |
| 35  | 36         | 96      | 98       | 100      | 98.0   |


```python
# create a new column to indicate whether each student passed or failed the exam (passing score is 80 or higher)
df['passFail'] = df['median'].apply(lambda x: "pass" if x >= 80 else "fail")
df
```

|     | Student_ID | Algebra | Geometry | Calculus | median | passFail |
| --- | ---------- | ------- | -------- | -------- | ------ | -------- |
| 0   | 1          | 85      | 90       | 78       | 85.0   | pass     |
| 1   | 2          | 92      | 88       | 95       | 92.0   | pass     |
| 2   | 3          | 78      | 75       | 82       | 78.0   | fail     |
| 3   | 4          | 95      | 92       | 89       | 92.0   | pass     |
| 4   | 5          | 88      | 85       | 92       | 88.0   | pass     |
| 5   | 6          | 76      | 78       | 85       | 78.0   | fail     |
| 6   | 7          | 89      | 91       | 96       | 91.0   | pass     |
| 7   | 8          | 83      | 80       | 88       | 83.0   | pass     |
| 8   | 9          | 90      | 95       | 92       | 92.0   | pass     |
| 9   | 10         | 81      | 83       | 86       | 83.0   | pass     |
| 10  | 11         | 86      | 89       | 93       | 89.0   | pass     |
| 11  | 12         | 93      | 96       | 91       | 93.0   | pass     |
| 12  | 13         | 84      | 82       | 89       | 84.0   | pass     |
| 13  | 14         | 91      | 94       | 97       | 94.0   | pass     |
| 14  | 15         | 79      | 81       | 87       | 81.0   | pass     |
| 15  | 16         | 87      | 86       | 90       | 87.0   | pass     |
| 16  | 17         | 94      | 97       | 95       | 95.0   | pass     |
| 17  | 18         | 82      | 84       | 91       | 84.0   | pass     |
| 18  | 19         | 96      | 98       | 99       | 98.0   | pass     |
| 19  | 20         | 80      | 79       | 83       | 80.0   | pass     |
| 20  | 21         | 98      | 99       | 100      | 99.0   | pass     |
| 21  | 22         | 75      | 77       | 81       | 77.0   | fail     |
| 22  | 23         | 92      | 93       | 98       | 93.0   | pass     |
| 23  | 24         | 89      | 92       | 95       | 92.0   | pass     |
| 24  | 25         | 77      | 76       | 80       | 77.0   | fail     |
| 25  | 26         | 95      | 96       | 98       | 96.0   | pass     |
| 26  | 27         | 81      | 82       | 87       | 82.0   | pass     |
| 27  | 28         | 90      | 91       | 94       | 91.0   | pass     |
| 28  | 29         | 78      | 80       | 84       | 80.0   | pass     |
| 29  | 30         | 97      | 99       | 100      | 99.0   | pass     |
| 30  | 31         | 84      | 86       | 90       | 86.0   | pass     |
| 31  | 32         | 91      | 94       | 97       | 94.0   | pass     |
| 32  | 33         | 76      | 78       | 82       | 78.0   | fail     |
| 33  | 34         | 88      | 90       | 93       | 90.0   | pass     |
| 34  | 35         | 82      | 84       | 89       | 84.0   | pass     |
| 35  | 36         | 96      | 98       | 100      | 98.0   | pass     |
| 36  | 37         | 85      | 87       | 92       | 87.0   | pass     |
| 37  | 38         | 79      | 81       | 86       | 81.0   | pass     |
| 38  | 39         | 93      | 95       | 98       | 95.0   | pass     |
| 39  | 40         | 80      | 82       | 85       | 82.0   | pass     |
| 40  | 41         | 87      | 89       | 94       | 89.0   | pass     |
| 41  | 42         | 94      | 96       | 99       | 96.0   | pass     |
| 42  | 43         | 83      | 85       | 91       | 85.0   | pass     |
| 43  | 44         | 92      | 94       | 97       | 94.0   | pass     |
| 44  | 45         | 77      | 79       | 83       | 79.0   | fail     |
| 45  | 46         | 90      | 92       | 95       | 92.0   | pass     |
| 46  | 47         | 86      | 88       | 93       | 88.0   | pass     |
| 47  | 48         | 98      | 100      | 100      | 100.0  | pass     |
| 48  | 49         | 81      | 83       | 88       | 83.0   | pass     |
| 49  | 50         | 95      | 97       | 99       | 97.0   | pass     |

# BONUS

```python
def pass_fail(score):
    if score >= 80:
        return "pass"
    else:
        return "fail"

# calculate pass fail on all 3 subjects
label = df[['Algebra', 'Geometry', 'Calculus']].map(pass_fail)
label.head()
```

|     | Algebra | Geometry | Calculus |
| --- | ------- | -------- | -------- |
| 0   | pass    | pass     | fail     |
| 1   | pass    | pass     | pass     |
| 2   | fail    | fail     | pass     |
| 3   | pass    | pass     | pass     |
| 4   | pass    | pass     | pass     |


```python
# merge the two dataframes
df.merge(right=label,left_index=True, right_index=True)
```

|     | Algebra | Geometry | Calculus |
| --- | ------- | -------- | -------- |
| 0   | pass    | pass     | fail     |
| 1   | pass    | pass     | pass     |
| 2   | fail    | fail     | pass     |
| 3   | pass    | pass     | pass     |
| 4   | pass    | pass     | pass     |

# Summary:  
The tutorial demonstrated how to analyze a dataset of student performance in a mathematics exam using Pandas. It covered importing libraries, loading data, checking data types, calculating average scores, identifying top performers, and creating new columns to indicate pass/fail status.  

# Key Takeaways:
- Loading data from clipboard into a Pandas DataFrame
- Checking data types and info using `df.info()` and `df.head()`
- Calculating median/average scores using `df.median()` or `df.mean()`
- Creating new columns using `df['new_column']`
- Sorting data using `df.sort_values()` and selecting top rows using `df.head()`
- Applying conditional logic using `apply()` and lambda functions (e.g., pass/fail status)
- Merging DataFrames using `df.merge()`
- Using map function to apply pass/fail logic to individual subjects

















