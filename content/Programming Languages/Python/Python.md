Python is by far my favorite programming language. I have been able to do so much with it: [[automation]], [[Web Programming]], [[Data Analysis]], [[Data wrangling]], etc. I was the kind of person that would first try to do a programming task in Python and ignore the rest. Just in the last few years, specially after the release of Chat GPT, I have changed my mind. I know am less concerned on what programming language I use, and simply code in the language that is needed for the task. Never the less, I am still a big fan of the entire Python ecosystem.

# Basic Notepad++ Settings
In general I have used very basic methods to writing code and Notepad++ has been my favorite. I also have heavily made use of the [[Jupyter Notebook]].

## Inconsistent Indentation
If you are having issues running Python scripts and the error mentions issues related to "inconsistent indentation", this usually means your notepad++ file is mixing tabs and spaces.

To see if your file has this issue, go to View > Show Symbol > Show White Space and TAB. If you see both tabs and spaces then that is your issue. Make sure you only use spaces.

![[Pasted image 20240315103922.png]]

## Python Tab Settings
- Go to Settings > Preferences > Language
- Tab Settings, select python
- Change "Use default value" to "Replace by space"

![[Pasted image 20240315104349.png]]

# Running a Basic Python Script
In certain job environments, double-clicking a .py file will not work for you. I have found that using [[Windows Powershell]] to run the [[Python]] file has provided me a much more consistent result. Create the two files below and place them in the same directory.

If you double-click the PowerShell script, this will run your Python file and you should see the "hello world" message.

**example.py**
``` python
print('hello world')
```

**RUN_script.cmd**
``` bash
@ECHO OFF
SET PATH=%PATH%;"C:\Program Files\Python"
python example.py

PAUSE
```

# Imports
Here we focus on how to import Python libraries. In most of the scripts you write, you will need to import certain libraries at the top of your code in order to have access to them. Don't worry if you do not know what these libraries do, the important thing is to notice how these libraries are imported.

``` python
# basic way to import a library
import os

# you can give your libraries as alias
import unittest as test

# you can import specific functions instead of the entire library
from os import getcwd, remove
```

# Variables
Here we will talk about declaring variables in Python. Note that no data types are need to be associated with variables and that all variables are objects in Python.

``` python
from datetime import datetime

# declare a date variable
current_time = datetime.now()

# declare a number variable
num = 5

# declare a string variable
# you can use single or double quotes
alpha = 'hello world'
```

# Data Structures
Python comes with several data structures or ways to store and work with data.

``` python
# this is a list
data = [0,1,2,3,4,5,6,7,8,9]

# use [x] to access the item at location x in the list
# all lists start at 0
print('first item', data[0])

# you can also select from the back of the list
# -1 will get you the last item in the list
# -2 for "second from last"
print('last item', data[-1])

# you can "slice" a list using : and ::
print('first three items', data[:3])
print('last three items', data[-3:])
print('start at the fourth item', [3:])
print('the odd items', data[::2])

# all lists have a length, use len(list name)
# mathematical functions can also, in general, be applied to lists if they contain numbers
print('length of list', len(data))
print('largest number in the list', max(data))
print('smallest number', min(data))
print('sum', sum(data))

# we can find the index of the max and min using argmax() and argmin()
print('the largest number in the list is', max(data), 'and is found at index:', argmax(data))

# items can be added to a list by using list_name.append(item)
# add 3 to the list
data.append(3)

# add 4 
data.append(4)
print(data)

# finally, we can de-dupe a list and sort
data.sort()
print('sorted list', data)
print('select distinct values', list(set(data)))

# items can be removed from the list using list_name.remove(item)
# remove 3 from the list
data.remove(3)

# remove 4
data.remove(4)
print(data)
```

There are also dictionaries and tuples. Feel free to use Chat GPT to learn more about them. Out of these two, tuples are probably used less frequently.

# Conditional Statements
Here are some examples of if/else statements

``` python
if 1 == 1:
	print('one equals one')
	
if i < 0:
	print('one is less than zero')
else:
	print('1 does not equal 0')

if 1 != 1:
	print('one does not equal one')
elif 1 == 0:
	print('1 is equal to zero')
else:
	print('1 does not equal to 0')

if (1 == 1 and 0 < 1):
	print('and operator')

if (1 == 1 or 0 == 1):
	print('or operator')
```

# Looping

