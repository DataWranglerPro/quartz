This is a continuation from the [[Python]] [[parser]] scripts I was asked to create at work.

Here is a brief summary:
- At work I had the task to reverse engineer some .csv files. I was given a folder with hundreds of .txt files and then asked to convert these into .csv files.
- I half wrote some Python code and I ended up having to re-write it to accomplish the task that kept changing over time.

Below is my final Python script. It takes a set of .txt files and converts them to csv files.

# Folder Structure
- input
	- app
		- tr
		- appSuites.json
- output
	- app
		- appSuites
- parser.bat
- parser.py
- settings.json

# parser.bat
Some of the folks at work had issues running Python files directly, so this is just a helper file that they can just click on to see the results and look for any errors in the terminal. 

``` sh
@ECHO OFF
SET PATH=%PATH%;"C:/Program Files\Python38"
python parser.py
PAUSE
```


# settings.json

I intended to have multiple settings.json files depending on the application. This is simply to have the end user create the variables in this json file instead of the Python code itself. Yes, the data below is made up as I can't really share the actual values I used.

``` json
{
	"tr_folder": "input/app/tr",
	"file_name": "output/app/app_master.csv",
	"header_list": ["a","b","c"],
	"header_list_new": ["a","b"],
	"max_length": 200,
	"root_folder": "output/app/appSuites",
	"suites_config": "input/app/appSuites.json",
	"suite_suffix": "_appTransactions.csv",
	"test_case_slices": [5,1,1,1,1,15,3,6,6,7]
}
```


# appSuites.json

This is the file that will tell Python the file/folder structure of the final .csv files.

- **Suite** - will be used to tie rows from the .txt files to the json object below
- **Folder** - will be used to determine the folder/file where to place the .txt content

``` json
{
	"columns": [
		{
			"Suite": "aaa",
			"Folder": "appSuites/bbb"
		},
		{
			"Suite": "bbb",
			"Folder": "appSuites/bbb"
		}		
	]
}
```

# parser.py

This is the main Python script that contains all of the logic.

``` python
# import libraries
import os
import csv
import json
import shutil
from pathlib import Path

def main():
	''' generate csv files based on txt files '''
	# current working directory
	cwd = Path(os.getcwd())

	# read settings file
	settings = read_json('settings.json')

	# variables
	tr_folder = cwd.joinpath(settings['tr_folder'])
	file_name = cwd.joinpath(settings['file_name'])
	header_list = settings['header_list']
	header_list_new = settings['header_list_new']
	max_length = settings['max_length']
	root_folder = cwd.joinpath(settings['root_folder'])
	suites_config = cwd.joinpath(settings['suites_config'])
	suite_suffix = settings['suite_suffix']
	test_case_slices = settings['test_case_slices']

	# add header row
	add_header(file_name, header_list)

	# generate test cases
	add_test_cases(tr_folder, max_length, file_name, test_case_slices)

	# edit test cases
	edit_test_cases(file_name, header_list_new)

	# generate suite csv files
	create_suites(file_name, root_folder, suites_config, suite_suffix)

def add_header(file_name, header_list):
	''' add header row '''
	with open(file_name, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(header_list)

def add_test_cases(tr_folder, max_length, file_name, test_case_slices):
	''' parse .txt files and save them in a master csv file '''

	# loop through the folder
	for (path1, dirs1, files1) in os.walk(p_path):
		# loop through all the files
		for file1 in files1:
			# read text file
			with open (path1 + '/' + file1, 'r', encoding='UTF-8') as file:
				# loop through each line
				for line in file:
					# ignore lines that do not match max_length
					if len(line) != max_length:
						print(file1 + " invalid length of " + str(len(line)))
						continue
					
					# parse row
					parsed = list(slices(line, *test_case_slices*))
					final = parsed
					final.insert(0, file1)

					# append to csv file
					with open(file_name, 'a', newline='') as csvfile:
						f = csv.writer(csvfile, delimiter=',')
						f.writerow(final)
def edit_test_cases(file_name, header_list_new):
	''' make changes to csv file '''
	with open(file_name, 'r+') as csvfile:
		# read the file
		reader = csv.DictReader(csvfile)
		data = list(reader)

	for row in data:
		# remove column
		del row['c']

	# move to the beginning of the file
	csvfile.seek(0)

	# use new headers
	writer = csv.DictWriter(csvfile, fieldnames=header_list_new, lineterminator='\n')

	# write to file and clean up
	writer.writeheader()
	writer.writerows(data)
	csvfile.truncate()

def create_suites(file_name, root, suites_config, suite_siffix):
	''' use config jaon to create the csv files '''

	# delete existing csv files
	shutil.rmtree(root)

	# create folder if missing
	os.makedirs(root, exist_ok=True)

	# read suites config json file
	json_data - read_json(suites_config)

	# loop through csv
	with open(file_name, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		data = list(reader)

	for row in data:
		flag = False # keep track orphan rows

		for j in json_data['columns']:
			# find match
			if j['Suite'] in row['col1']:
				flag=True
				fn=root.joinpath(j['Folder'], j['Suite'] + suite_suffix)

				# create folder if missing
				os.makedirs(root.joinpath(j['Folder']), exists_ok=True)

				if os.path.exists(fn):
					with open(fn, 'a', newline='') as csvfile:
						writer = csv.DiscWriter(csvfile, fieldnames=reader.filednames, lineterminator='\n')
						writer.writerow(row)
				else:
					with open(fn, 'w', newline='') as csvfile:
						writer = csv.DiscWriter(csvfile, fieldnames=reader.filednames, lineterminator='\n')
						writer.writeheader()
						writer.writerow(row)	

			if flag == False:
				print('WARNING: test case not in config file: ' + row['col1'])

def slices(s, *args):
	''' get substring of length n '''
	position = 0
	for length in args:
		yield s[position:position + length]
		position += length

def read_json(file_path):
	''' generic json readaer '''
	with open(file_path, 'r') as f:
		json_data = json.load(f)

	return json_data

if __name__ == "__main__":
	main()
```