#!/usr/bin/env python

import sys
import time
import math
import os
import shutil
import argparse
import datetime
import subprocess as sp
try:
   import matplotlib
   import matplotlib.mlab as mlab
   import matplotlib.pyplot as pyplot
   UsingMatPlotLib=1
except ImportError:
   UsingMatPlotLib=0


strDesc='Makes and tetrahedron symmetric dissociation curve!'
parser=argparse.ArgumentParser(description=strDesc)
parser.add_argument('-s', '--save', action="store_true", help='Save the specific office as office.csv.')
parser.add_argument('-i', '--input', type=str, default='waitTime.csv', help='For an alternative csv file')
#parser.add_argument('-f', '--final', type=float, default=5.00000000, help='Specify the ending distance for the curve. Default: 5.0')
parser.add_argument('-o', '--office', action='append', default=['Oakland'],help='Specify offices you want to probe')
parser.add_argument('-p', '--plot', action="store_false",default=True, help='Plot using matplotlib')
parser.add_argument('-a', '--appt', action="store_true",default=False, help='Use the appointment wait time instead of just the usual one.')
 
args = parser.parse_args()
print args

data_file_name = args.input
if args.appt:
  data_file_name = 'apptWaitTime.csv' 

shutil.copy(data_file_name,data_file_name+'.tmp')

print data_file_name+'.tmp'
sp.call(['sed','-i','.bkup', '-E', '-e', "s/,[ ]*/,/g", data_file_name+'.tmp'])
#r = mlab.csv2rec(data_file_name+'.tmp')
#print r

data_file = open(data_file_name+'.tmp','r')

header = data_file.readline().split(',')


time_data = [] 
office_data = {}
office_index = {}
for o in args.office:
   if o in header:   
      office_data[o] = []
      office_index[o] = header.index(o)


line = data_file.readline()
while line !='':
   flag = False
   for o in args.office:
      if int(line.split(',')[office_index[o]]) != -10:
         office_data[o].append(int(line.split(',')[office_index[o]]))
         flag = True
   if flag:
      time_data.append(datetime.datetime.strptime(line.split(',')[0],'%a %b %d %H:%M:%S %Y'))
   line = data_file.readline()

fig = pyplot.figure()
ax = fig.add_subplot(111)
ax.plot(time_data,office_data[args.office[0]],'o-')

pyplot.savefig('what.svg')
#pyplot.show()
      
   
   



