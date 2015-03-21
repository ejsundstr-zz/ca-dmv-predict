
#Selenium attempt
from selenium import webdriver


def get_wait_times(driver,number):
  office_url = 'http://apps.dmv.ca.gov/web/fieldoffice.html?number=' + str(number)
  driver.get(office_url)
  cells = driver.find_element_by_id("WaitTimesData").find_elements_by_class_name("cell")
  if(len(cells) > 1):
    return [cells[1].text,cells[3].text]
  else:
    return ['NaN','Nan']

driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)
for i in range(0,10):
  get_wait_times(driver,504)
