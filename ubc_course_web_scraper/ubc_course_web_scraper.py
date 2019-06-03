from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from bs4 import element 
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen 

from course import Course 

def enter_details(course, instructor, columns):
	"""Enter details of the given course"""
	term = str(columns[0].string).strip()
	day = str(columns[1].string).strip().split()
	start_time = str(columns[2].string).strip()
	end_time = str(columns[3].string).strip()
	building = str(columns[4].string).strip()
	room = str(columns[5].string).strip()

	course.set_details(term, day, start_time, end_time, instructor, building, room)

def enter_seat_summary(course, seats): 
	"""Enter seat summary of the given course"""
	total_seats_remaining = str(seats[0].text).split(":")[-1]
	currently_registered = str(seats[1].text).split(":")[-1]
	general_seats_remaining = str(seats[2].text).split(":")[-1]
	restricted_seats_remaining = str(seats[3].text).split(":")[-1]
	
	course.set_seat_summary(total_seats_remaining, currently_registered, general_seats_remaining, restricted_seats_remaining)

def init_course(page, link):
	"""Initialize Course with section_id, activity, course_name, and link to the course"""
	pivot = -1 if len(str(page.select("body > div.container > div.content.expand > h4")[0].text).split()) < 5 else -2 
	section_id = " ".join(str(page.select("body > div.container > div.content.expand > h4")[0].text).split()[:pivot])
	activity = " ".join(str(page.select("body > div.container > div.content.expand > h4")[0].text).split()[pivot:])[1:-1]
	course_name = page.select("body > div.container > div.content.expand > h5")[0].text

	return Course(link, section_id, activity, course_name)

# main 
base_url = "https://courses.students.ubc.ca"

# todo: testing url 
url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-department&dept=CPSC"
driver = webdriver.Chrome() 
driver.get(url)

page = soup(driver.page_source, "html.parser") 
courses_table = page.find("tbody") # fetch courses of specific subject 

# todo: for testing 
# print(driver.current_url)
# driver.find_element_by_link_text("CPSC 103").click() 
# print(driver.current_url)

subject_dict = {} 

# testing: update with iteration once done with a single course 
course = courses_table.contents[1]
if isinstance(course, element.Tag):
	course_link = base_url + course.find("a")["href"] 
	course_id = course.find("a").text 

	# click on every course to view all course sections 
	driver.find_element_by_link_text(course_id).click() 
	page = soup(driver.page_source, "html.parser")
	sections_table = page.find("tbody") # fetch all sections of specific course 

	sections = [] 

	for section in sections_table:
	# testing: first section of the course; update with iteration once done with a single section 
	# section = sections_table.contents[0]
		if isinstance(section, element.Tag): 
			section_id = section.find("a").text
			link = base_url + section.find("a")["href"]

			# click on every section to view the detail 
			driver.find_element_by_link_text(section_id).click() 
			page = soup(driver.page_source, "html.parser")

			course = init_course(page, link)
			# fetch the table with course detail 
			for detail in page.find_all("table", {"class": "table table-striped"}):
				# fetch instructor table 
				instructor = str(page.select("body > div.container > div.content.expand > table:nth-child(18) > tbody > tr")[0].text).split(":")[-1].strip()
				# fetch all columns from the table
				columns = detail.find("tbody").find("tr").contents
				enter_details(course, instructor, columns) 

			# fetch the table with seating summary 
			for summary in page.find_all("table", {"class": "'table"}): 
				seats = summary.find("tbody").find_all("tr")
				enter_seat_summary(course, seats)

			# add course to the list of course sections 
			sections.append(course) 

			# go back to previous page (ie. page of list of sections)
			driver.back() 

# add list of course sections to the course dictionary 
subject_dict["CPSC"] = sections 

for section in sections: 
	print(str(section) + "\n")

driver.quit() 
