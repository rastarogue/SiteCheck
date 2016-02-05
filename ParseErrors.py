# -*- coding: utf-8 -*-
"""
Created on Tue Feb 02 15:47:16 2016

@author: Liam McAloon
"""

import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

lines=[]

day=89400
week=7*day
month=30*day
year=365*day

class error:
    def __init__(self, date ,run_time, errors, count, ce, rt, ct, uk, status_bad):
        self.date=time.strptime(date)
        self.raw_time=time.mktime(self.date)
        self.plot_time=mdates.date2num(datetime.fromtimestamp(self.raw_time))
        self.run_time=float(run_time)
        self.errors=int(errors)
        self.count=int(count)
#        self.ce=ce
#        self.rt=rt
#        self.ct=ct
#        self.uk=uk
#        self.bad=status_bad
        self.ce=responses(ce)
        self.rt=responses(rt)
        self.ct=responses(ct)
        self.uk=responses(uk)
        self.bad=responses(status_bad)
        
    def __str__(self):
        string_date=time.asctime(self.date)
        string_gen="Date: "+string_date+" Number of Errors: "+str(self.errors)
        return string_gen
    
class responses:
    def __init__(self,error_chain):
        temp=error_chain.split('+')
        self.number=int(temp[0])
        self.list=[]
        if self.number!=0:
            for item in temp[1:]:
                self.list.append(item)
        
    
    
logs=open('log.txt','r')
for line in logs:
    #print line
    lines.append(line)
logs.close()

#print lines

lists=[]
for line in lines:
    test=line.split('|')
    #print test
    lists.append(test[0:-1])
#print lists

logs=[]
for line in lists:
    temp=error(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8])
    print temp
    logs.append(temp)
#print logs
    
x=[]    
y=[]
for line in logs:
    x.append(line.plot_time)
    y.append(line.errors)

fig, ax = plt.subplots()
plt.plot(x, y, 'ro')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_minor_locator(mdates.HourLocator())
plt.tick_params(which='both', width=2)
plt.tick_params(which='major', length=7)
plt.tick_params(which='minor', length=4, color='r')

plt.gcf().autofmt_xdate()
plt.show()
