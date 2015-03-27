
# coding: utf-8

# Import and set style
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.style.use('forkedriver')
# read the data
df = pd.read_csv('waitTime.csv',parse_dates=[0],index_col=[0])

trimmed = df['2013-02-11':'2013-03-15']
retrim = trimmed.resample('5min')
#remove the weekends
cleaned = retrim[retrim.index.dayofweek < 5]
#remove the unopened hours
cleaned = cleaned[cleaned.index.hour > 7]
cleaned = cleaned[cleaned.index.hour < 18]

grouped = cleaned.groupby(lambda x :(x.dayofweek, x.hour, x.minute)).mean()
for officename in grouped:
  fig =plt.figure(figsize=(15,5))
  grouped[officename].plot()
  xlim = plt.xlim()
  loc = [ 118. , 252. , 360. , 480. ]
  temp = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
  plt.xticks(loc,['', '', '', ''])
  plt.title('Averaged Non-Appointment Wait Times for ' + officename,fontsize=18)
  plt.ylabel('Time (minutes)')
  plt.text(43, -6, 'Monday',fontsize=12)
  plt.text(160, -6, 'Tuesday',fontsize=12)
  plt.text(275, -6, 'Wednesday',fontsize=12)
  plt.text(390, -6, 'Thursday',fontsize=12)
  plt.text(525, -6, 'Friday',fontsize=12)
  plt.savefig('plots/'+officename.replace(' ','_')+'.png')
  plt.close()

