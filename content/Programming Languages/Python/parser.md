At work I had the task to reverse engineer some .csv files. I was given a folder with hundreds of .txt files and then asked to convert these into .csv files.

Below is an example of what these text files looked like:
``` txt
111111111 firstmiddlelast 3054444444huerfyher6fr643g 0 0
```

As you can tell from the data above, some of it makes sense and some of it is a bit cryptic. The real data (I obviously cannot post it here) was much longer and even more confusing. 

What made the task challenging was that I could not simply parse the string via a delimiter. These were fixed length data files and I needed to know the specifications of each column to properly parse it.

**Side Note:** I did try to get the information via meetings and SMEs, but that ended up fruitless.

Luckily the java code that parsed these text files told me how to parse it. Yay!

This is how the code looked like for one data element:
``` java
// last name starts at position 61 and ends at position 80
lstName = getField(61, 20)
```

Now that I have all the data I need to parse the text files, lets write some Python code.

``` python
import os
import csv

def main(p_path):
	''' Loop through all the files in fodler '''
	# loop through all the folders
	for (path1, dirs1, files1):
		# read text file
		with open (path1 + '/' + file1, 'r', encoding='UTF-8') as file:
			# loop through each line
			for line in file:
				# ignore lines that do not equal 80
				if len(line) != 80:
					print(file1 + " invalid length of " + str(len(line)))
					continue
				parsed = list(slices(line, 9,1,10,40,20))
				final = parsed
				final.insert(0, file1)
				with open('david.csv', 'a', newline='') as csvfile:
					f = csv.writer(csvfile, delimiter=',')
					f.writerow(final)

def slices(s, *args):
	''' get substring of length n '''
	position = 0
	for length in args:
		yield s[position:position + length]
		position += length

if __name__ == "__main__":
	main(r'C:\Users\david\convertMe)
```

Everything in the Python code is pretty standard. We loop through all the files in a folder, open the text files one at a time, and we read the data in each file line by line. I did add a condition to skip a file that the line is not of length 80. I am expecting all of the lines to be exactly 80 characters long, so any files that do not meet this criteria will be ignored.

The slices function may be the only piece that at first looks a bit confusing. The (star)args parameter allows me to pass as many parameters to the slices function as I want. Remember that these numbers simply represent the length of the data element in the string. Let's walk through the code a bit so you get the idea.

``` python
# simple example
list(slices('The slices function', 4,7,8))
```

If we run the code above, what will we get?...
``` python
['The ', 'slices ', 'function']
```

- 'The ' is of length 4
- 'slices  ' is of length 7
- 'function' is of length 8

The code will get the substring from position 0 to position (0+4), which equals "The ". On the second iteration, it starts grabs the substring from position 4 to position (4+7), which equals "slices ". Get it? We are moving across the string a little at a time. You just have to make sure the numbers you are feeding the function are grabbing the correct substrings.

Another point to make is that the yield keyword will return a generator object. This is why I wrapped it in a list to actually see the results.
``` python
<generator object slices at 0x00001E7A2C38F20>
```

The code ends by saving my list into a csv file. Note that I used the 'a' append flag, so that on every iteration, a new line is added to the file.

That is pretty much it, hope you learned something new today.







