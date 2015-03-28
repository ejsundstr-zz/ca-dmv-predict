"""Functions and variables for testing if offices are open
 
   This code can only be run from the CA time zone 
   Could be cleaned up but python timezone stuff is hard...

"""

import datetime
import math

#This is only setup with holidays for 2015

def is_holiday(dt):
  holidays = [datetime.datetime.strptime('May 25 Monday 2015','%B %d %A %Y'),
            datetime.datetime.strptime('July 4 Saturday 2015','%B %d %A %Y'),
            datetime.datetime.strptime('September 7 Monday  2015','%B %d %A %Y'),
            datetime.datetime.strptime('November 11 Wednesday 2015','%B %d %A %Y'),
            datetime.datetime.strptime('November 26 Thursday 2015','%B %d %A %Y'),
            datetime.datetime.strptime('November 27 Friday 2015','%B %d %A %Y'),
            datetime.datetime.strptime('December 25 Friday 2015','%B %d %A %Y')]
  #now holidays
  for h in holidays:
    #if the current date time is greater than
    #  the holiday and less than the next day
    if h < dt and dt < h + datetime.timedelta(1):
      #It's a Holiday
      return True
  return False

#Could be optimized... Checks the holidays for every office could exchange those loops..
def is_open(office,dt):
  wkstr = office['officeHours']
  #Convert the DMV's listed hours into a list by day.
  week = ['n' if d == 'n' else d.split('-') for d in wkstr.split(',')]
  #This is quick so check it first
  if len(week[dt.weekday()]) < 2:
    return False
  else:
    day = week[dt.weekday()]
    cur = dt.hour*100+dt.minute
    #return if cur is between the opening and closing time
    return (int(day[0]) < cur and cur < int(day[1]))

def open_close(offices):
  #Convert the DMV's listed hours into a list by day.
  wkdy_open = [2359,2359,2359,2359,2359,2359,2359]
  wkdy_close = [  0,   0,   0,   0,   0,   0,   0]
  for o in offices:
    hourlist = offices[o]['officeHours'].split(',')
    cur_open = [2359 if d == 'n' else int(d.split('-')[0]) for d in hourlist]
    cur_close = [0 if d == 'n' else int(d.split('-')[1]) for d in hourlist]
    wkdy_open = [min(a,b) for a,b in zip(wkdy_open,cur_open)]
    wkdy_close = [max(a,b) for a,b in zip(wkdy_close,cur_close)]
  wkdy_open =  [ datetime.time(math.floor(t/100),int(t)%100) for t in wkdy_open ]
  wkdy_close = [ datetime.time(math.floor(t/100),int(t)%100) for t in wkdy_close ]
  return wkdy_open, wkdy_close 
