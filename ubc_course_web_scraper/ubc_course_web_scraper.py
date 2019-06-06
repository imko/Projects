from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from bs4 import element 
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen 
import re 

# testing 
import traceback 

from course import Course 

def enter_details(course, instructors, details):
	"""Enter details of the given course"""
	for info in details: 
		term = str(info[0]).strip() if str(info[0]).strip() else None 
		days = str(info[1]).strip() if str(info[1]).strip() else None 
		start_time = str(info[2]).strip() if str(info[2]).strip() else None
		end_time = str(info[3]).strip() if str(info[3]).strip() else None
		building = str(info[4]).strip() if str(info[4]).strip() else None 
		room = str(info[5]).strip() if str(info[5]).strip() else None 

		course.set_schedule(term, days, start_time, end_time, instructors, building, room)

def enter_seat_summary(course, seats): 
	"""Enter seat summary of the given course"""
	course.set_seat_summary(seats[0], seats[1], seats[2], seats[3])

def init_course(page, link):
	"""Initialize Course with section_id, activity, course_name, and link to the course"""
	pivot = -1 if len(str(page.select("body > div.container > div.content.expand > h4")[0].text).split()) < 5 else -2 
	section_id = " ".join(str(page.select("body > div.container > div.content.expand > h4")[0].text).split()[:pivot])
	activity = " ".join(str(page.select("body > div.container > div.content.expand > h4")[0].text).split()[pivot:])[1:-1]
	course_name = page.select("body > div.container > div.content.expand > h5")[0].text

	return Course(link, section_id, activity, course_name)

def get_instructors(driver): 
	"""Find instructors and return in a tuple"""
	instructor_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[3]")
	instructors = re.split(":|\n", str(instructor_table.text))
	try: 
		index_instructor = instructors.index("Instructor")
		index_ta = instructors.index("TA")
		instructor_list = [s.strip() for s in instructors[index_instructor+1:index_ta]]
		ta_list = [s.strip() for s in instructors[index_ta+1:]]
	except:
		instructor_list = [s.strip() for s in instructors[index_instructor+1:]]
		ta_list = None 
	
	return (instructor_list, ta_list)

# main 
base_url = "https://courses.students.ubc.ca"

# TODO: fix when single subject works 
url = "https://courses.students.ubc.ca/cs/courseschedule?sesscd=S&tname=subj-department&sessyr=2019&dept=CPSC&pname=subjarea"
driver = webdriver.Chrome() 
driver.get(url)

page = soup(driver.page_source, "html.parser") 
courses_table = page.find("tbody") # fetch courses of specific subject 

# TODO: fix cases when there's 2 different links to the same course AND work placements 
subject_dict = {} 
for course in courses_table.contents:
	if isinstance(course, element.Tag):
		course_link = base_url + course.find("a")["href"] 
		course_id = course.find("a").text 
		# click on every course to view all course sections 
		driver.find_element_by_link_text(course_id).click() 
		page = soup(driver.page_source, "html.parser")
		sections_table = page.find("tbody") # fetch all sections of specific course 

		sections = [] 
		for section in sections_table:
			# check if current section is an HTML element tag 
			if isinstance(section, element.Tag): 
				try: 
					link = base_url + section.find("a")["href"]

					# click on every section to view the detail 
					driver.find_element_by_link_text(section.find("a").text).click() 
					page = soup(driver.page_source, "html.parser")

					course = init_course(page, link)

					# fetch the table with course detail 
					detail_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[2]/tbody")
					# make a list of list of needed info 
					details = [] 
					for tr in detail_table.find_elements_by_xpath("./tr"):
						info = []
						for td in tr.find_elements_by_xpath("./td"):
							info.append(td.text) 
						details.append(info)

					enter_details(course, get_instructors(driver), details)

					# for detail in page.find_all("table", {"class": "table table-striped"}):
					# 	instructors = get_instructors(driver)

					# 	# fetch all details from the table
					# 	details = detail.find("tbody").find("tr").contents
						
					# 	enter_details(course, instructors, details) 

					# 	# fetch the table with seating summary 
					summary_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[4]/tbody") 
					seats = [] 
					for tr in summary_table.find_elements_by_xpath("./tr"): 
						for td, k in enumerate(tr.find_elements_by_xpath("./td")): 
							if td == 1:
								seats.append(k.text) 
					enter_seat_summary(course, seats) 

					# 	for summary in page.find_all("table", {"class": "'table"}): 
					# 		seats = summary.find("tbody").find_all("tr")
					# 		enter_seat_summary(course, seats)

					# add course to the list of course sections 
					sections.append(course) 

					# TESTING 
					print(str(link) + " --> Successful")
					print(str(course) + "\n")

					# go back to previous page (ie. page of list of sections)
					driver.back() 
				except: 
					# print(traceback.format_exc()) # testing for course with more than one row 
					continue 

		# TODO: fix 'key' when single subject works
		# add list of course sections to the course dictionary 
		subject_dict["CPSC"] = sections 

		# go back to previous page (ie. page of list of courses)
		driver.back()

driver.quit() 
