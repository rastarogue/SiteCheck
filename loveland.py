# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 15:59:22 2016

@author: liam
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 16:44:55 2016

@author: liam
"""

import os
import requests
import shutil
import time
        

def test_sites(domainlist):
    """ Takes a cleaned up list of domain, tries to load them if they are CMS6, not a blank domain and hosted by Vision If the response is 200, good, anything else count the error"""
    errors=0
    t1=time.time()
    results=[]
    index=0
    count=0
    count=len(domainlist)
    for domain in domainlist:
        try:
            resp=requests.head("http://"+domain, timeout=fail_time).status_code
            results.append([clientname[index],str(resp),'cms5c',"http://"+domain,str(resp)])
            if (resp!=200 and resp!=302):
                errors=errors+1
                print resp
        except requests.exceptions.ConnectTimeout as ct:
            results.append([clientname[index],"ConnectTimeout="+str(fail_time), server[index], "http://"+domain,"ConnectTimeout"])
            errors=errors+1
        except requests.exceptions.ReadTimeout as rt:
            results.append([clientname[index],"ReadTimeout="+str(fail_time), server[index], "http://"+domain,"ReadTimeout"])
            errors=errors+1
        except requests.ConnectionError as ce:
            results.append([clientname[index],"Connection Error",server[index],"http://"+domain,"ConnectionError"])
            errors=errors+1
        except requests.RequestException as g:
            results.append([clientname[index],'unknown',server[index],"http://"+domain,"unknown"])
            errors=errors+1                    
        index=index+1
    t2=time.time()
    run_time=t2-t1
    return run_time, results, errors, count

def process_errors(thing):
    str_error=str(thing[0])
    for row in thing[1]:
        str_error=str_error+"+"+row
    return str_error+"|"

def process_results(run_time, results, errors, count, log):
    try:
        temp=open('log_loveland.txt','a')
    except:
        temp=open('log_loveland.txt','w')
    ce=[0,[]]
    rt=[0,[]]
    ct=[0,[]]
    uk=[0,[]]
    status_good=[0,[]]
    status_bad=[0,[]]
    for row in results:
        if row[4]=="ConnectionError":
            ce[0]=ce[0]+1
            ce[1].append(row[0])
        elif row[4]=="ReadTimeout":
            rt[0]=rt[0]+1
            rt[1].append(row[0])
        elif row[4]=="ConnectTimeout":
            ct[0]=ct[0]+1
            ct[1].append(row[0])
        elif row[4]=="unknown":
            uk[0]=uk[0]+1
            uk[1].append(row[0])
        else:
            if (row[4]=='200' or row[4]=='302'):
                status_good[0]=status_good[0]+1
                status_good[1].append(row[0])
            else:
                status_bad[0]=status_bad[0]+1
                status_bad[1].append(row[0])  
    check=[time.ctime(), run_time, errors, count, ce, rt, ct, uk, status_bad, status_good]
    processed=process_errors(ce)+process_errors(rt)+process_errors(ct)+process_errors(uk)+process_errors(status_bad)
    check_write=time.ctime()+"|"+str(run_time)+"|"+str(errors)+"|"+str(count)+"|"+processed+"\n"
    temp.write(check_write)
    temp.close()
    print check_write
    return check


######################################################################   
fail_time=15.0
pause=120
log=[]


domainlist=['www.ci.loveland.co.us','www.colliergov.net']
clientname=['Loveland, City of - CO', 'Collier County - FL']
server=['cms5c','unknown']

start_time=time.time()
end_time=start_time+6048000

def copylog():
    dest="C:\wamp\www\log_loveland.txt"
    shutil.copy2("C:\Users\Liam\Desktop\Git Site Check\SiteCheck\log_loveland.txt",dest)

while(time.time()<=end_time):
    os.system("ipconfig /flushdns")
    print "\n"
    run_time, results, errors, count = test_sites(domainlist)
    process_results(run_time,results,errors,count,log)[0:8]
    copylog()
    time.sleep(pause)
        
    
    
