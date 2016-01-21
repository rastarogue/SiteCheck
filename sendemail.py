# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 16:59:22 2016

@author: liam
"""

import smtplib

text=open('C:\Users\Liam\Desktop\Git Site Check\credentials.txt')
username = text.readline().strip('\n')
password = text.readline().strip('\n')
text.close()

def send_email(recipient, subject, body):
    gmail_user = username
    gmail_pwd = password
    FROM = username
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"