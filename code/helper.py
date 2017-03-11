import time
import calendar

class Helper():
	"""
		Class that has functions used for computations in other classes
	"""
	# def __init__(self, arg):
	# 	self.day    = time.strftime("%d")
	# 	self.month  = time.strftime("%m")
	# 	self.year   = time.strftime("%Y")
	# 	self.hour   = time.strftime("%H")
	# 	self.minute = time.strftime("%M")
		
	def isEndOfMonth(self, month, day):
		""" 
			Function that determines if its the last day of the month

			Returns: 
				bool: True if its end of the month, False otherwise.
		"""

		return ((month == 1 and day == 31) or (month == 2 and day == 28)  or
				(month == 3 and day == 31) or (month == 4 and day == 30)  or
				(month == 5 and day == 31) or (month == 6 and day == 30)  or
				(month == 7 and day == 31) or (month == 8 and day == 31)  or
				(month == 9 and day == 30) or (month == 10 and day == 31) or
				(month == 11 and day == 30) or (month == 12 and day == 31))

	def getDay(self):
		""" Returns the current day """
		return time.strftime("%d")

	def getMonth(self):
		""" Returns the current month """
		return time.strftime("%m")

	def getYear(self):
		""" Returns the current year """
		return time.strftime("%Y")

	def getHour(self):
		""" Returns the current hour """
		return time.strftime("%H")

	def getYesterday(self):
		""" 
			Returns yesterday in an array.
			[year,month,day]
		"""
		yesterday = []
		current_day = int(self.getDay())-1
		current_year = int(self.getYear())
		current_month = self.getMonth()
		if current_day == 0:
			current_month = int(self.getMonth()) -1
			if (current_month == 1 or current_month == 3 or
				current_month == 5 or current_month == 7 or
				current_month == 8 or current_month == 10 or
				current_month == 12 or current_month == 12):
				current_day	= 31
			elif (current_month == 2):
				current_day = 28
			else:
				current_day = 30
			if current_month == 0:
				current_month = 31
				current_year = int(self.getYear()) - 1
			# yesterday = str(current_year)+str(current_month)
		if len(str(current_day)) == 1:
			current_day = "0" + str(current_day)
		yesterday.append(str(current_year))
		yesterday.append(str(current_month))
		yesterday.append(str(current_day))

		return yesterday

	def getDateInEpoch(self, timestamp):
		return calendar.timegm(time.strptime(timestamp,'%m/%d/%Y %H:%M'))