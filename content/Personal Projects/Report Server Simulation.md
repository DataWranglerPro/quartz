* 06/01/2012 - While working for [[Infinite Energy]] in Gainesville in the reporting team. We used [[Microsoft SSRS]] to create and schedule our reports. We has over 400 reports and scheduling them became an issue. The timing of them and the resources they took where becoming an issue. Some of them were dependent on each other and some of them took so long that it prevented others from finishing in a timely fashion. There needed to be a way to more strategically schedule them. So I created a [[Simulation]] of the entire report server using [[Python]].

![[sql.txt]]

![[Report Server Manager 1.3.py]]


![[Report Server Manager Manual.doc]]
**Report Server Manager**

**Summary**
The target audience for this tool is an analyst that is comfortable working with and manipulating code. The target audience is a person that enjoys analyzing data and using data to answer questions. The code is written in Python and its goal is to simulate a generic report server. The basic job of the report server is to automatically run reports on a schedule that is determined by a user. Most likely the person in charge of scheduling reports is the person reading this document. The main problem is that most report servers I have worked with do not help the user to efficiently schedule reports. This in turn leads to reports being scheduled at random times which may or may not conflict with the reports already scheduled. As the number of reports grow, it becomes harder and harder to manage schedules within the report server.

Since this tool simulates a report server. You can simulate what will happen to the server if for example you add a report and schedule it to run every day at 8am. You can simulate adding 100 reports scheduled at different times. The simulation will display its results in four CSV files which you can then do your own analysis on. It is my hope that this will help the reader better understand, manage, and answer any what if questions before actually implementing any changes to the actual report server.

Not that this is a simulation and it will attempt to act as closely as possible to the actual report server but not exactly. One of the four output CSV files shows you summary statistics for your current report server. This is done so you can compare this report with the results you get from the simulation and verify that the simulation is accurately mimicking the report server.

I know you have a lot of questions right now but please be patient, the sections below will answer all of your questions.

**Preliminary Questions**
1. What is the current status of my report server?
   Here you got two options, you can either run the sql code provided in the text file (sql.txt) or run the simulation script. After running the python script (Report Server Manager 1.3.py), it will write four CSV files in the location of the python script. Open the CSV file named “ReportSummaryStats”, this file will have all of the data you are looking for. I am assuming you are familiar with the python scripting language and you know how to run the python script. I am also assuming you can run SQL code on your own.

  Before you run the simulation make sure to type in the name of your report server. I am also assuming the database of your server is called “ReportServer” (line 6), if it is not please change it.

  Code:

  1. _## Target Report Server_
  2. _ReportServer = '__Type your report server here__’_
  4. _## Connect to server_
  5. _cnxn = pyodbc.connect(‘DRIVER={SQL Server};SERVER=’ + ReportServer +_
  6. ‘_;DATABASE=__ReportServer__;Trusted_Connection=yes’)_
  7. _cursor = cnxn.cursor()_
    
Note that we are only collecting data for reports that are on a subscription. I am also assuming you are on a Microsoft SQL server. If you are not, you will have to write your own query and modify the python code above since it is specifically written for a SQL server.

If you just run the SQL script all you have to do is point the SQL code to the correct server.

For every report, data is collected in two parts. We first collect all the data of the report when it has run and completed successfully. We then collect all the data of the report when it has run but not completed successfully. We then aggregate the data and provide summary statistics like (How long does the report take to run, time is usually starts, failure rate, what days of the week does the report run, etc.)

The way we determined what days the report runs is not very obvious. The backend does not provide us with an easy way to determine when the reports are scheduled. To remedy this, what we did is query the data for an entire month and extrapolate when the report usually runs. For example, if we query the report database for an entire month for one report and we notice it has run every Monday. We then can rest assure that this report will only run every Monday. The holes with this strategy are the reports that run every month, every year, every quarter, etc. For example, if a report runs the first Monday of every month and last month this meant it ran on a Wednesday. The SQL code will tag this report as running every Wednesday. This is obviously wrong but this is the cost/benefits with the current simulation model we are providing you.

The way we determined the average processing times and start times is the following way. We grabbed two weeks of execution data and used that to determine the summary statistics. This in our eyes gives us a good picture on how the reports are currently behaving. The holes in this strategy are if reports are constantly being rescheduled or if the reports on the server are new (have a week of less of execution data). The more time the reports have been running on the server and have not had a schedule change the more accurate the SQL query will be.

This data alone is worth gold. You can determine what reports take a long time to run (over 30min) and which reports constantly fail (high failure rate). The information below will be represented in one row on the CSV file. Here we can see that “ABC Report” usually starts at 6am (AvgStartTimehr_P), takes around 37 minutes (AvgProcessingTimeT_P) to process, has a failure rate of 28% (FailureRate), and runs every day of the week. Note this summary information is only using the data when “ABC Report” completed successfully. Anything labeled with a “_F” means data when the report failed. So for the example below we can see that the report takes around 37 minutes when it runs successfully but it takes 122 minutes (AvgProcessingTimeT_F) when it fails to complete. As you can see you can identify which reports fail consistently and which reports take a long time to process.

