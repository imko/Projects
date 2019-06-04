"""Used for testing"""
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from bs4 import element 
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen 
import re 

url = "https://courses.students.ubc.ca/cs/courseschedule?sesscd=S&pname=subjarea&tname=subj-section&course=113&sessyr=2019&section=971&dept=ATSC"
driver = webdriver.Chrome() 

driver.get(url)
page = soup(driver.page_source, "html.parser")

for detail in page.find_all("table", {"class": "table table-striped"}):
	instructor_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[3]")
	list = re.split(":|\n", str(instructor_table.text))

	try: 
		index_instructor = list.index("Instructor")
		index_ta = list.index("TA")
		instructor_list = [s.strip() for s in list[index_instructor+1:index_ta]]
		ta_list = [s.strip() for s in list[index_ta+1:]]
	except:
		instructor_list = [s.strip() for s in list[index_instructor+1:]]
		ta_list = None 
	
	tmp = (instructor_list, ta_list)
	print(tmp)

driver.quit()
