# -*- coding: utf-8 -*-
"""
Created on Tue Feb 02 15:47:16 2016

@author: Liam McAloon
"""

import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

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

#print logs

def gen_plot(start_time, end_time, time_frame,logs):
    plt.ioff()
    print "Start Time: "+str(start_time)
    print "End Time: "+str(end_time)
    title='Errors_over_Time_'+time_frame
    x=[]    
    y=[]
    for line in logs:
        if (line.raw_time>=start_time and line.raw_time<=end_time):
            x.append(line.plot_time)
            y.append(line.errors)
            #print line.date
    #time.sleep(10)
    fig, ax = plt.subplots()
    plt.bar(x, y, width=.005, linewidth=0)
    plt.ylabel('Number of Errors')
    plt.xlabel('Date/Time of check')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_minor_locator(mdates.HourLocator(range(1,24,2)))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
    ax.yaxis.minor_label_orientation=-3.14/4
    plt.ylim(ymin=0, ymax=(max(y)+1))
    plt.tick_params(which='both', width=2)
    plt.tick_params(which='major', length=16,pad=20)
    plt.tick_params(which='minor', length=8, color='r')
    plt.xticks(rotation=45)
    plt.title(title)
    plt.gcf().autofmt_xdate()
    fig.set_size_inches(30,10)
    plt.savefig('C:\\wamp\\www\\'+title+'.png',bbox_inches='tight')
    plt.close(fig)
    #plt.show()
    
    return "figure saved: "+title

def generate_graphs():
    lines=[]
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
        #print temp
        logs.append(temp)
    
    time.clock()
    end_time=time.mktime(time.localtime())
    time_frame="Last_Month"
    print gen_plot(end_time-month, end_time, time_frame, logs)
    time.clock()
    time_frame="Last_Week"
    print gen_plot(end_time-week, end_time, time_frame, logs)
    time.clock()
    time_frame="Last_48_Hours"
    print gen_plot(end_time-2*day, end_time, time_frame, logs)
    time.clock()
    time_frame="Last_24_Hours"
    print gen_plot(end_time-day, end_time, time_frame, logs)
    time.clock()