**Here is a sample of the data available for you:**

ReportName = ABC Report
AvgProcessingTimeT_P = 37.0
StDevProcessingTime_P = 5.166743
AvgStartTimehr_P = 6.0
StDevStartTimehr_P = 0.0
AvgStartTimemi_P = 0.0
StDevStartTimemi_P = 0.0
FailureRate = 0.277778
Sun_P = TRUE
Mon_P = TRUE
Tue_P = TRUE
Wed_P = TRUE
Thu_P = TRUE
Fri_P = TRUE
Sat_P = TRUE
AvgProcessingTimeT_F = 122.0
StDevProcessingTime_F = 23.691771
AvgStartTimehr_F = 8.0
StDevStartTimehr_F = 1.949359
AvgStartTimemi_F = 39.0
StDevStartTimemi_F = 15.139353
Sun_F = FALSE
Mon_F = FALSE
Tue_F = FALSE
Wed_F = FALSE
Thu_F = FALSE
Fri_F = FALSE
Sat_F = TRUE

2. How do I run the simulation for one day?
   We are assuming you want to run the report for one day and that day being a Sunday. This means only reports that run on Sundays will run in our simulation. We also assume you only want to run one replication or the simulation is only going to run one time. We also assume you already know how to run a python script. The code that we will be changing is below.

- ReportDetails – This is an array that will hold all the transactions that happen to each report. This includes the name of the report, the time the report started running, the time the report finished running, the time it took to run the report, the number of minutes it waited until a slot was open, if the report failed during execution, what attempt number is it on, the day of the simulation, and what replication is it part of.
    
- maxTime = int(HoursInADay*SixtyMinutes*NumberofDays) – This variable determines how long or for how many minutes the simulation will run for.
    
    - i.e. int(24*60*3) = 3 days
    - i.e. int(24*60*4) = 4 days
        
- seed() – Random seed generator
- ServerCapacity = int(n) – Maximum number of slots available. In other words the maximum number of reports that can be run at the same time
   - k – Declare the report resource object
    - Days = n – This will tell you what day the simulation is on (i.e. Day 0, Day 1, Day 2....)
    - MaxDays = n – Maximum number of days to run the simulation
        - i.e. If Days = 0 and MaxDays = 2, then the simulation will run for Sunday(0), Monday(1), and Tuesday(2)
        - i.e. If Days = 0 and MaxDays = 9, then the simulation will run for Sunday(0), Monday(1), Tuesday(2), Wednesday(3), Thursday(4), Friday(5), Saturday(6), Sunday(7), Monday(8), and Tuesday(9)
    - DayOfWeek = n – What day to start the simulation.
        - i.e. 0 = Sunday
        - i.e. 1 = Monday
    - ServerRetries = n – The maximum number of times the report server will try to re-run a report when it fails. The server will keep re-running the report until it runs successfully or when the maximum number of retries has been reached.
    - RetryDelay = n – The number of minutes the server will wait after a report that has failed is re-run.
        - i.e. Report fails at time zero, it waits n minutes, the server will then run the report again. The first time it ran was at time zero and the second time it ran was at time (0 + n).
        
**The modified code should look like this (I highlighted the variables that need to be chaged):**

_## Experiment data ------------------------------_
_ReportDetails = [] # initialize array, all report details_
_maxTime = int(24*60*1)_
_seed()_
_ServerCapacity = int(2)_
_k = Resource(capacity=ServerCapacity, name="SSRS2005", unitName="Slots", qType=FIFO, preemptable=False,_
_monitored=True, monitorType=Monitor)_
_Days = 0_
_MaxDays = 0_
_DayOfWeek = 0_
_ServerRetries = 3_
_RetryDelay = 15_

_## Experiment/Model -----------------------------------_
_for rep in range(1, 2):_
_initialize()_
_s = Source(name='Source')_
_activate(s, s.generate(D=Days, MD=MaxDays, DOW=DayOfWeek, resource=k, run=rep), at=0.0)_
_simulate(until=maxTime)_

3. How do I run multiple replications?
In other words how does one run the simulation multiple times to get a more accurate picture of the results?

_## Experiment/Model -----------------------------------_
_for rep in range(1, 2):_
_initialize()_
_s = Source(name='Source')_
_activate(s, s.generate(D=Days, MD=MaxDays, DOW=DayOfWeek, resource=k, run=rep), at=0.0)_
_simulate(until=maxTime)_

In this example range(1,2) run the simulation once.
- range(1,3) run the simulation two times.
   - range(1,4) run the simulation three times.
    - range(1,21) run the simulation twenty times.
    - range(1,101) run the simulation one hundred times.
    
  3. How do I run the simulation for a week?
