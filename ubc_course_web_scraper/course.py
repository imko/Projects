class Course(): 
	"""Course class that contains all important information"""

	def __init__(self, link, section, activity, course_name, course_grades_link): 
		"""Initialize course link"""
		self.schedules = []
		self.instructors = [] 
		self.link = link
		self.course_grades_link = course_grades_link 
		self.section = section 
		self.activity = activity
		self.course_name = course_name

	def set_schedule(self, term, days, start_time, end_time, instructors, building, room): 
		"""Update and set course details"""
		self.term = term
		self.schedules.append(
			{
				days:
				{
					"start_time": start_time,
					"end_time": end_time,
					"instructor": instructors[0],
					"ta": instructors[1],
					"building": building, 
					"room": room,
				}
			}
		)

	def set_seat_summary(self, total_seats_remaining, currently_registered, general_seats_remaining, restricted_seats_remaining):
		"""Update and set seat summary of the course"""
		self.seat_summary = {
			"total_seats_remaining": total_seats_remaining,
			"currently_registered": currently_registered, 
			"general_seats_remaining": general_seats_remaining, 
			"restricted_seats_remaining": restricted_seats_remaining,
		}

	def display_schedule(self): 
		"""Return string representation of the course days with start time and end time"""
		msg = ""
		for schedule in self.schedules: 
			for day, info in schedule.items(): 
				msg += str(day) + " --> " + str(info) + "\n"

		return msg 
		
	def display_details(self): 
		"""Return string representation of the course details"""
		return "LINK: " + self.link + "\nGRADES LINK: " + self.course_grades_link + "\nSECTION: " + self.section + "\nACTIVITY: " + self.activity + "\nCOURSE NAME: " + self.course_name + "\nTERM: " + str(self.term) + "\n" + self.display_schedule() 

	def display_seat_summary(self): 
		"""Return string representation of the course seat summary"""
		msg = "" 
		for title, value in self.seat_summary.items(): 
			msg += str(title) + ": " + str(value) + "\n"

		return msg 

	def __str__(self): 
		"""Return string representation of the course details AND seat summary"""
		return self.display_details() + self.display_seat_summary() 
