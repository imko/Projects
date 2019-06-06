from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from bs4 import element 
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen 
import re 
import collections

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

def enter_seat_summary(course, seats, has_seat_summary): 
	"""Enter seat summary of the given course"""
	if has_seat_summary:
		course.set_seat_summary(seats[0], seats[1], seats[2], seats[3])
	else:
		course.set_seat_summary(None, None, None, None)

def init_course(page, link):
	"""Initialize Course with section_id, activity, course_name, and link to the course"""
	pivot = -1 if len(str(page.select("body > div.container > div.content.expand > h4")[0].text).split()) < 5 else -2 
	section_id = " ".join(str(page.select("body > div.container > div.content.expand > h4")[0].text).split()[:pivot])
	activity = " ".join(str(page.select("body > div.container > div.content.expand > h4")[0].text).split()[pivot:])[1:-1]
	course_name = page.select("body > div.container > div.content.expand > h5")[0].text

	return Course(link, section_id, activity, course_name)

def get_instructors(driver, has_detail_table): 
	"""Find instructors and return in a tuple"""
	if has_detail_table:
		instructor_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[3]") 
	else:
		instructor_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[2]")

	instructors = re.split(":|\n", str(instructor_table.text))

	index_instructor = None 
	try: 
		index_instructor = instructors.index("Instructor") 
		index_ta = instructors.index("TA")
		instructor_list = [s.strip() for s in instructors[index_instructor+1:index_ta]]
		ta_list = [s.strip() for s in instructors[index_ta+1:]]
	except:
		instructor_list = [s.strip() for s in instructors[index_instructor+1:]] if index_instructor else None  
		ta_list = None 

	return (instructor_list, ta_list)

# main 
base_url = "https://courses.students.ubc.ca"
url = "https://courses.students.ubc.ca/cs/courseschedule?tname=subj-all-departments&sessyr=2019&sesscd=S&pname=subjarea"
# TODO: fix when single subject works 
# url = "https://courses.students.ubc.ca/cs/courseschedule?sesscd=S&tname=subj-department&sessyr=2019&dept=CPSC&pname=subjarea"
driver = webdriver.Chrome() 
driver.get(url)

subject_links = {}
subject_table = driver.find_element_by_xpath("//*[@id=\"mainTable\"]/tbody")
for subject in subject_table.find_elements_by_xpath("./tr/td/a[@href]"): 
	subject_links[subject.text.split()[0]] = subject.get_attribute("href")

ordered_subject_links = collections.OrderedDict(sorted(subject_links.items()))
subject_dict = {} 
for subject, subject_link in ordered_subject_links.items(): 
	driver.get(subject_link)
	page = soup(driver.page_source, "html.parser") 

	# fetch all the links to the courses 
	course_links = {}
	courses_table = driver.find_element_by_xpath("//*[@id=\"mainTable\"]/tbody")
	for course in courses_table.find_elements_by_xpath("./tr/td/a[@href]"): 
		course_links[course.text] = course.get_attribute("href") 

	ordered_course_links = collections.OrderedDict(sorted(course_links.items())) 
	# click every course link in the list 
	for course, course_link in ordered_course_links.items(): 
		driver.get(course_link) 
		page = soup(driver.page_source, "html.parser") 

		# fetch all the links to the sections 
		section_links = {} 
		section_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[2]/tbody") 
		for section in section_table.find_elements_by_xpath("./tr/td/a[@href]"): 
			section_links[section.text] = section.get_attribute("href") 

		ordered_section_links = collections.OrderedDict(sorted(section_links.items())) 
		# click every section link in the list 
		sections = [] 
		for section, section_link in ordered_section_links.items(): 
			driver.get(section_link) 
			page = soup(driver.page_source, "html.parser") 

			course = init_course(page, section_link) 

			# fetch the table with course detail 
			detail_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[2]/tbody") 

			# make a list of list of needed info 
			details = [] 
			for tr in detail_table.find_elements_by_xpath("./tr"): 
				info = [] 
				for td in tr.find_elements_by_xpath("./td"): 
					info.append(td.text) 
				if len(info) == 6: 
					details.append(info) 
				else: 
					break
			has_detail_table = False if len(details) <= 0 else True 
			
			# check if the course does NOT have detail table 
			seats = [] 
			try: 
				if has_detail_table: 
					summary_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[4]/tbody") 
				else: 
					details = [[None, None, None, None, None, None]] 
					summary_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[3]/tbody") 

				has_seat_summary = True 
				for tr in summary_table.find_elements_by_xpath("./tr"): 
					for td, k in enumerate(tr.find_elements_by_xpath("./td")): 
						if td == 1: 
							seats.append(k.text) 
				if len(seats) < 4: 
					has_seat_summary = False 
			except: 
				continue 

			enter_details(course, get_instructors(driver, has_detail_table), details) 
			enter_seat_summary(course, seats, has_seat_summary) 

			# add course to the list of course sections 
			sections.append(course) 

			# TESTING 
			print(str(section) + str(course.schedules) + " --> Successful") 

			# go back to previous page (ie. page of list of sections) 
			driver.back() 

	driver.back() 

driver.quit() 
