#!/usr/bin/env python

from HTMLParser import HTMLParser
import re
import os
import sys
import time
import urllib2
import pickle
import datetime

class MyHTMLParser(HTMLParser):
   def __init__(self):
      HTMLParser.__init__(self)
      self.data_list = []
   #def handle_starttag(self, tag, attrs):
      #print "Encountered a start tag:", tag
   #def handle_endtag(self, tag):
      #print "Encountered an end tag :", tag
   def handle_data(self, data):
      #print "Encountered some data  :", data
      self.data_list.append(data)
   def get_data(self):
      return self.data_list

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
#   for abb in rev_weekdict[d]:
#      weekdict[abb] = d
#print weekdict

weekdict ={'Wed': 'Wednesday', 'Sun': 'Sunday', 'Fri': 'Friday', 'Tu': 'Tuesday', 'Thurs': 'Thursday', 'Thursday': 'Thursday', 'Sunday': 'Sunday', 'Th': 'Thursday', 'Fr': 'Friday', 'Monday': 'Monday', 'Friday': 'Friday', 'Mon': 'Monday', 'Tue': 'Tuesday', 'F': 'Friday', 'Mo': 'Monday', 'M': 'Monday', 'Tues': 'Tuesday', 'Su': 'Sunday', 'Wednesday': 'Wednesday', 'S': 'Saturday', 'W': 'Wednesday', 'Sa': 'Saturday', 'We': 'Wednesday', 'Tuesday': 'Tuesday', 'Thur': 'Thursday', 'Saturday': 'Saturday', 'Sat': 'Saturday'}

offices_filename = 'ca-dmv-office.pkl'
offices_update = True
offices = {}

#Reading and unpickling
if os.path.exists(offices_filename):
   temp_stat = os.stat(offices_filename)
   if (time.time() - temp_stat.st_mtime) < 432000:
      offices_update = False
      offices_file = open(offices_filename,'rb')
      offices = pickle.load(offices_file)
 
if offices_update == True:
   main_page = urllib2.urlopen('http://apps.dmv.ca.gov/fo/offices/toc_fo.htm')
   for line in main_page:
      if 'http://apps.dmv.ca.gov/fo/offices/appl/fo_data_read.jsp?foNumb=' in line:
         refs = line.split('href')
         for r in refs:
            r = r.split("</a>")[0]
            r = r.replace("&nbsp;", " ")
            my_match = re.search("\s*=\s*\"http://apps\.dmv\.ca\.gov/fo/offices/appl/fo_data_read\.jsp\?foNumb=(\d+)&server=en\"\s*>\s*([\w\s).-]+)", r)
            if my_match != None:
               off_name = my_match.group(2).strip()
               offices[off_name] = {'id':my_match.group(1).strip()}
               #Grabbing the closing times for the offices
               office_page = urllib2.urlopen('http://apps.dmv.ca.gov/fo/offices/appl/fo_data_read.jsp?foNumb='+offices[off_name]['id']+'&server=en')
               str_times = {}
               oline = office_page.readline()
               while(oline != ''):
                  if 'hoursOpen' in oline and "display:block" in oline:
                     oline = office_page.readline()
                     html_parser = MyHTMLParser()
                     html_parser.feed(oline.strip())
                     data = html_parser.get_data()
                     for i in data:
                        days = i.split(':',1)[0].replace('.','')
                        hours = i.split(':',1)[1]
                        for d in days.split(','):
                           if d.strip() in weekdict:
                              str_times[weekdict[d.strip()]] = hours
                     break
                  if 'daysOpen' in oline and not "display:none" in oline:
                     oline = office_page.readline()
                     lines =[]
                     while 'div' not in oline:
                        if oline.strip() != '':
                           lines.append(oline)
                        oline = office_page.readline()
                     for l in lines:
                        html_parser = MyHTMLParser()
                        html_parser.feed(l.strip())
                        data = html_parser.get_data()
                        for i in data:
                           days = i.split(':',1)[0].replace('.','')
                           hours = i.split(':',1)[1]
                           for d in days.split(','):
                              if d.strip() in weekdict:
                                 str_times[weekdict[d.strip()]] = hours
                     break 
                  oline = office_page.readline()
               times = {} 
               for k in str_times.keys():
                  if 'Closed' in str_times[k]:
                     continue
                  time_range = str_times[k].split('-')
                  open_time = to_minutes(time.strptime(time_range[0].strip(),'%I:%M %p'))
                  close_time = to_minutes(time.strptime(time_range[1].strip(),'%I:%M %p'))
                  times[k]=[open_time,close_time]
               offices[off_name]['times'] = times
               offices[off_name]['apptWaitTime'] = {}
               offices[off_name]['nonApptWaitTime'] = {}
   offices_file = open(offices_filename,'wb')
   pickle.dump(offices,offices_file,-1)

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
   



