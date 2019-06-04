class Course(): 
	"""Course class that contains all important information"""

	def __init__(self, link, section_id, activity, course_name): 
		"""Initialize course link"""
		self.link = link
		self.section_id = section_id 
		self.activity = activity
		self.course_name = course_name

	def set_details(self, term, days, start_time, end_time, instructors, building, room): 
		"""Update and set course details"""
		self.term = term
		self.days = days 
		self.start_time = start_time 
		self.end_time = end_time 
		self.instructors = instructors[0] 
		self.tas = instructors[1]
		self.building = building
		self.room = room 

	def set_seat_summary(self, total_seats_remaining, currently_registered, general_seats_remaining, restricted_seats_remaining):
		"""Update and set seat summary of the course"""
		self.total_seats_remaining = total_seats_remaining 
		self.currently_registered = currently_registered 
		self.general_seats_remaining = general_seats_remaining 
		self.restricted_seats_remaining = restricted_seats_remaining  

	def display_details(self): 
		"""Return string representation of the course details"""
		return "link: " + self.link + "\nsection id: " + self.section_id + "\nactivity: " + self.activity + "\ncourse name: " + self.course_name + "\nterm: " + str(self.term) + "\ndays: " + str(self.days) + "\nstart time: " + str(self.start_time) + "\nend time: " + str(self.end_time) + "\ninstructor: " + str(self.instructors) + "\nta: " + str(self.tas) + "\nbuilding: " + str(self.building) + "\nroom: " + str(self.room) 

	def display_seat_summary(self): 
		"""Return string representation of the course seat summary"""
		return "total seats remaining: " + self.total_seats_remaining + "\ncurrently registered: " + self.currently_registered + "\ngeneral seats remaining: " + self.general_seats_remaining + "\nrestricted seats remaining: " + self.restricted_seats_remaining 

	def __str__(self): 
		"""Return string representation of the course details AND seat summary"""
		return self.display_details() + "\n" + self.display_seat_summary() 
