#!/usr/bin/env python

from SimpleHTMLParser import SimpleHTMLParser
from scrapin import get_wait_times
import requests
import os
import sys
import time
import urllib.request
import urllib.parse
import pickle
import datetime
import requests
from selenium import webdriver


office_dict = {}
main_url = 'http://apps.dmv.ca.gov/fo/offices/toc_fo.htm'
with requests.Session() as session:
  session.get(main_url)
  response = session.get('http://apps.dmv.ca.gov/web/data/foims_offices_min.json?_=1426900468274');
  fo_json = response.json()
  
  for o in fo_json['foims_offices']['offices']:
    office_dict[int(o['number'])] = o['name']
print("Finished Constructing Office List")

driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)
for office_id in office_dict.keys():
  wait_times = get_wait_times(driver,office_id)
  print(office_dict[office_id],wait_times[0],wait_times[1])


exit()
'''
Selenium attempt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

element = driver.find_element_by_id("passwd-id")


def update_offices():
  driver = webdriver.Firefox()
  main_url = 'http://apps.dmv.ca.gov/fo/offices/toc_fo.htm'
  driver.get(main_url)
  elem = driver.find_el
  assert "No results found." not in driver.page_source
  driver.close()
  main_url = 'http://apps.dmv.ca.gov/web/fieldoffice.html?number=510'
  user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
  values = {'name' : 'Eric Jon Sundstrom'}
  headers = { 'User-Agent' : user_agent }

  data  = urllib.parse.urlencode(values)
  data = data.encode('utf-8')
  req = urllib.request.Request(url, data, headers)
  response = urllib.request.urlopen(req)
  main_page = response.read()
  
  main_page = urllib.request.urlopen(main_url).read().decode()
  print(main_page)
  print(type(main_page))
  dumbout = open('Alturas.html','w')
  dumbout.write(main_page)
  dumbout.close()
'''

'''  for line in main_page:
    if 'http://apps.dmv.ca.gov/web/fieldoffice.html?number=' in line:
      print("CATS", line)
      refs = line.split('href')
      for r in refs:
        print(refs)
        r = r.split("</a>")[0]
        r = r.replace("&nbsp;", " ")
        my_match = re.search("\s*=\s*\"http://apps\.dmv\.ca\.gov/fo/offices/appl/fo_data_read\.jsp\?foNumb=(\d+)&server=en\"\s*>\s*([\w\s).-]+)", r)
        if my_match != None:
          off_name = my_match.group(2).strip()
          offices[off_name] = {'id':my_match.group(1).strip()}
          #Grabbing the closing times for the offices
          office_page = urllib.request.urlopen('http://apps.dmv.ca.gov/fo/offices/appl/fo_data_read.jsp?foNumb='+offices[off_name]['id']+'&server=en')
          str_times = {}
          oline = office_page.readline()
          while(oline != ''):
            if 'hoursOpen' in oline and "display:block" in oline:
              oline = office_page.readline()
              html_parser = SimpleHTMLParser()
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
                html_parser = SimpleHTMLParser()
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
  #offices_file = open(offices_filename,'wb')
  #pickle.dump(offices,offices_file,-1)
'''
update_offices()