Here the simulation starts on a Sunday and ends on a Saturday. The day the simulation starts can be altered by changing the variable “DayOfWeek”. We are also assuming you will only run the simulation one time. Notice maxTime has changed from 24*60*1 to 24*60*7. This is in order so that the simulation runs for a week. If you think reports may take long enough to bleed into the 2nd week, you may entertain the idea of increasing the value of maxTime. If not you may get a situation where a report started on the seventh day but never finished because it would have finished on the 8th day but the simulation only ran for 7 days thus never capturing the end date of the report.

_## Experiment data ------------------------------_
_ReportDetails = [] # initialize array, all report details_
_maxTime = int(24*60*7)_
_seed()_
_ServerCapacity = int(2)_
_k = Resource(capacity=ServerCapacity, name="SSRS2005", unitName="Slots", qType=FIFO, preemptable=False,_
_monitored=True, monitorType=Monitor)_
_Days = 0_
_MaxDays = 6_
_DayOfWeek = 0_
_ServerRetries = 3_
_RetryDelay = 15_

_## Experiment/Model -----------------------------------_
_for rep in range(1, 2):_
_initialize()_
_s = Source(name='Source')_
_activate(s, s.generate(D=Days, MD=MaxDays, DOW=DayOfWeek, resource=k, run=rep), at=0.0)_
_simulate(until=maxTime)_

3. How do I change the number of reports that can be run at the same time?
By default SQL server decides how many reports the server can handle at the same time. This can be changed by your DB administrator but in my experience it has been two. In the simulation this can be easily changed to suite your needs by changing the highlighted line of code below.
  
_## Experiment data ------------------------------_
_ReportDetails = [] # initialize array, all report details_
_maxTime = int(24*60*7)_
_seed()_
_ServerCapacity = int(2)_
_k = Resource(capacity=ServerCapacity, name="SSRS2005", unitName="Slots", qType=FIFO, preemptable=False,_
_monitored=True, monitorType=Monitor)_
_Days = 0_
_MaxDays = 6_
_DayOfWeek = 0_
_ServerRetries = 3_
_RetryDelay = 15_

3. How do I change the number of times the server will re-try to run a report that failed?
When a report fails, the report server will queue up the report and re-attempt to run it again. It will continue to do this until the report runs successfully or it has reached the maximum number of retries. By default SQL server will try to run the report 3 more times after the initial attempt. The report server will also wait n minutes before re-running the report. These two values can be changed and are highlighted below.

_## Experiment data ------------------------------_
_ReportDetails = [] # initialize array, all report details_
_maxTime = int(24*60*7)_
_seed()_
_ServerCapacity = int(2)_
_k = Resource(capacity=ServerCapacity, name="SSRS2005", unitName="Slots", qType=FIFO, preemptable=False,_
_monitored=True, monitorType=Monitor)_
_Days = 0_
_MaxDays = 6_
_DayOfWeek = 0_
_ServerRetries = 3_
_RetryDelay = 15_

**What if Questions?**
  1. What if I want to add a new report that does not exist on the report server and see how it affects the other reports?
    2. What if I want to add many new reports and see how they affect the system?
    3. What if I want to modify certain attributes of existing reports and see how they affect the system?
    4. What if I want to delete or ignore some of the reports currently on the report server before I run the simulation?
    5. What if I do not want to use the reports currently on my report server and make up my own?
    
**Line by line explanation of code**
Import simulation package
_from SimPy.Simulation import *_
  
Import math package to model report variability:
- Time report begins running
- Processing time

_from random import expovariate, seed_

Import package to write csv files
_import csv_

Import package to get current time
_import datetime_

Import package to be able to connect to a sql server
_import pyodbc_

The ReportServer variable is set to the report server of your choice. We then connect to server using the current users credentials.

Code:
_## Target Report Server_
_ReportServer = 'devdb4'_

_## Connect to server_
_cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + ReportServer + ';DATABASE=ReportServer;Trusted_Connection=yes')_

_cursor = cnxn.cursor()_

The sql code to get the current status of the report server is supplied in a text file named “sql”. This script will grab all reports that have a subscription and pull summary statistics for you. The code is run on the server and its results will be saved to an array named “arr”.

Code:
_## Open sql file to be run_
_f = open('sql.txt', 'r')_
  
_## Run sql code and assign it to array named "arr"_
_cursor.execute(f.read())_
_arr = cursor.fetchall()_

If you want to check the contents of the text file run the following code:
_## Open sql file to be run_
_f = open('sql.txt', 'r')_
_print f.read()_

If you want to check the contents of the array (short hand):
_print arr_

If you want to check the contents of the array (using loops):
_for x in range(0, len(arr)):_
_for y in range(0, len(arr[x])):_
_print arr[x][y]_

If you just want to check the first row of the array:
_print arr[0]_

