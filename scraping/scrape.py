
#Selenium attempt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import numpy as np


def wait_times(driver,number):
  office_url = 'http://apps.dmv.ca.gov/web/fieldoffice.html?number=' + str(number)
  driver.get(office_url)

  try:
    element = WebDriverWait(driver, 2).until(
      EC.presence_of_element_located((By.ID, "WaitTimesData"))
      )
    cells = element.find_elements_by_class_name("cell")
    if(len(cells) > 1):
      try:
        appt = int(cells[1].text.split(':')[0])*60+int(cells[1].text.split(':')[1])
        non = int(cells[3].text.split(':')[0])*60+int(cells[3].text.split(':')[1])
      except:
        non = np.nan
        appt = np.nan
      return [appt,non]
    else:
      return [np.nan,np.nan]
  except:
    print("Always Excepting")
    return [np.nan,np.nan]

