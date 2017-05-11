import sys
class FunctionalUnit(object):
	"""The class that represent functional unit of the simulator

	"""
	def __init__(self, name,count,cycle):
		self.count = count
		self.name = name
		self.cycle = cycle
		self.used = 0
		self.usageLog = []
	def occupy(self):
		if self.used < self.count:
			self.used+=1
			return True
		else:
			return False
	def free(self):
		if used > 0:
			used-=1
	def isHazard(self,requestTime):
		# get the number of record from log that has the start and end time within
		number,minValue = self.currentUsageNumber(requestTime)
		result= number == self.count # it should not be greater
		return result,minValue

	def currentUsageNumber(self,requestTime):
		count = 0
		minvalue=sys.maxint
		for item in self.usageLog:
			if item > requestTime:
				count+=1
				if item < minvalue:
					minvalue=item

		return count,minvalue

	def log(self,start ,end):
		usageLog.append(completionTime)