**Explain the data in the array “arr”:**
##== Define "arr" ==##
##==================##
arr = [ReportName – The name of the report,
Pass - Average Processing Time in minutes,
Pass - StDev Processing Time in minutes,
Pass - Average Start Time HR in hours,
Pass - StDev Start Time HR in hours,
Pass - Average Start Time Mi in minutes,
Pass - StDev Start Time Mi in minutes,
Pass - Failure Rate Percentage,
Pass - Runs Sunday,
Pass - Runs Monday,
Pass - Runs Tuesday,
Pass - Runs Wednesday,
Pass - Runs Thursday,
Pass - Runs Friday,
Pass - Runs Saturday,
=========================================

Fail - Average Processing Time in minutes,
Fail - StDev Processing Time in minutes,
Fail - Average Start Time HR in hours,
Fail - StDev Start Time HR in hours,
Fail - Average Start Time Mi in minutes,
Fail - StDev Start Time Mi in minutes,
Fail - Runs Sunday,
Fail - Runs Monday,
Fail - Runs Tuesday,
Fail - Runs Wednesday,
Fail - Runs Thursday,
Fail - Runs Friday,
Fail - Runs Saturday

**Note:**
**Pass – Summary statistics using only the data of reports that completed successfully
**Fail – Summary statistics using only the data of reports that did not complete successfully

**Explain simulation code:**
Initial simulation variables are set here:

_## Experiment data ------------------------------_
_ReportDetails = []_
_maxTime = int(24*60*14)_
_seed()_
_ServerCapacity = int(2)_
_k = Resource(capacity=ServerCapacity, name="SSRS2005", unitName="Slots", qType=FIFO, preemptable=False,_
_monitored=True, monitorType=Monitor)_
_Days = 0_
_MaxDays = 7_
_DayOfWeek = 0_
_ServerRetries = 3_
_RetryDelay = 15_

- ReportDetails – This is an array that will hold all the transactions that happen to each report. This includes the name of the report, the time the report started running, the time the report finished running, the time it took to run the report, the number of minutes it waited until a slot was open, if the report failed during execution, what attempt number is it on, the day of the simulation, and what replication is it part of.
    
- maxTime = int(HoursInADay*SixtyMinutes*NumberofDays) – This variable determines how long or for how many minutes the simulation will run for.
    
    - i.e. int(24*60*3) = 3 days
    - i.e. int(24*60*4) = 4 days
        
- seed() – Random seed generator
- ServerCapacity = int(n) – Maximum number of slots available. In other words the maximum number of reports that can be run at the same time
   - k – Declare the report resource object, see section 7
- Days = n – This will tell you what day the simulation is on (i.e. Day 0, Day 1, Day 2....)    
- MaxDays = n – Maximum number of days to run the simulation
    - i.e. If Days = 0 and MaxDays = 2, then the simulation will run for Sunday(0), Monday(1), and Tuesday(2)
    - i.e. If Days = 0 and MaxDays = 9, then the simulation will run for Sunday(0), Monday(1), Tuesday(2), Wednesday(3), Thursday(4), Friday(5), Saturday(6), Sunday(7), Monday(8), and Tuesday(9)
- DayOfWeek = n – What day to start the simulation.
       - i.e. 0 = Sunday
       - i.e. 1 = Monday       
- ServerRetries = n – The maximum number of times the report server will try to re-run a report when it fails. The server will keep re-running the report until it runs successfully or when the maximum number of retries has been reached.
- RetryDelay = n – The number of minutes the server will wait after a report that has failed is re-run.
    - i.e. Report fails at time zero, it waits n minutes, the server will then run the report again. The first time it ran was at time zero and the second time it ran was at time (0 + n).
        
Here I try to explain the flow of events and the code behind it all. It might be slightly confusing the first time you take a look at it but it will eventually make sense.

1. initialize()
- This sets the internal clock to zero
- It initializes global simulation variables
- Created before any process objects are created

2. s = Source(name='Source')
- Create a new Source object
- Passes a variable name (name='Source') to all the functions under the Source class
- A process object is "passive" when first created, i.e., it has no scheduled events
- Note that the variable "name" cannot be changed. Typing "Name" or "Reportname" will cause an error

3. activate(s, s.generate(D=Days, MD=MaxDays, DOW=DayOfWeek, resource=k, run=rep), at=0.0)
- Activates process object s
- Calls the generate function and passes four parameters (D, MD, DOW, resource, run)
- D will tell you what day the simulation is on (i.e. Day 0, Day 1, Day 2....)
- MD controls the number of days the simulation will run for
- DOW will tell you what day of the week the simulation is currently on (0=Sun, 1=Mon, etc..)
- resource will determine the maximum number of reports that can be run at the same time
- run will determine how many replications will the simulation perform
- at=0.0 – Determines when the simulation will start, when to activate the process object, default is now()
- Activation of process objects adds events to the simulation schedule

4. simulate(until=maxTime)
- This starts the simulation and end the simulation when the end time is reached
- Activated process objects will not start operating until the simulate(until=endtime) statement is executed
- maxTime = int(HoursInADay*SixtyMinutes*NumberofDays)
- i.e. int(24*60*3) = 4,320 minutes = 3 days
- i.e. int(24*60*4) = 5,760 minutes = 4 days

Code:
_## Experiment/Model -----------------------------------_
_for rep in range(1, 2):_
_initialize()_
_s = Source(name='Source')_
_activate(s, s.generate(D=Days, MD=MaxDays, DOW=DayOfWeek, resource=k,_
_run=rep), at=0.0)_
_simulate(until=maxTime)_

Note that these four lines of code are all under a “for loop”. The purpose of the “for loop” is to run the simulations multiple times. Since the time reports start and the time the reports take to run vary, we need to make sure we run the simulation many times to get a realistic average. For example, take a report that takes anywhere from 0 to 2 hours to run. If we run the simulation one time, the results might come out saying the report took 5 minutes to run. It would not be wise to assume that on average this report will take 5 minutes to run. It did take 5 minutes to run when we ran the simulation, but we need to run the simulation many times in order to get a more realistic picture on how long does the report on average actually take to run. You can set the number of replication in the [_range(start, end)_] part of the code.

6. At this point the only events scheduled are the _activate(s, s.generate….)_. This means as soon as the code _simulate(until=maxTime)_ is run, we start running the code inside the generate function. The variables that get passed to the generate function are shown below.

- D = Days = 0, i.e. We start at day 0
- MD = MaxDays = 2, i.e. run the simulation for three days (0, 1, 2)
- DOW = DayOfWeek = 0, i.e. start with day 0 or Sunday
- resource = k, this will be explained in section 7
- run = rep, this tells us which replication the simulation is currently on

7. k = Resource(capacity=ServerCapacity, name="SSRS2005", unitName="Slots", qType=FIFO, preemptable=False,
monitored=False, monitorType=Monitor)
- Defines a resource object k
- capacity is a positive real or integer value that specifies the total number of identical units in Resource object r.
- capacity=ServerCapacity=n, i.e. The server can handle a maximum of 2 reports at a time
- name is a descriptive name for this Resource object
- unitName is a descriptive name for a unit of the resource
- qType is either FIFO or PriorityQ. It specifies the queue discipline of the resource's waitQ; typically, this is FIFO and that is the default value. If PriorityQ is specified, then higher-priority requests waiting for a unit of Resource r are inserted into the waitQ ahead of lower priority requests.
- preemptable is a Boolean (False or True); typically, this is False and that is the default value. If it is True, then a process requesting a unit of this resource may preempt a lower-priority process in the activeQ, i.e., one that is already using a unit of the resource.
- monitored is a boolean (False or True). If set to True, then information is gathered on the sizes of r's waitQ and activeQ, otherwise not.
- monitorType is either Monitor or Tally and indicates the type of Recorder to be used

8. The generate function while loop (while D <= MD:)
- Loop until the variable D is less than or equal to MD
- This loop is used to simulate report executions that span multiple days
- Without this loop the reports will only run for one day
- This makes it possible to simulate for example reports that only run on Mondays and on Wednesdays.
- This loop also monitors what day of the week it is in, using the DOW variable
- i.e. DOW=0=Sunday, DOW=1=Monday,....., DOW=6=Saturday
- After the variable reaches 6, it then gets reset to 0

9. The generate function has a “for loop” that loops (number of records in the array) of times.

Code:
_for x in range(0, len(arr)):_

a. We first pick the x report in the array and put all of its attributes inside variables

Code:
_## Set up Report variables_
_ReportName = arr[x][0]_
_if arr[x][1] is None:_
_AvgPT_P = float(0)_
_else:_
_AvgPT_P = float(arr[x][1]) ##Pass - Average Processing Time in minutes_
_if arr[x][2] is None:_
_StDevPT_P = float(0)_

_else:_
_StDevPT_P = float(arr[x][2]) ##Pass - StDev Processing Time in minutes_
_if arr[x][3] is None:_
_AvgSThr_P = float(0)_
_else:_

_AvgSThr_P = float(arr[x][3]) ##Pass - Average Start Time HR in hours_

Note:
I was forced to convert all these values to floats because of some type mismatches when these variables were used later in the code.

b. We also determine if the report failed or if it ran succesfully
- The function RPTstatus(pass failure rate) is used to determine the outcomes
- If the probability is greater than the outcome of a random number (a number between 0 and 1) then return 1, else return 0. for example, report abc has a failure rate of 20%. We then call the RPTstatus function. The random number (_random.random()_) generated is 0.60 or 60%. Since 0.20 is smaller than 0.60, report abc completed successfully and the function RPTstatus returns a zero.

Code:
_ReportFailed = s.RPTstatus(FRate)_

Function Code:
_def RPTstatus(self,Probability):_
_return random.random() < Probability_

c. We then calculate when the report is scheduled to start running in minutes
- ReportStartTime_P and ReportStartTime_F
- We use a normal distribution function to determine the values
- We multiply by 60 because the units are originally in hours and we need to convert them to minutes
- D*24*60, used to adjust start times depending on what day it is
- We also have logic that prevents the start times from being negative

Code:
_ReportStartTime_P = (random.normalvariate(AvgSThr_P, StDevSThr_P)*60 +_
_random.normalvariate(AvgSTmi_P, StDevSTmi_P) + D*24*60)_
_ReportStartTime_F = (random.normalvariate(AvgSThr_F, StDevSThr_F)*60 +_
_random.normalvariate(AvgSTmi_F, StDevSTmi_F) + D*24*60)_
_if ReportStartTime_P < 0:_
_ReportStartTime_P = 0_
_if ReportStartTime_F < 0:_
_ReportStartTime_F = 0_

d. event1 = SimEvent(ReportName)
- We create an event named ReportName (name of current report)
- This will allow us to determine when the report finishes so that we can rerun it if it failed
- At this point we just create the event but nothing is done with it here

e. The section "if ((DOW == 0...." checks if the report is scheduled to run on a specific day of the week
- If yes then it continues, if not then the report is ignored

Code:
_if ((DOW == 0 and Sun_P == 1) or_
_(DOW == 1 and Mon_P == 1) or_
_(DOW == 2 and Tue_P == 1) or_
_(DOW == 3 and Wed_P == 1) or_
_(DOW == 4 and Thu_P == 1) or_
_(DOW == 5 and Fri_P == 1) or_
_(DOW == 6 and Sat_P == 1)):_

f. if (ReportFailed):
- Check if the report failed
- If it did then
- c = Customer(name = ReportName)
* Now that we have verified the report is scheduled to run...
* Create a new Customer object
* Passes a variable name (name = ReportName) to all the functions under the Customer class
* Note that the variable "name" cannot be changed. Typing "Name" or "Rptname" will cause an error

I) activate(c,c.visit(...parameters...), at=ReportStartTime_F)
- Activates the process object c
- Calls the visit function and passes parameters (....parameters...)
- at=ReportStartTime_F, determines when the report will start executing
* [yield hold,self,0] - I was forced to place this line here or else I would get an error
- c = Customer(name = ReportName)
* Now that we have verified the report failed, we schedule it to be re-run...
* Create a new Customer object
* Passes a variable name (name = ReportName) to all the functions under the Customer class
* Note that the variable "name" cannot be changed. Typing "Name" or "Rptname" will cause an error

