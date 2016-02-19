# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 15:25:37 2015

@author: liam
"""

import shutil

def copylog():
    dest="C:\wamp\www\cgi-bin\log.txt"
    shutil.copy2("C:\Users\Liam\Desktop\Git Site Check\SiteCheck\log.txt",dest)

