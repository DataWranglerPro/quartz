
from SimPy.Simulation import *
from random import expovariate, seed
import csv
import datetime
import pyodbc

## Target Report Server
ReportServer = 'devdb4'

## Connect to server
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + ReportServer + ';DATABASE=ReportServer;Trusted_Connection=yes')
cursor = cnxn.cursor()

## Open sql file to be run
f = open('sql.txt', 'r')

## Run sql code and assign it to array named "arr"
cursor.execute(f.read())
arr = cursor.fetchall()


## Model components -----------------------------
class Source(Process):                              
    """ Loops through all reports """

    def generate(self,D,MD,DOW,resource,run):

        while D <= MD:

            for x in range(0, len(arr)):
                
                ## Set up Report variables
                ReportName = arr[x][0]
                if arr[x][1] is None:
                    AvgPT_P = float(0)
                else:
                    AvgPT_P = float(arr[x][1]) ##Pass - Average Processing Time in minutes
                if arr[x][2] is None:
                    StDevPT_P = float(0)
                else:
                    StDevPT_P = float(arr[x][2]) ##Pass - StDev Processing Time in minutes
                if arr[x][3] is None:
                    AvgSThr_P = float(0)
                else:
                    AvgSThr_P = float(arr[x][3]) ##Pass - Average Start Time HR in hours
                if arr[x][4] is None:
                    StDevSThr_P = float(0)
                else:                   
                    StDevSThr_P = float(arr[x][4]) ##Pass - StDev Start Time HR in hours
                if arr[x][5] is None:
                    AvgSTmi_P = float(0)
                else:   
                    AvgSTmi_P = float(arr[x][5]) ##Pass - Average Start Time Mi in minutes
                if arr[x][6] is None:
                    StDevSTmi_P = float(0)
                else:   
                    StDevSTmi_P = float(arr[x][6]) ##Pass - StDev Start Time Mi in minutes
                FRate = arr[x][7] ##Pass - Failure Rate Percentage
                Sun_P = arr[x][8] ##Pass - Runs Sunday
                Mon_P = arr[x][9] ##Pass - Runs Monday
                Tue_P = arr[x][10] ##Pass - Runs Tuesday
                Wed_P = arr[x][11] ##Pass - Runs Wednesday
                Thu_P = arr[x][12] ##Pass - Runs Thursday
                Fri_P = arr[x][13] ##Pass - Runs Friday
                Sat_P = arr[x][14] ##Pass - Runs Saturday
                ##==========================================================
                if arr[x][15] is None:
                    AvgPT_F = float(0)
                else:
                    AvgPT_F = float(arr[x][15]) ##Fail - Average Processing Time in minutes
                if arr[x][16] is None:
                    StDevPT_F = float(0)
                else:
                    StDevPT_F = float(arr[x][16]) ##Fail - StDev Processing Time in minutes
                if arr[x][17] is None:
                    AvgSThr_F = float(0)
                else:
                    AvgSThr_F = float(arr[x][17]) ##Fail - Average Start Time HR in hours
                if arr[x][18] is None:
                    StDevSThr_F = float(0)
                else:                   
                    StDevSThr_F = float(arr[x][18]) ##Fail - StDev Start Time HR in hours
                if arr[x][19] is None:
                    AvgSTmi_F = float(0)
                else:   
                    AvgSTmi_F = float(arr[x][19]) ##Fail - Average Start Time Mi in minutes
                if arr[x][20] is None:
                    StDevSTmi_F = float(0)
                else:   
                    StDevSTmi_F = float(arr[x][20]) ##Fail - StDev Start Time Mi in minutes
                Sun_F = arr[x][21] ##Fail - Runs Sunday
                Mon_F = arr[x][22] ##Fail - Runs Monday
                Tue_F = arr[x][23] ##Fail - Runs Tuesday
                Wed_F = arr[x][24] ##Fail - Runs Wednesday
                Thu_F = arr[x][25] ##Fail - Runs Thursday
                Fri_F = arr[x][26] ##Fail - Runs Friday
                Sat_F = arr[x][27] ##Fail - Runs Saturday
                ##==========================================================
                ReportFailed = s.RPTstatus(FRate)
                #print ReportFailed
                ReportStartTime_P = (random.normalvariate(AvgSThr_P, StDevSThr_P)*60 +
                                         random.normalvariate(AvgSTmi_P, StDevSTmi_P) + D*24*60)
                ReportStartTime_F = (random.normalvariate(AvgSThr_F, StDevSThr_F)*60 +
                                         random.normalvariate(AvgSTmi_F, StDevSTmi_F) + D*24*60)
                if ReportStartTime_P < 0:
                    ReportStartTime_P = 0
                if ReportStartTime_F < 0:
                    ReportStartTime_F = 0

                event1 = SimEvent(ReportName)
                
                if ((DOW == 0 and Sun_P == 1) or
                    (DOW == 1 and Mon_P == 1) or
                    (DOW == 2 and Tue_P == 1) or
                    (DOW == 3 and Wed_P == 1) or
                    (DOW == 4 and Thu_P == 1) or
                    (DOW == 5 and Fri_P == 1) or
                    (DOW == 6 and Sat_P == 1)):
                    if (ReportFailed):            
                        c = Customer(name = ReportName)
                        activate(c,c.visit(AvgPT_P, StDevPT_P,
                                           AvgSThr_P, StDevSThr_P,
                                           AvgSTmi_P, StDevSTmi_P,
                                           FRate,
                                           Sun_P, Mon_P, Tue_P, Wed_P, Thu_P, Fri_P, Sat_P,
                                           AvgPT_F, StDevPT_F,
                                           AvgSThr_F, StDevSThr_F,
                                           AvgSTmi_F, StDevSTmi_F,
                                           Sun_F, Mon_F, Tue_F, Wed_F, Thu_F, Fri_F, Sat_F,
                                           r=resource,WhatDay=D,WeekDay=DOW,MyEvent=event1,F=ReportFailed,run=run), at=ReportStartTime_F)
                        yield hold,self,0
                        c = Customer(name = ReportName)
                        activate(c,c.reSchedule(AvgPT_P, StDevPT_P,
                                           AvgSThr_P, StDevSThr_P,
                                           AvgSTmi_P, StDevSTmi_P,
                                           FRate,
                                           Sun_P, Mon_P, Tue_P, Wed_P, Thu_P, Fri_P, Sat_P,
                                           AvgPT_F, StDevPT_F,
                                           AvgSThr_F, StDevSThr_F,
                                           AvgSTmi_F, StDevSTmi_F,
                                           Sun_F, Mon_F, Tue_F, Wed_F, Thu_F, Fri_F, Sat_F,
                                           r=resource,WhatDay=D,WeekDay=DOW,MyEvent=event1,F=ReportFailed,run=run), at=ReportStartTime_F)
                        yield hold,self,0
                    else:
                        c = Customer(name = ReportName)
                        activate(c,c.visit(AvgPT_P, StDevPT_P,
                                           AvgSThr_P, StDevSThr_P,
                                           AvgSTmi_P, StDevSTmi_P,
                                           FRate,
                                           Sun_P, Mon_P, Tue_P, Wed_P, Thu_P, Fri_P, Sat_P,
                                           AvgPT_F, StDevPT_F,
                                           AvgSThr_F, StDevSThr_F,
                                           AvgSTmi_F, StDevSTmi_F,
                                           Sun_F, Mon_F, Tue_F, Wed_F, Thu_F, Fri_F, Sat_F,
                                           r=resource,WhatDay=D,WeekDay=DOW,MyEvent=event1,F=ReportFailed,run=run), at=ReportStartTime_P)
                        yield hold,self,0

            D = D + 1
            if DOW == 6:
                DOW = 0
            else:
                DOW = DOW + 1
                #print DOW

    def RPTstatus(self,Probability):
        return random.random() < Probability