I) activate(c,c.reSchedule(...parameters...), at=ReportStartTime_F)
- Activates the process object c
- Calls the reSchedule function and passes parameters (....parameters...)
- at=ReportStartTime_F, determines when the function will start executing
- event1 (see step 9d) - Will ensure the report does not restart until it completes processing
* [yield hold,self,0] - I was forced to place this line here or else I would get an error
- If the report completed successfully then
- It calls the visit function like above but begins executing the function at ReportStartTime_P
- It does not call the reSchedule function since the report does not need to be rerun

Code:
_if (ReportFailed):_
_c = Customer(name = ReportName)_
_activate(c,c.visit(AvgPT_P, StDevPT_P,_
_AvgSThr_P, StDevSThr_P,_
_AvgSTmi_P, StDevSTmi_P,_
_FRate,_
_Sun_P, Mon_P, Tue_P, Wed_P, Thu_P, Fri_P, Sat_P,_
_AvgPT_F, StDevPT_F,_
_AvgSThr_F, StDevSThr_F,_
_AvgSTmi_F, StDevSTmi_F,_
_Sun_F, Mon_F, Tue_F, Wed_F, Thu_F, Fri_F, Sat_F,_
_r=resource,WhatDay=D,WeekDay=DOW,MyEvent=event1,F=ReportFailed,run=run), at=ReportStartTime_F)_
_yield hold,self,0_
_c = Customer(name = ReportName)_
_activate(c,c.reSchedule(AvgPT_P, StDevPT_P,_
_AvgSThr_P, StDevSThr_P,_
_AvgSTmi_P, StDevSTmi_P,_
_FRate,_
_Sun_P, Mon_P, Tue_P, Wed_P, Thu_P, Fri_P, Sat_P,_
_AvgPT_F, StDevPT_F,_
_AvgSThr_F, StDevSThr_F,_
_AvgSTmi_F, StDevSTmi_F,_
_Sun_F, Mon_F, Tue_F, Wed_F, Thu_F, Fri_F, Sat_F,_
_r=resource,WhatDay=D,WeekDay=DOW,MyEvent=event1,F=ReportFailed,run=run), at=ReportStartTime_F)_
_yield hold,self,0_

