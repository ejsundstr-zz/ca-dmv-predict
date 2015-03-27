
#Selenium attempt
from selenium import webdriver
import numpy as np


def wait_times(driver,number):
  office_url = 'http://apps.dmv.ca.gov/web/fieldoffice.html?number=' + str(number)
  driver.get(office_url)
  cells = driver.find_element_by_id("WaitTimesData").find_elements_by_class_name("cell")
  if(len(cells) > 1):
      try:
        appt = int(cells[1].text.split(':')[0])*60+int(cells[1].text.split(':')[1])
        break
        appt = np.nan
      try:
        non = int(cells[3].text.split(':')[0])*60+int(cells[1].text.split(':')[3])
        break
      except:
        non = np.nan
    return [appt,non]
  else:
    return [np.nan,np.nan]