``` python
# we can iterate over n items using a for loop
# a shortcut for making the list [0,...,n-1]  is the function range(n)

# print the numbers 0-4
for i in range(5):
	print(i)

# print the numbers 0-4
for i in range(0,5):
	print(i)

# iterating over something and appending is a common way of building lists 
# create array
output = []

# build the list by using a for loop
for i in range(5):
	output.append(i**2) # **2 operator means squared
print(output)

# this works but is slow, a faster way to do this is to use a lst comprehension
output2 = [i**2 for i in range(5)]
print(output2)

# we can also put conditions in the list comprehension
# build the first 10 squares for all even numbers
output3 = [i**2 for i in range(10) if i%2==0] # % means modulus (remainder)
print(output3)

# the zip command lines up two lists together
L1 = [1,2,3]
L2 = ['x', 'y', 'z']

# the ouput of a list of tuples
for list1, list2 in zip(L1,L2):
	print(list1, list2)

# this can also be done with list comprehension
print([(x,y,str(x)+y) for x,y in zip(L1,L2)])

# we can also make more complex lists
output = [(x,y,str(x)+y) for x,y in zip(L1,L2)]

# iterate over our output for a nicer looking print statement
for z in output:
	print(z)

# we can also do this differently 
for a1, a2, a3 in output:
	print(a1,a2,a3)

# WHILE Statements

# counter
i = 0

# loop while i < 5
while i < 5:
	print(i)
	
	# increment counter
	i = i + 1
```

# Functions

``` python
# define functions
def simple_add(number):
	return number

def simple_add2(n1, n2):
	return n1 + n2

def simple_add3(n1=2, n2=2):
	return n1 + n2

# return 10
simple_add(10)

# return 2 + 5
simple_add2(2,5)

# return 1 + 3
simple_add3(1,3)

# use default parameters
simple_add3()
```

# Coding Standards
I have always tried to push for the idea that everyone in the team should be following the same coding standards.

I try to follow the PEP 8 style guide: https://peps.python.org/pep-0008/

## Indentation
- Use 4 spaces per indentation level
- Use spaces and not tabs
	- Python disallows mixing tabs and spaces for indentation
	- Make sure Notepad++ is set up to use spaces

## Imports
- Imports are always put at the top of the file
- One library per line

## String Quotes
- In Python, single-quoted strings and double-quoted string are the same
- Try to be consistent

## Comments
- Use block commenting (""" or ''') for documenting functions/classes
- Use single # comments for everything else

## Functions/Variables
- All lowercase names
- Use underscores to improve readability
- Use all caps for CONSTANTS
- Use CamelCase for classes

## Folder Structure
Here is a basic folder structure if you are writing an application. There are many variations in the wild, use what works for you.

Project/
|--app.cmd
|--tests.cmd
|--config/
|--docs/
|--lib/
|--scripts/
|--spool/
|--tests/

- **Project** - Main folder, you can use any name you want here
- **app.cm**d - PowerShell command to run application
- **tests.cmd** - PowerShell command to run all tests
- **config** - Folder that contains all configuration files
- **docs** - Folder that contains all documentation files
- **lib** - Folder that contains all Python files
- **scripts** - Folder that contains all SQL files
- **spool** - Folder that contains all SQL spooled files
- **tests** - Folder that contains all test files

# Libraries I have used in the past
* [[Pulp]]
* [[Pandas]]
* [[sqlite3]]
* [[matplotlib]]
* [[numpy]]
* [[tornado]]
* [[talib]]
* [[scipy]]
* [[redis]]
* [[reportlab]]
* [[sqlalchemy]]
* [[psycopg2]]
* [[smtplib]]
* [[email]]
* [[datetime]]
* [[statsmodels]]
* [[json]]
* [[time]]
* [[logging]]
* [[sys]]
* [[urllib2]]
* [[urllib]]
* [[itertools]]
* [[sklearn]]
* [[BeautifulSoup]]
* [[jinja2]]
* [[glob]]
* [[requests]]
* [[subprocess]]
* [[os]]
* [[pyodbc]]
* [[bs4]]
* [[re]]
* [[io]]
* [[tkinter]]
* [[csv]]
* [[Music21]]
* [[SimPy]]
* [[pil]]
* [[mpl_toolkits]]
* [[bokeh]]
* [[collections]]
* [[math]]
* [[argparse]]
* [[folium]]
* [[StringIO]]
* [[mpld3]]
* [[networkx]]
* [[seaborn]]
* [[sas7bdat]]
* [[random]]
