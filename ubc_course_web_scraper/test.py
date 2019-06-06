"""Used for testing"""
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from bs4 import element 
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen 
import re 

# multiple: "https://courses.students.ubc.ca/cs/courseschedule?sesscd=S&pname=subjarea&tname=subj-section&course=121&sessyr=2019&section=V01&dept=CPSC"
# single: "https://courses.students.ubc.ca/cs/courseschedule?sesscd=S&pname=subjarea&tname=subj-section&course=121&sessyr=2019&section=911&dept=CPSC"
# empty: "https://courses.students.ubc.ca/cs/courseschedule?sesscd=S&pname=subjarea&tname=subj-section&sessyr=2019&course=649&section=941&dept=CPSC"

url = "https://courses.students.ubc.ca/cs/courseschedule?sesscd=S&pname=subjarea&tname=subj-section&sessyr=2019&course=649&section=941&dept=CPSC"
driver = webdriver.Chrome() 

driver.get(url)
page = soup(driver.page_source, "html.parser")

table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[2]/tbody")
details = [] 
for tr in table.find_elements_by_xpath("./tr"):
	tmp = []
	for td in tr.find_elements_by_xpath("./td"):
		tmp.append(td.text)
	details.append(tmp)

print("LEN: " + str(len(tmp[1])))

summary_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[4]/tbody") 
seats = [] 
for tr in summary_table.find_elements_by_xpath("./tr"): 
	for td, k in enumerate(tr.find_elements_by_xpath("./td")): 
		if td == 1:
			seats.append(k.text) 

print(details)
print(seats[:4])


driver.quit()

# schedules = []
# schedules.append(
# 	{
# 		("Mon Tue Wed"):
# 		{
# 			"start_time": "9:30",
# 			"end_time": "11:30",
# 			"instructor": ["Allen, Dijkstra"],
# 			"ta": None,
# 			"building": "building_1", 
# 			"room": "room_1",
# 		}
# 	}
# )
# schedules.append(
# 	{
# 		("Thu Fri"):
# 		{
# 			"start_time": "2:30",
# 			"end_time": "4:30",
# 			"instructor": ["Estey, Anthony"],
# 			"ta": ["TA_1", "TA_2"],
# 			"building": "building_2", 
# 			"room": "room_2",
# 		}
# 	}
# )

# print(list(schedules[1].values())[0])
# /html/body/div[2]/div[4]/table[2]/tbody