_else:_
_c = Customer(name = ReportName)_
_activate(c,c.visit(AvgPT_P, StDevPT_P,_
_AvgSThr_P, StDevSThr_P,_
_AvgSTmi_P, StDevSTmi_P,_
_FRate,_
_Sun_P, Mon_P, Tue_P, Wed_P, Thu_P, Fri_P, Sat_P,_
_AvgPT_F, StDevPT_F,_
_AvgSThr_F, StDevSThr_F,_
_AvgSTmi_F, StDevSTmi_F,_
_Sun_F, Mon_F, Tue_F, Wed_F, Thu_F, Fri_F, Sat_F,_
_r=resource,WhatDay=D,WeekDay=DOW,MyEvent=event1,F=ReportFailed,run=run), at=ReportStartTime_P)_
_yield hold,self,0_

g. So when the simulation starts the time is zero (see step 4), then the next scheduled events were activated at step 9f. This step will start executing at time ReportStartTime_F or ReportStartTime_P and call the function visit and or the function reSchedule

h. def visit(self,...parameters...):
- The function visit will default all its variables to zero if no values are passed in

i. arrive = now()
- Records the time the report requested to be run by the server

j. print "We are in Day " + str(WhatDay)
- For debugging purposes
- What day are we in (0, 1, 2, …., n)

