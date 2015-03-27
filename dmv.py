#!/usr/bin/env python

import SimpleHTMLParser
import re
import os
import sys
import time
import urllib2
import pickle
import datetime



def to_minutes(thetime):
  return 60*thetime.tm_hour+thetime.tm_min

def is_open(office_times):
  cur_time = time.localtime()
  cur_min = to_minutes(cur_time)
  day = time.strftime('%A',cur_time)
  if day in office_times:
    if cur_min > office_times[day][0] and cur_min < office_times[day][1]:
      return True
  return False


#rev_weekdict ={ 
#'Monday': ['M','Mo','Mon','Monday'],
#'Tuesday': ['Tu','Tu','Tue','Tues','Tuesday'],
#'Wednesday': ['W','We','Wed','Wednesday'],
#'Thursday': ['Th','Thur','Thurs','Thursday'],
#'Friday': ['F','Fr','Fri','Friday'],
#'Saturday': ['S','Sa','Sat','Saturday'],
#'Sunday': ['Su','Sun','Sunday']
#}
#weekdict = {}
#for d in rev_weekdict.keys():
#  for abb in rev_weekdict[d]:
#    weekdict[abb] = d
#print weekdict

weekdict ={'Wed': 'Wednesday', 'Sun': 'Sunday', 'Fri': 'Friday', 'Tu': 'Tuesday', 'Thurs': 'Thursday', 'Thursday': 'Thursday', 'Sunday': 'Sunday', 'Th': 'Thursday', 'Fr': 'Friday', 'Monday': 'Monday', 'Friday': 'Friday', 'Mon': 'Monday', 'Tue': 'Tuesday', 'F': 'Friday', 'Mo': 'Monday', 'M': 'Monday', 'Tues': 'Tuesday', 'Su': 'Sunday', 'Wednesday': 'Wednesday', 'S': 'Saturday', 'W': 'Wednesday', 'Sa': 'Saturday', 'We': 'Wednesday', 'Tuesday': 'Tuesday', 'Thur': 'Thursday', 'Saturday': 'Saturday', 'Sat': 'Saturday'}

offices_filename = 'ca-dmv-office.pkl'
offices_update = True
offices = {}
'''
#Reading and unpickling
if os.path.exists(offices_filename):
  temp_stat = os.stat(offices_filename)
  if (time.time() - temp_stat.st_mtime) < 432000:
    offices_update = False
    offices_file = open(offices_filename,'rb')
    offices = pickle.load(offices_file)
 '''
if offices_update == True:

headerStr ='Time Stamp, '
for o in sorted(offices.keys()):
  headerStr += o +', '

appt_time_file = open("apptWaitTime.csv",'w+')
time_file = open("waitTime.csv",'w+')
appt_time_file.write(headerStr+'\n')
time_file.write(headerStr+'\n')

allClosed = True

while True:
  actual_time = time.time()
  time_line = time.asctime(time.localtime(actual_time)) + ','
  appt_time_line = time_line
  for o in sorted(offices.keys()):
    #print "Getting information for Office " + o
    offices[o]['apptWaitTime'][actual_time] = -10
    offices[o]['nonApptWaitTime'][actual_time] = -10
    if is_open(offices[o]['times']):
      allClosed = False
      office_page = urllib2.urlopen('http://apps.dmv.ca.gov/fo/offices/appl/fo_data_read.jsp?foNumb='+offices[o]['id']+'&server=en')
      for line in office_page:
        if 'showClosedDiv' in line:
          if not 'display:none' in line:
            break
        elif 'noCustWait' in line:
          if not 'display:none' in line:
            break
        elif 'custWait' in line:
          if 'display:none' in line:
            break
        elif 'apptWaitTime' in line:
          mod_line = line.split('>')[1]
          mod_line = mod_line.split('<')[0]
          mod_line = mod_line.strip()
          minutes = -10
          if '***' not in mod_line and ':' in mod_line:
            minutes = int(mod_line.split(":")[0])*60+int(mod_line.split(":")[1])
          offices[o]['apptWaitTime'][actual_time] = minutes
        elif 'nonApptWaitTime' in line:
          mod_line = line.split('>')[1]
          mod_line = mod_line.split('<')[0]
          mod_line = mod_line.strip()
          minutes = -10
          if '***' not in mod_line and ':' in mod_line:
            minutes = int(mod_line.split(":")[0])*60+int(mod_line.split(":")[1])
          offices[o]['nonApptWaitTime'][actual_time] = minutes
    appt_time_line += '{0:d}, '.format(offices[o]['apptWaitTime'][actual_time])
    time_line += '{0:d}, '.format(offices[o]['nonApptWaitTime'][actual_time])
  appt_time_file.write(appt_time_line+'\n')
  time_file.write(time_line+'\n')
  appt_time_file.flush()
  time_file.flush()
  if allClosed:
    time.sleep(3600)
  else:
    time.sleep(10)
  allClosed = True
  



