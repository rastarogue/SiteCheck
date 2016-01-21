# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 16:44:55 2016

@author: liam
"""

import os
import requests
import xlrd
import time
import sendemail
        
        
def parsedomain(domain):
    """ Cleans up the domains from the VSD to be useable by the program.
    Prepends www, no http:// or https://"""
    domain=domain[domain.find("://")+3:].strip("/")
    if (domain[:3]!="www"):
        domain="www."+domain
    return domain
    
    
def build_page(content):
    """ Builds a webpage, adding header, html and body tags. Takes in HTML content """
    header='<head><meta http-equiv="refresh" content="60";/><title>Site Status</title></head>'
    html_open='<html>'
    html_close='</html>'
    body_open='<body>'
    body_close='</body>'
    return html_open+header+body_open+content+body_close+html_close

def test_sites(domainlist):
    """ Takes a cleaned up list of domain, tries to load them if they are CMS6, not a blank domain and hosted by Vision If the response is 200, good, anything else count the error"""
    errors=0
    t1=time.time()
    results=[]
    index=0
    count=0
    for domain in domainlist:
        if (cmstype[index]=="6.0" and domain!="www." and hostlist[index]=="Vision"):
            count=count+1
            try:
                resp=requests.head("http://"+domain, timeout=fail_time).status_code
                #print "Site: "+clientname[index]+"\t Status Code: "+str(resp)
                results.append([clientname[index],str(resp),server[index],"http://"+domain])
                if (resp!=200 and resp!=302):
                    errors=errors+1
                    print resp
            except requests.exceptions.ConnectTimeout:
                results.append([clientname[index],'timeout',server[index],"http://"+domain])
                errors=errors+1
            except:
                results.append([clientname[index],'0',server[index],"http://"+domain])
                errors=errors+1
                #print "Site: "+clientname[index]+" is having trouble"
        index=index+1
    t2=time.time()
    run_time=t2-t1
    return run_time, results, errors, count

def process_results(run_time, results, errors, count, last_five):
    str_rep="Number of sites checked: "+str(count)+" <br>\nNumber of errors: "+str(errors)+" <br>\nRun Time: "+str(run_time/60.0)[0:4]+"mins <br>\n"

    str_error=''
    prnt_error=''
    if errors!=0:
        for row in results:
            if (row[1]!='200' and row[1]!='302'):
                str_error=str_error+row[1]+": "+'<a href=\"'+row[3]+'\">'+row[0]+'</a>'+" server: "+row[2]+" <br>\n"
                prnt_error=str_error+row[1]+": "+row[0]+" server: "+row[2]+" <br>\n"
    output=time.ctime()+" <br>\n"+str_rep+prnt_error+str_break
    print output
    output=time.ctime()+" <br>\n"+str_rep+str_error+str_break
    text=open('C:\wamp\www\check_results.html','a')
    text.write(output)
    text.close()
    html=open('C:\wamp\www\site_status.html','w')
    last_five[4]=last_five[3]
    last_five[3]=last_five[2]
    last_five[2]=last_five[1]
    last_five[1]=last_five[0]
    last_five[0]=output
    content=last_five[0]+last_five[1]+last_five[2]+last_five[3]+last_five[4]
    html.write(build_page(content))
    html.close()

######################################################################   
os.system("ipconfig /flushdns")
book=xlrd.open_workbook("Z:/Vision Documents/Account Management/Vision Site Database.xlsx")
sh=book.sheet_by_index(0)
domainlist1=[]
domainlist=[]
clientname=[]
hostlist=[]
cmstype=[]
maint=[]
server=[]
str_break='=====================================================================<br>\n'
fail_time=15.0
pause=60

#email info
fromaddr = 'rastarogue@gmail.com'
toaddrs  = ['liam.at.vision@gmail.com','lmcaloon@visioninternet.com']
msg = ''
subject='Site Alert'


for row in range(sh.nrows):
    if (row>0):
        clientname.append(str(sh.cell_value(rowx=row,colx=0)))
        domainlist1.append(str(sh.cell_value(rowx=row,colx=8)))
        hostlist.append(str(sh.cell_value(rowx=row,colx=4)))
        cmstype.append(str(sh.cell_value(rowx=row,colx=3)))
        maint.append(str(sh.cell_value(rowx=row,colx=5)))
        server.append(str(sh.cell_value(rowx=row,colx=18)))
 
for domain in domainlist1:
    domainlist.append(parsedomain(domain))

start_time=time.time()
end_time=start_time+6048000

last_five=['','','','','']

while(time.time()<=end_time):
    os.system("ipconfig /flushdns")
    print "\n"
    run_time, results, errors, count = test_sites(domainlist)
    process_results(run_time, results, errors, count, last_five)
    time.sleep(pause)
        
    
    