class Customer(Process):                                
    """ Customer arrives, gets served by the clerk, and leaves """
    
    def visit(self,AvgPT_P=0, StDevPT_P=0,
                   AvgSThr_P=0, StDevSThr_P=0,
                   AvgSTmi_P=0, StDevSTmi_P=0,
                   FRate=0,
                   Sun_P=0, Mon_P=0, Tue_P=0, Wed_P=0, Thu_P=0, Fri_P=0, Sat_P=0,
                   AvgPT_F=0, StDevPT_F=0,
                   AvgSThr_F=0, StDevSThr_F=0,
                   AvgSTmi_F=0, StDevSTmi_F=0,
                   Sun_F=0, Mon_F=0, Tue_F=0, Wed_F=0, Thu_F=0, Fri_F=0, Sat_F=0,
                   r=0,WhatDay=0,WeekDay=0,MyEvent=0,F=False,Attempt=0,run=0):
        
        arrive = now()       #arrival time
        #print "We are in Day " + str(WhatDay)
        #print "%7.4f %s: Here I am"%(now(),self.name)
        
        yield request,self,r    #request resource
        wait = now()-arrive  #waiting time
        #print "%8.3f %s: Waited %6.3f"%(now(),self.name,wait)


        if (F):
            #print "%7.4f %s: Report Failed"%(now(),self.name)
            ProcessingTime_F = random.normalvariate(AvgPT_F, StDevPT_F)
            if ProcessingTime_F < 0:
                ProcessingTime_F = 0
            yield hold,self,ProcessingTime_F  #time spent processing report
            
            yield release,self,r    #relsease resource
            MyEvent.signal()
            #print "%7.4f %s: Report completed"%(now(),self.name)
            ReportDetails.append([self.name, arrive, now(), (now() - arrive), wait, F, Attempt, WhatDay, WeekDay, run])
        else:
            #print "%7.4f %s: Report Passed"%(now(),self.name)
            ProcessingTime_P = random.normalvariate(AvgPT_P, StDevPT_P)
            if ProcessingTime_P < 0:
                ProcessingTime_P = 0
            yield hold,self,ProcessingTime_P  #time spent processing report
            
            yield release,self,r    #release resource
            #print "%7.4f %s: Report completed"%(now(),self.name)
            ReportDetails.append([self.name, arrive, now(), (now() - arrive),  wait, F, Attempt, WhatDay, WeekDay, run])

    def reSchedule(self,AvgPT_P=0, StDevPT_P=0,
                   AvgSThr_P=0, StDevSThr_P=0,
                   AvgSTmi_P=0, StDevSTmi_P=0,
                   FRate=0,
                   Sun_P=0, Mon_P=0, Tue_P=0, Wed_P=0, Thu_P=0, Fri_P=0, Sat_P=0,
                   AvgPT_F=0, StDevPT_F=0,
                   AvgSThr_F=0, StDevSThr_F=0,
                   AvgSTmi_F=0, StDevSTmi_F=0,
                   Sun_F=0, Mon_F=0, Tue_F=0, Wed_F=0, Thu_F=0, Fri_F=0, Sat_F=0,
                   r=0,WhatDay=0,WeekDay=0,MyEvent=0,F=False,run=0):

        Attempts = ServerRetries       #Max number of retries

        while (Attempts > 0 and F == True):
            #print self.name + " attempts left " + str(Attempts)
            #print F
            yield waitevent, self, MyEvent #wait until previous attempt has completed
            #print self.eventsFired
            yield hold,self,RetryDelay #wait x number of minutes before retry

            RptFailed = s.RPTstatus(FRate)
            F = RptFailed
            WhatDay = int(now()/(24*60))

            ## Make sure WeekDay is between 0 and 6
            if WeekDay >= 7:
                WeekDay = WeekDay - (7*int(WeekDay/7))
            AttemptNumber = (ServerRetries - Attempts) + 1
            
            c = Customer(name = self.name)
            activate(c,c.visit(AvgPT_P, StDevPT_P,
                               AvgSThr_P, StDevSThr_P,
                               AvgSTmi_P, StDevSTmi_P,
                               FRate,
                               Sun_P, Mon_P, Tue_P, Wed_P, Thu_P, Fri_P, Sat_P,
                               AvgPT_F, StDevPT_F,
                               AvgSThr_F, StDevSThr_F,
                               AvgSTmi_F, StDevSTmi_F,
                               Sun_F, Mon_F, Tue_F, Wed_F, Thu_F, Fri_F, Sat_F,
                               r,WhatDay,WeekDay,MyEvent,F,AttemptNumber,run), at=0.0)
            yield hold,self,0

            if (F): #if report failed again
                Attempts = Attempts - 1
                



