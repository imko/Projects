from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from bs4 import element 
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen 
import re 
import collections
import xlwt 
from xlwt import Workbook 

from course import Course 
from ubc_course_database import UBCDatabase

def init_course(driver, page, section_link, course_grades_link) :
	"""Initialize Course with section_id, activity, course_name, and link to the course"""
	header = ""
	for t in driver.find_elements_by_xpath("/html/body/div[2]/div[4]/h4"): 
		header += t.text
	pivot = -1 if len(str(header).split()) < 5 else -2 
	section_id = " ".join(str(header).split()[:pivot])
	activity = " ".join(str(header).split()[pivot:])[1:-1]
	course_name = ""
	for t in driver.find_elements_by_xpath("/html/body/div[2]/div[4]/h5"):
		course_name += t.text 
	# pivot = -1 if len(str(page.select("body > div.container > div.content.expand > h4")[0].text).split()) < 5 else -2 
	# section_id = " ".join(str(page.select("body > div.container > div.content.expand > h4")[0].text).split()[:pivot])
	# activity = " ".join(str(page.select("body > div.container > div.content.expand > h4")[0].text).split()[pivot:])[1:-1]
	# course_name = page.select("body > div.container > div.content.expand > h5")[0].text

	return Course(section_link, section_id, activity, course_name, course_grades_link)

def init_workbook():
	"""Initialize workbook for saving data"""
	workbook = Workbook() 
	sheet = workbook.add_sheet("Sheet 1") 

	return workbook, sheet, 0 	

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
	# check for no instructor table 
	try: 
		if has_seat_summary:
			course.set_seat_summary(seats[0], seats[1], seats[2], seats[3])
		else:
			course.set_seat_summary(None, None, None, None)
	except: 
		course.set_seat_summary(None, None, None, None)

def get_instructors(driver, has_detail_table): 
	"""Find instructors and return in a tuple"""
	has_instructor_table = True 
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
		# TA is not found in the table 
		instructor_list = [s.strip() for s in instructors[index_instructor+1:]] if index_instructor is not None else None  
		ta_list = None 

	return (instructor_list, ta_list)

def write_excel_headers(row, sheet):
	"""Write headers of the information"""
	sheet.write(row, 0, "TERM")
	sheet.write(row, 1, "SECTION")
	sheet.write(row, 2, "COURSE NAME")
	sheet.write(row, 3, "ACTIVITY")
	sheet.write(row, 4, "DAYS")
	sheet.write(row, 5, "START TIME")
	sheet.write(row, 6, "END TIME")
	sheet.write(row, 7, "INSTRUCTOR")
	sheet.write(row, 8, "TA")
	sheet.write(row, 9, "LOCATION")
	sheet.write(row, 10, "COURSE GRADE LINK")
	sheet.write(row, 11, "TOTAL SEATS REMAINING")
	sheet.write(row, 12, "CURRENTLY REGISTERED")
	sheet.write(row, 13, "GENERAL SEATS REMAINING")
	sheet.write(row, 14, "RESTRICTED SEATS REMAINING")

	return row + 1 

def write_course_info(course, row, sheet): 
	"""Write course info with give row of the excel file"""
	sheet.write(row, 0, course.term)
	sheet.write(row, 1, course.section)
	sheet.write(row, 2, course.course_name)
	sheet.write(row, 3, course.activity)
	sheet.write(row, 10, course.course_grades_link)
	sheet.write(row, 11, course.seat_summary["total_seats_remaining"])
	sheet.write(row, 12, course.seat_summary["currently_registered"])
	sheet.write(row, 13, course.seat_summary["general_seats_remaining"])
	sheet.write(row, 14, course.seat_summary["restricted_seats_remaining"])
	
	# loop through schedule for possible multiple schedules 
	for i in range(len(course.schedules)):
		offset = tmp_offset = 1
		for day, info in course.schedules[i].items(): 
			sheet.write(row+offset-1, 4, str(day))
			sheet.write(row+offset-1, 5, str(info["start_time"]))
			sheet.write(row+offset-1, 6, str(info["end_time"]))
			if info["instructor"] is not None:
				for j in range(len(info["instructor"])):
					sheet.write(row+offset+j-1, 7, str(info["instructor"][j]))
				# check if offset needs to be updated 
				tmp_offset = len(info["instructor"]) if len(info["instructor"]) > offset else offset 
			else:
				sheet.write(row, 7, str(info["instructor"]))
			if info["ta"] is not None: 
				for j in range(len(info["ta"])):
					sheet.write(row+offset+j-1, 8, str(info["ta"][j])) 
				# check if offset needs to be updated 
				tmp_offset = len(info["ta"]) if len(info["ta"]) > tmp_offset else tmp_offset 
			else: 
				sheet.write(row, 8, str(info["ta"]))
			sheet.write(row+offset-1, 9, str(info["building"]) + ", " + str(info["room"]))
		# check if offset needs to be updated or not 
		if tmp_offset != offset:
			offset = tmp_offset
		row += offset 

	return row

def write_to_excel_sheet(course, row, sheet): 
	"""Write course info in excel file"""
	if row == 0: 
		row = write_excel_headers(row, sheet) 
	else: 
		row = write_course_info(course, row, sheet)

	return row

