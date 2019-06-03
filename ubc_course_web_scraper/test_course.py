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
		self.course = Course("LINK")

	def tearDown(self):
		pass 

	def test_set_details(self):
		term = "1"
		days = ["Mon", "Tue", "Fri"]
		start_time = "17:30"
		end_time = "19:30"
		instructor = "instructor_1"
		building = "building_1"
		room = "1000"
		self.course.set_details(term, days, start_time, end_time, instructor, building, room)
		self.assertEqual(self.course.term, term)
		self.assertEqual(self.course.days, days)
		self.assertEqual(self.course.start_time, start_time)
		self.assertEqual(self.course.end_time, end_time)
		self.assertEqual(self.course.instructor, instructor)
		self.assertEqual(self.course.building, building)
		self.assertEqual(self.course.room, room)
		self.assertEqual(self.course.display_details(), "section: " + self.course.section + "\nactivity: " + self.course.activity + "\nterm: " + term + "\ndays: " + str(days) + "\nstart time: " + start_time + "\nend time: " + end_time + "\ninstructor: " + instructor + "\nbuilding: " + building + "\nroom: " + room)

	def test_set_seat_summary(self):
		total_seats_remaining = "200"
		currently_registered = "15"
		general_seats_remaining = "200"
		restricted_seats_remaining = "0"
		self.course.set_seat_summary(total_seats_remaining, currently_registered, general_seats_remaining, restricted_seats_remaining)
		self.assertEqual(self.course.total_seats_remaining, total_seats_remaining)
		self.assertEqual(self.course.currently_registered, currently_registered)
		self.assertEqual(self.course.general_seats_remaining, general_seats_remaining)
		self.assertEqual(self.course.restricted_seats_remaining, restricted_seats_remaining)
		self.assertEqual(self.course.display_seat_summary(), "total seats remaining: " + total_seats_remaining + "\ncurrently registered: " + currently_registered + "\ngeneral seats remaining: " + general_seats_remaining + "\nrestricted seats remaining: " + restricted_seats_remaining)

	# def test_mock_mock(self): 
	# 	with patch("employee.requests.get") as mocked_get: 
	# 		mocked_get.return_value.ok = True 
	# 		mocked_get.return_value.text = "Success" 

	# 		schedule = self.emp1.monthly_schedule("may") 
	# 		mocked_get.assert_called_with("http://company.com/Shafer/may") 
	# 		self.assertEqual(schedule, "Success") 

	# def test_mock_mock(self): 
	# 	with patch("employee.requests.get") as mocked_get: 
	# 		mocked_get.return_value.ok = False

	# 		schedule = self.emp1.monthly_schedule("may") 
	# 		mocked_get.assert_called_with("http://company.com/Shafer/may") 
	# 		self.assertEqual(schedule, "Bad Response!") 

# python -m uniitest test_course.py
if __name__ == "__main__":
	unittest.main() 
