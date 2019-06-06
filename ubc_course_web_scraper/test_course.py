import unittest 
from unittest.mock import patch 
from course import Course 

class TestCourse(unittest.TestCase): 
	"""A test suite for Course class"""

	@classmethod
	def setUpClass(cls):
		pass

	@classmethod
	def tearDownClass(cls):
		pass

	def setUp(self):
		self.course = Course("LINK", "CPSC 110 100", "Lecture", "Computational Thinking")

	def tearDown(self):
		pass 

	def test_set_details(self):
		term = "1"
		days = ("Mon", "Tue", "Fri")
		start_time = "17:30"
		end_time = "19:30"
		instructor = [["instructor_1"], ["ta_1", "ta_2"]]
		building = "building_1"
		room = "1000"
		self.course.set_schedule(term, days, start_time, end_time, instructor, building, room)
		self.assertEqual(self.course.term, term)
		self.assertEqual(list(self.course.schedules[0].keys())[0], days)
		self.assertEqual(list(self.course.schedules[0].values())[0]["start_time"], start_time)
		self.assertEqual(list(self.course.schedules[0].values())[0]["end_time"], end_time)
		self.assertEqual(list(self.course.schedules[0].values())[0]["instructor"], instructor[0])
		self.assertEqual(list(self.course.schedules[0].values())[0]["ta"], instructor[1])
		self.assertEqual(list(self.course.schedules[0].values())[0]["building"], building)
		self.assertEqual(list(self.course.schedules[0].values())[0]["room"], room)

	def test_set_seat_summary(self):
		total_seats_remaining = "200"
		currently_registered = "15"
		general_seats_remaining = "200"
		restricted_seats_remaining = "0"
		self.course.set_seat_summary(total_seats_remaining, currently_registered, general_seats_remaining, restricted_seats_remaining)
		self.assertEqual(self.course.seat_summary["total_seats_remaining"], total_seats_remaining)
		self.assertEqual(self.course.seat_summary["currently_registered"], currently_registered)
		self.assertEqual(self.course.seat_summary["general_seats_remaining"], general_seats_remaining)
		self.assertEqual(self.course.seat_summary["restricted_seats_remaining"], restricted_seats_remaining)

# python -m uniitest test_course.py
if __name__ == "__main__":
	unittest.main() 
