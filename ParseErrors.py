# -*- coding: utf-8 -*-
"""
Created on Tue Feb 02 15:47:16 2016

@author: Liam McAloon
"""

import time
lines=[]

day=89400
week=7*day
month=30*day
year=365*day

class error:
    def __init__(self, date ,run_time, errors, count, ce, rt, ct, uk, status_bad):
        self.date=time.strptime(date)
        self.run_time=float(run_time)
        self.errors=int(errors)
        self.count=int(count)
        self.ce=responses(ce)
        self.rt=responses(rt)
        self.ct=responses(ct)
        self.uk=responses(uk)
        self.bad=responses(status_bad)
    
class responses:
    def __init__(self,ce):
        pass
    
    
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

print lists