## Experiment data ------------------------------
ReportDetails = [] # initialize array, all report details
maxTime = int(24*60*7)
seed()
ServerCapacity = int(2)   
k = Resource(capacity=ServerCapacity, name="SSRS2005", unitName="Slots", qType=FIFO, preemptable=False,
monitored=True, monitorType=Monitor)
Days = 0
MaxDays = 6
DayOfWeek = 0
ServerRetries = 3
RetryDelay = 15

## Experiment/Model -----------------------------------
for rep in range(1, 2):
    initialize()
    s = Source(name='Source')
    activate(s, s.generate(D=Days, MD=MaxDays, DOW=DayOfWeek, resource=k, run=rep), at=0.0)
    simulate(until=maxTime)

## Results ----------------------------------------------
#print k
WaitSumm = k.waitMon.count(), k.waitMon.mean(), k.waitMon.var(), k.waitMon.total()
print WaitSumm
ActiveSumm = k.actMon.count(), k.actMon.mean(), k.actMon.var(), k.actMon.total()
print ActiveSumm

#print ReportDetails

CurrentTime = datetime.datetime.now()
CurrentTime = CurrentTime.strftime("%Y-%m-%d_%H-%M-%S")

with open('ReportDetails_' + CurrentTime + '.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(['ReportName', 'TimeStart', 'TimeEnd', 'ProcessingTime', 'WaitTime', 'RptFailed', 'RptAttempt', 'Day', 'WeekDay', 'Replication'])
    writer.writerows(ReportDetails)

with open('ServerActiveDetails_' + CurrentTime + '.csv', 'wb') as a: 
    writer1 = csv.writer(a)
    writer1.writerow(['TimeMin', 'ActiveSlots'])
    writer1.writerows(k.actMon)

with open('ServerWaitingDetails_' + CurrentTime + '.csv', 'wb') as b: 
    writer2 = csv.writer(b)
    writer2.writerow(['TimeMin', 'NumberWaiting'])
    writer2.writerows(k.waitMon)

with open('ReportSummaryStats_' + CurrentTime + '.csv', 'wb') as c: 
    writer3 = csv.writer(c)
    writer3.writerow(['ReportName', 'AvgProcessingTimeT_P', 'StDevProcessingTime_P', 'AvgStartTimehr_P',
                      'StDevStartTimehr_P', 'AvgStartTimemi_P', 'StDevStartTimemi_P', 'FailureRate',
                      'Sun_P', 'Mon_P', 'Tue_P', 'Wed_P', 'Thu_P', 'Fri_P', 'Sat_P',
                      'AvgProcessingTimeT_F', 'StDevProcessingTime_F', 'AvgStartTimehr_F',
                      'StDevStartTimehr_F', 'AvgStartTimemi_F', 'StDevStartTimemi_F', 
                      'Sun_F', 'Mon_F', 'Tue_F', 'Wed_F', 'Thu_F', 'Fri_F', 'Sat_F'])
    writer3.writerows(arr)