def fetch_section_links(driver):
	"""Fetch all section links"""
	section_links = {} 
	section_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[2]/tbody") 
	for section in section_table.find_elements_by_xpath("./tr/td/a[@href]"): 
		section_links[section.text] = section.get_attribute("href") 

	return section_links

def fetch_course_links(driver): 
	"""Fetch all course links"""
	course_links = {}
	courses_table = driver.find_element_by_xpath("//*[@id=\"mainTable\"]/tbody")
	for course in courses_table.find_elements_by_xpath("./tr/td/a[@href]"): 
		course_links[course.text] = course.get_attribute("href") 

	return course_links 

def fetch_subject_links(driver):
	"""Fetch all subject links"""
	subject_links = {}
	subject_table = driver.find_element_by_xpath("//*[@id=\"mainTable\"]/tbody")
	for subject in subject_table.find_elements_by_xpath("./tr/td/a[@href]"): 
		subject_links[subject.text.split()[0]] = subject.get_attribute("href")

	return subject_links 

def fetch_details(detail_table):
	"""Fetch a list of details and return true if the list exists, false otherwise"""
	details = [] 
	for tr in detail_table.find_elements_by_xpath("./tr"): 
		info = [] 
		for td in tr.find_elements_by_xpath("./td"): 
			info.append(td.text) 
		# check if it's valid detail table 
		if len(info) == 6: 
			details.append(info) 
		else: 
			break
	# no detail table if details list is empty 
	has_detail_table = False if len(details) <= 0 else True 

	return details, has_detail_table

def click_link(driver, subject_link): 
	"""Click on the link and return soup"""
	driver.get(subject_link) 
	return soup(driver.page_source, "html.parser") 

def update_course_detail(driver, course, details, has_detail_table): 
	"""Check and update course detail and return course"""
	seats = [] 
	instructors = (None, None)
	has_seat_summary = True 
	try: 
		if has_detail_table: 
			summary_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[4]/tbody") 
		else: 
			details = [[None, None, None, None, None, None]] 
			summary_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[3]/tbody") 

		for tr in summary_table.find_elements_by_xpath("./tr"): 
			for td, k in enumerate(tr.find_elements_by_xpath("./td")): 
				if td == 1: 
					seats.append(k.text) 
		if len(seats) < 4: 
			has_seat_summary = False 

		instructors = get_instructors(driver, has_detail_table) 
	except: 
		pass 

	enter_details(course, instructors, details) 
	enter_seat_summary(course, seats, has_seat_summary) 

	return course 

def run(slacknotes_url, url):
	# initialize database 
	db = UBCDatabase() 
	# db.reset()
	db.create_table() 

	# initialize workbook
	workbook, sheet, row = init_workbook() 

	# open the website 
	driver = webdriver.Chrome() 
	driver.get(url)

	# fetch every link of the subjects 
	subject_links = fetch_subject_links(driver)

	# click the subject link 
	subject_dict = {} 
	ordered_subject_links = collections.OrderedDict(sorted(subject_links.items()))
	for subject, subject_link in ordered_subject_links.items(): 
		# click on the link
		page = click_link(driver, subject_link)

		# fetch all the links to the courses 
		course_links = fetch_course_links(driver)

		# click every course link in the list 
		ordered_course_links = collections.OrderedDict(sorted(course_links.items())) 
		for c, course_link in ordered_course_links.items(): 
			# concatenate course name (ie. CPSC213)
			course_name_list = c.split()[:2]
			course_name_list[-1] = course_name_list[-1][:-1] if len(course_name_list[-1]) > 3 else course_name_list[-1] 
			course_name = course_name_list[0]
			course_number = course_name_list[1] 
			course_grades_link = str(slacknotes_url) + str(course_name_list[0] + course_name_list[1]) 

			# click on the link
			page = click_link(driver, course_link)

			# fetch all the links to the sections 
			section_links = fetch_section_links(driver)

			# click every section link in the list 
			sections = [] 
			ordered_section_links = collections.OrderedDict(sorted(section_links.items())) 
			for section, section_link in ordered_section_links.items(): 
				page = click_link(driver, section_link)

				course = init_course(driver, page, section_link, course_grades_link) 

				# fetch the table with course detail 
				detail_table = driver.find_element_by_xpath("/html/body/div[2]/div[4]/table[2]/tbody") 

				# fetch a list of details and check if detail table is present 
				details, has_detail_table = fetch_details(detail_table)
				
				# check if the course does NOT have detail table 
				# add course to the list of course sections 
				sections.append(update_course_detail(driver, course, details, has_detail_table))

				# write to excel sheet 
				# row = write_to_excel_sheet(course, row, sheet) 
				# store in database 
				db.data_entry(course_name, course_number, course)

				# TESTING 
				print(str(section) + " --> Successful") 

				# go back to previous page (ie. page of list of sections) 
				driver.back() 

		# save to excel file every subject 
		workbook.save("ubc_course_data.xls")
		driver.back() 

	db.close()
	driver.quit() 

# main 
slacknotes_url = "https://slacknotes.com/grades/"
url = "https://courses.students.ubc.ca/cs/courseschedule?tname=subj-all-departments&sessyr=2019&sesscd=S&pname=subjarea"

run(slacknotes_url, url) 