k. print "%7.4f %s: Here I am"%(now(),self.name)
- For debugging purposes
- Time report requested to be run by the server

l. yield request,self,r
- Request one unit of the resource
- If the server is free then the report can start running immediately and the code moves on to the next line. If the server is busy, the report is automatically queued by the Resource. When it eventually comes available the PEM moves on to the next line.

m. wait = now()-arrive
- Calculate how long the report had to wait until it started to run

n. print "%8.3f %s: Waited %6.3f"%(now(),self.name,wait)
- For debugging purposes
- Time report waited before the server was free to run the report

o. if (F):
- If the report failed
- We then calculate how long the report takes to complete
* ProcessingTime_F
* We use a normal distribution function to determine the values
* We also have logic that prevents the start times from being negative

I) yield hold,self,ProcessingTime_F
- Yields' can delay a process, put it to sleep, request a shared resource or provide a resource
- In this case it will delay the visit function for a total of ProcessingTime_F minutes

II) yield release,self,r
- Release one unit of the resource
- The current report finishes running and the server frees up one slot for

any remaining reports in the queue

III) MyEvent.signal()
- This line gives "the signal, the report has completed", to the function reSchedule

IV) print "%7.4f %s: Report completed"%(now(),self.name)
- For debugging purposes
- Time report finished running

V) ReportDetails.append([self.name, arrive, (now() - arrive), now(), wait, F, Attempt, WhatDay, WeekDay, run])
- Log all the data that has happened to the report thus far.
- self.name, The name of the report
- arrive, The time the report requested to be run by the server
- now(), The current simulation time
- wait, The time the report had to wait before it got served by the server
- F, If 0 the report passed, if 1 the report failed
- Attempt, How many attempts have been made to run the report. This number can range from 1 to (1 + maximum number of re-attemts allowed)
- WhatDay, What day are we currently in
- WeekDay, What day of the week are we in
- run, What replication are we currently in

VI) The visit function completes and we now go back to the generate function
- yield hold,self,0
* We are now back in the generate function
* delay the process for 0 minutes
* This line needs to be here or it will cause an error ????

VII) The generate function will loop again starting the process at step 9a
- If the report passed
- We then calculate how long the report takes to complete
* ProcessingTime_P
* We use a normal distribution function to determine the values
* We also have logic that prevents the start times from being negative

I) yield hold,self,ProcessingTime_P
- Yields' can delay a process, put it to sleep, request a shared resource or provide a resource
- In this case it will delay the visit function for a total of ProcessingTime_P minutes

II) yield release,self,r
- Release one unit of the resource
- The current report finishes running and the server frees up one slot for

any remaining reports in the queue

III) print "%7.4f %s: Report completed"%(now(),self.name)
- For debugging purposes
- Time report finished running

IV) ReportDetails.append([self.name, arrive, now(), (now() - arrive), wait, F, Attempt, WhatDay, WeekDay, run])
- Log all the data that has happened to the report thus far.
- self.name, The name of the report
- arrive, The time the report requested to be run by the server
- now(), The current simulation time
- wait, The time the report had to wait before it got served by the server
- F, If 0 the report passed, if 1 the report failed
- Attempt, How many attempts have been made to run the report. This number can range from 1 to (1 + maximum number of re-attemts allowed)
- WhatDay, What day are we currently in
- WeekDay, What day of the week are we in
- run, What replication are we currently in

V) The visit function completes and we now go back to the generate function
- yield hold,self,0
* We are now back in the generate function
* delay the process for 0 minutes
* This line needs to be here or it will cause an error ????

VI) The generate function will loop again starting the process at step 9a
10. Note that if the report failed
- Not only is the visit function running but the reSchedule function is also running at the same time
- The reSchedule function will wait until MyEvent.signal() (see 9k, part III) is triggered

11. reSchedule function
a. Attempts = ServerRetries
- Take notes on how many time the server has tried to run the report successfully

b. while (Attempts > 0 and F == True):
- Continue to run the code while we have run out of retries and the report still is failing

