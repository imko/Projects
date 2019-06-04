from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from bs4 import element 
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen 
import re 

from course import Course 

def enter_details(course, instructors, columns):
	"""Enter details of the given course"""
	term = str(columns[0].string).strip() if str(columns[0].string).strip() else None 
	day = str(columns[1].string).strip().split() if len(str(columns[1].string).strip().split()) > 0 else None 
	start_time = str(columns[2].string).strip() if str(columns[2].string).strip() else None
	end_time = str(columns[3].string).strip() if str(columns[3].string).strip() else None
	building = str(columns[4].string).strip() if str(columns[4].string).strip() else None 
	room = str(columns[5].string).strip() if str(columns[5].string).strip() else None 

	course.set_details(term, day, start_time, end_time, instructors, building, room)

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

# todo: testing url 
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
				# TODO: fix cases when there's 2 different links to the same course AND work placements 
				try: 
					link = base_url + section.find("a")["href"]

					# click on every section to view the detail 
					driver.find_element_by_link_text(section.find("a").text).click() 
					page = soup(driver.page_source, "html.parser")

					course = init_course(page, link)

					# fetch the table with course detail 
					for detail in page.find_all("table", {"class": "table table-striped"}):
						instructors = get_instructors(driver)

						# fetch all columns from the table
						columns = detail.find("tbody").find("tr").contents
						
						enter_details(course, instructors, columns) 

						# fetch the table with seating summary 
						for summary in page.find_all("table", {"class": "'table"}): 
							seats = summary.find("tbody").find_all("tr")
							enter_seat_summary(course, seats)

					# add course to the list of course sections 
					sections.append(course) 

					# TESTING 
					print(str(link) + " --> Successful")
					print(str(course) + "\n")

					# go back to previous page (ie. page of list of sections)
					driver.back() 
				except: 
					continue 

		# add list of course sections to the course dictionary 
		subject_dict["CPSC"] = sections 

		# go back to previous page (ie. page of list of courses)
		driver.back()

driver.quit() 
