#!/usr/bin/env python3

import pandas as pd
import requests

#def add_new_office(df,name):
  
#def swap_id(df,kwargs):


#TODO add things to make this more fault tolerant including converting to a new set of numbers for each office
#for now returning a duplicated list one by number and one by officename
def update_offices(old_by_id=False):
  '''Update the office dictionaries
  
     Sends an http request for the dmv offices json 
     Creates and returns two redundant python dictionaries 
        one by name and the other by id.
     Also checks if the dictionary has changed 
       (new elements/change of id/etc)
       and returns an array of functions to call on the 
  '''
  by_id = {} #dict by id
  by_name = {} #dict by name
  #list of tuples of (functions,arguments) to update the df
  update = [] 
  with requests.Session() as session:
    response = session.get('http://apps.dmv.ca.gov/web/data/foims_offices_min.json?_=1426900468274');
    offices = response.json()['foims_offices']['offices']
    for o in offices:
      by_id[int(o['number'])] = o
      by_name[o['name']] = o

  '''for k in old_by_id:
    #Missing id
    if k not in by_id:
      #Check if the id has changed:
      if old_by_id[k]['name'] in by_name:
           
      #A new office:
      elif len(old_by_id) < len(by_id):
        update.append((add_new_offices,by_id[k]['name']))
      else:
        error_str = "I don't know how to fix the dictionary discrepency"'''
  return by_id, by_name, update

def print_offices_4_map():
  office_dict = {} 
  with requests.Session() as session:
    response = session.get('http://apps.dmv.ca.gov/web/data/foims_offices_min.json?_=1426900468274');
    offices = response.json()['foims_offices']['offices']
    f = open('offices.js','w')
    f.write('var offices = [\n')
    for o in offices:
      f.write('{\n') 
      f.write('  number    : {:d},\n'.format(o['number']))
      f.write('  name      : \'{:s}\',\n'.format(o['name']))
      f.write('  latitude  : {:s},\n'.format(o['latitude']))
      f.write('  longitude : {:s},\n'.format(o['longitude']))
      f.write('  address   : \'{:s}\'\n'.format(o['address']))
      f.write('},\n') 
    f.write('];\n')

