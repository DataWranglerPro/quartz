
> [!NOTE] 
> - This tutorial is also available on [nbviewer](https://nbviewer.org/github/DataWranglerPro/quartz/blob/v4/content/Assets/notebooks/university_grades_analysis.ipynb), offering an alternative platform for your learning convenience.
> - 🔥 Free Pandas Course: https://hedaro.gumroad.com/l/tqqfq

### Description  
You are a Data Analyst at a large university, and they need your help. The university's administration wants to analyze student performance in different departments. They have collected data on student grades, majors, and demographics. However, the data is a mess, and the school needs your Pandas skills to clean and analyze it.  

### Tasks  
- **Handle Missing Values:** The dataset contains missing values for some students' grades. Use Pandas to identify and handle these missing values appropriately.  
- **Data Merging:** The data is split into three separate datasets (student info, grades, and courses). Use Pandas to merge these datasets into a single, unified dataset.  
- **Grouping and Aggregation:** Calculate the average grade for each department and major. Find the department with the highest average grade.

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

The dataset contains information about students, their grades, and their demographics.  

### student_info table:  
- **Student ID (int):** Unique identifier for each student
- **Name (str):** Student name
- **Major (str):** Student major (e.g., CS, Math, Physics, Biology)
- **Gender (str):** Student gender (Male or Female)

### grades table:  
- **Student ID (int):** Foreign key referencing the student_info table
- **Course (str):** Course name (e.g., Math 101, CS 202, Physics 303, Biology 404)
- **Grade (float):** Student grade for the course (between 0 and 100)

### courses table:  
- **Course (str):** Course name (e.g., Math 101, CS 202, Physics 303, Biology 404)
- **Department (str):** Department offering the course (e.g., Math, CS, Physics, Biology)

```python
# set the seed
np.random.seed(0)

# student info
student_info = pd.DataFrame({
    'Student ID': range(1000, 2000),
    'Name': ['Student '+str(i) for i in range(1000, 2000)],
    'Major': np.random.choice(['CS', 'Math', 'Physics', 'Biology'], size=1000),
    'Gender': np.random.choice(['Male', 'Female'], size=1000)
})

# grades
grades = pd.DataFrame({
    'Student ID': np.random.choice(range(1000, 2000), size=5000),
    'Course': np.random.choice(['Math 101', 'CS 202', 'Physics 303', 'Biology 404'], size=5000),
    'Grade': np.random.uniform(0, 100, size=5000)
})

# courses
courses = pd.DataFrame({
    'Course': ['Math 101', 'CS 202', 'Physics 303', 'Biology 404'],
    'Department': ['Math', 'CS', 'Physics', 'Biology']
})

# generate missing grades
missing_grades = np.random.choice(range(5000), size=100, replace=False)
grades.loc[missing_grades, 'Grade'] = np.nan
```

# Data Merging:  

The data is split into three separate datasets (student info, grades, and courses). Use Pandas to merge these datasets into a single, unified dataset.

We can merge all three datasets in one line.  
- Merge student_info and grades on the column `Student ID`
- Merge the previously merged dataset with the courses dataset on the column `Course`.

```python
# merge datasets
df = student_info.merge(grades, left_on='Student ID', right_on='Student ID').merge(courses, left_on='Course', right_on='Course')
df.head()
```

|     | Student ID | Name         | Major | Gender | Course   | Grade     | Department |
| --- | ---------- | ------------ | ----- | ------ | -------- | --------- | ---------- |
| 0   | 1000       | Student 1000 | CS    | Female | Math 101 | 21.546156 | Math       |
| 1   | 1000       | Student 1000 | CS    | Female | Math 101 | 63.415641 | Math       |
| 2   | 1000       | Student 1000 | CS    | Female | Math 101 | 51.768279 | Math       |
| 3   | 1000       | Student 1000 | CS    | Female | CS 202   | 67.467882 | CS         |
| 4   | 1000       | Student 1000 | CS    | Female | Math 101 | 6.090085  | Math       |


Let's take a look at the column datatypes and see if we can verify we have null values in the `Grade` column. Do you see the 100 missing grades?

```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 5000 entries, 0 to 4999
    Data columns (total 7 columns):
     #   Column      Non-Null Count  Dtype  
    ---  ------      --------------  -----  
     0   Student ID  5000 non-null   int64  
     1   Name        5000 non-null   object 
     2   Major       5000 non-null   object 
     3   Gender      5000 non-null   object 
     4   Course      5000 non-null   object 
     5   Grade       4900 non-null   float64
     6   Department  5000 non-null   object 
    dtypes: float64(1), int64(1), object(5)
    memory usage: 273.6+ KB
    

# Handle Missing Values

The dataset contains missing values for some students' grades. Use Pandas to identify and handle these missing values appropriately.

For this specific dataset, since the data is completely random, there is no underlying pattern or relationship to rely on to determine what to replace the missing Grades with.  

**Note:** By default, the `dropna()` method examines all columns in a row and removes the entire row if it finds any missing value, which may not be suitable for all situations.

> What techniques have you used in the past to solve a similar problem?

```python
# simply drop the missing values
df = df.dropna()
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 4900 entries, 0 to 4999
    Data columns (total 7 columns):
     #   Column      Non-Null Count  Dtype  
    ---  ------      --------------  -----  
     0   Student ID  4900 non-null   int64  
     1   Name        4900 non-null   object 
     2   Major       4900 non-null   object 
     3   Gender      4900 non-null   object 
     4   Course      4900 non-null   object 
     5   Grade       4900 non-null   float64
     6   Department  4900 non-null   object 
    dtypes: float64(1), int64(1), object(5)
    memory usage: 306.2+ KB
    

# Grouping and Aggregation:  

Calculate the average grade for each department and major. Find the department with the highest average grade.

```python
# Calculate the average grade for each department and major
group = df.groupby(['Department','Major'])

group.mean(numeric_only=True)['Grade']
```


    Department  Major  
    Biology     Biology    49.178208
                CS         49.394462
                Math       49.527255
                Physics    48.719099
    CS          Biology    48.991467
                CS         48.233917
                Math       48.412236
                Physics    50.950611
    Math        Biology    54.027489
                CS         47.204560
                Math       47.157162
                Physics    52.300515
    Physics     Biology    48.697856
                CS         50.947873
                Math       48.599851
                Physics    48.544122
    Name: Grade, dtype: float64



It is pretty interesting that, out of all the departments, the Math department had the highest average grades.

```python
# Find the department with the highest average grade
group = df.groupby('Department')

group.mean(numeric_only=True).sort_values(by='Grade', ascending=False)['Grade'].head(1)
```

    Department
    Math    50.119793
    Name: Grade, dtype: float64


### In this tutorial, you learned how to:  

- **Handle Missing Values:** Identify and handle missing values in a dataset using Pandas. In this case, we simply dropped the missing values using df.dropna().
- **Merge Dataframes:** Merge multiple datasets (student info, grades, and courses) into a single, unified dataset using Pandas' merge function.
- **Group and Aggregate Data:** Calculate the average grade for each department and major using Pandas' groupby and mean functions.