c. yield waitevent, self, MyEvent
- Waits until MyEvent.signal() (see 9o, part III) is triggered
- Waits until the report that failed finishes running before we try to run it again

d. yield hold,self,RetryDelay
- Waits (RetryDelay) number of minutes before re-running the report

e. RptFailed = s.RPTstatus(FRate)
- We simulate the outcome of the next report outcome (fail vs pass)

f. F = RptFailed
- The outcome of the report (0 or 1) will be stored in variable F. This variable is then used to pass this information to the visit function.

g. WhatDay = int(now()/(24*60))
- Here we recalculate what day we are currently on
- This is because by the time we restart the report, we might have waited a long time and we might be on a different day than when the function was called

h. WeekDay
- We make sure this value is within 0 and 6

i. AttemptNumber = (ServerRetries - Attempts) + 1
- What attempt are we currently in

j. c =..., activate...yield...

- We call the visit function again and try to run the report once more

k. if (F):
- If the report failed again we lower the number of retries by one

l. The function continues to loop until the report runs successfully or the variable "Attempts" gets to zero.
- By default, a report can be run a maximum of 4 times (1 regular, 3 retries)
- This can be adjusted by the variable (ServerRetries)

12. The simulation will end when the maxTime variable equals the simulation time

  
**How are the results of the simulation generated?**

Get current time:
_CurrentTime = datetime.datetime.now()_
_CurrentTime = CurrentTime.strftime("%Y-%m-%d_%H-%M-%S")_

Create a CSV file:
- Name the CSV file “ReportDetails”
- Header row = 'ReportName', 'TimeStart', 'TimeEnd', 'ProcessingTime', 'WaitTime', 'RptFailed', 'RptAttempt', 'Day', 'WeekDay', 'Replication'
- The CSV files will be written o the same location the python script is located
- The other 3 CSV files are created the same way
    
Code:
_with open('ReportDetails_' + CurrentTime + '.csv', 'wb') as f:_
_writer = csv.writer(f)_
_writer.writerow(['ReportName', 'TimeStart', 'TimeEnd',_ 'ProcessingTime', _'WaitTime', 'RptFailed', 'RptAttempt', 'Day', ‘WeekDay’, 'Replication'])_
_writer.writerows(ReportDetails)_

There are four CSV files that hold all of the results of the simulation:
- **ReportDetails – Execution details of all reports**
    - ReportName – The name of the report
    - TimeStart - The time the report requested to be run by the server
    - TimeEnd – The time the report finished processing
    - ProcessingTime – The time the report took to run
    - WaitTime – The time the report had to wait before it got served by the server
    - RptFailed – If “FALSE” (0) the report passed, if “TRUE” (1) the report failed
    - RptAttempt – How many attempts have been made to run the report
    - Day – What day are we currently in
    - WeekDay – what day of the week are we currently in
    - Replication – What replication are we currently in
- **ReportSummaryStats – This holds the current state of the reporting server**
    - ReportName - The name of the report
    - AvgProcessingTimeT_P - Average Processing Time in minutes
    - StDevProcessingTime_P - StDev Processing Time in minutes
    - AvgStartTimehr_P - Average Start Time HR in hours
    - StDevStartTimehr_P - StDev Start Time HR in hours
    - AvgStartTimemi_P - Average Start Time Mi in minutes
    - StDevStartTimemi_P - StDev Start Time Mi in minutes
    - FailureRate - Failure Rate Percentage
    - Sun_P - Runs Sunday
    - Mon_P - Runs Monday
    - Tue_P - Runs Tuesday
    - Wed_P - Runs Wednesday
    - Thu_P - Runs Thursday
    - Fri_P - Runs Friday
    - Sat_P - Runs Saturday
    - AvgProcessingTimeT_F - Average Processing Time in minutes
    - StDevProcessingTime_F - StDev Processing Time in minutes
    - AvgStartTimehr_F - Average Start Time HR in hours
    - StDevStartTimehr_F - StDev Start Time HR in hours
    - AvgStartTimemi_F - Average Start Time Mi in minutes
    - StDevStartTimemi_F - StDev Start Time Mi in minutes
    - Sun_F - Runs Sunday
    - Mon_F - Runs Monday
    - Tue_F - Runs Tuesday
    - Wed_F - Runs Wednesday
    - Thu_F - Runs Thursday
    - Fri_F - Runs Friday
    - Sat_F - Runs Saturday

**Note:**
**Columns with the letter P – Summary statistics using only the data of reports that completed successfully
** Columns with the letter F – Summary statistics using only the data of reports that did not complete successfully

- **ServerActiveDetails – Tells you how many report were running broken down by time**    
    - TimeMin – The simulation time in minutes
    - Activeslots – Number of reports running at the same time
        
- **ServerWaitingDetails – Tells you how the number of report that are waiting to be run broken down by time**
    - TimeMin – The simulation time in minutes
    - NumberWaiting – Number of reports waiting in queue