Here is the process I have been attempting in [[BugCrowd]].

# Create Automation Tool
The first step is to create a tool that will allow me to attack targets and generate a report I can submit to [[BugCrowd]].

## Features
- Scans are driven by .yaml files
- Control over
	- What attacks to conduct
	- What subdomains to target
- Custom reports per attack/per target

I want to be able to work on an attack, code it, add test it against any number of targets. If the attack is successful, then generate a report, and finally submit it to the Bug Bounty program.

## Folder Structure
- \\config
	- holds [[yaml]] file that controls scan execution
- \\modules
	- contains all of the custom attacks (.py files)
- \\reporting
	- contains all of the custom reporting code (.py files)
- \\results
	- contains reports of successful attacks (.txt files)
- \\targets
	- holds the [[yaml]] files of our targets
- main.py
	- contains the core functionality to process [[yaml]], run attacks on targets, and call reporting code

## Target yaml file
Keeping the targets in a separate file allows me to control what I attack, the methods of attack, and allows custom reporting.

- Challenges
	- Making changes to a large number of [[yaml]] files
		- TO DO: I need add command line functionality to make changes in bulk to the [[yaml]] files

``` yaml
meta:
  company: ABC
  url: https://www.abc.com
  scope: >
    Any domain/property of ABC not listed in the targets section is out of scope. 
    This includes any/all subdomains not specifically listed.

subdomains:
  - abc.com
  - api.abc.com

modules:
  - name: run_custom_attack
    reporting_function: run_reporting_function
```

## Config file
This is a sample of the file that help me control scan execution runs. It is pretty basic but it allows me to run tests on a small population and allows me to run scans on all targets pretty seamless.

``` YAML
run_options:
  targets:
    - specific: ['abc.yaml']  # Specify specific target(s) to run
    - all: false  # Do not run all targets
  functions:
    - specific: ['run_custom_attack']  # Specify specific functions to run
    - all: false  # Do not run all functions
```

# Enumeration
The simple target will tell you exactly what subdomain you can target. I simply copy/paste that into a [[yaml]] file and it is added to the rotation of subdomains to attack. But there are those that will tell you that any url in a certain subdomain is available to be attacked. This means we need to enumerate and identify all those subdomains.

- https://crt.sh
	- This website lets you search a domain and it will return a bunch of subdomains
- [[sublist3r]] (via Kali)
	- Does a pretty good job at finding the subdomains via command line
	- Strategy
		- Do a search with 1st level domain
			- abc.com
		- Do additional search for 2nd level domains
			- qa.abc.com
		- Do additional search for 3rd level domains
			- dev.qa.abc.com 
		- Repeat until you run out of new results from [[sublist3r]]
	- **WARNING**
		- After a while, you will start to get blocked from the websites (i.e. Google) used by [[sublist3r]] to get the subdomains. This just means you will need to take a break of a few days and continue enumerating


# Upkeep
- Bad subdomains
	- You will get a good number of subdomains from your enumeration that you cannot ping/reach/scan and I recommend you just eliminate these from your attacks
	- I have a module that specifically flags bad subdomains and I remove those manually (for now) from my [[yaml]] target files.

