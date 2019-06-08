import sqlite3 

from course import Course 

class UBCDatabase():
	"""A class that is responsible for storing information in UBC course database"""

	def __init__(self):
		"""Initialize UBC Database"""
		self.conn = sqlite3.connect("ubc_course.db")  
		self.c = self.conn.cursor() 

	def create_table(self): 
		"""Create UBC course table"""
		self.c.execute("CREATE TABLE IF NOT EXISTS ubcCourseTable (term BLOB, course_name TEXT, course_number INTEGER, course_section TEXT, activity TEXT, days TEXT, start_time BLOB, end_time BLOB, instructor BLOB, building BLOB, room_number BLOB)") 

	def data_entry(self, course_name, course_number, course): 
		"""Store course info in the table"""
		for schedule in course.schedules: 
			for day, info in schedule.items(): 
				for instructor in info["instructor"]:
					self.c.execute("INSERT INTO ubcCourseTable(term, course_name, course_number, course_section, activity, days, start_time, end_time, instructor, building, room_number) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (course.term, course_name, course_number, course.section, course.activity, day, info["start_time"], info["end_time"], instructor, info["building"], info["room"]))
					self.conn.commit() 

	def reset(self): 
		"""Delete whole table"""
		self.c.execute("DROP TABLE ubcCourseTable")