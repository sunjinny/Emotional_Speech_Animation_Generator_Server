import numpy as np

# save in milliseconds
class Animation:
	#attrList = {}
	#orderedBSList = list()

	def __init__(self, blendshapeListPath):
		self.attrList = {}
		self.orderedBSList = list()
		self.BSPart = dict()
		data = open(blendshapeListPath)
		for bs in data.read().split():
			part = bs.split(',')
			self.BSPart[part[1]] = part[0]
			self.orderedBSList.append(part[1])

	def createAttribute(self, attributeName):
		if attributeName in self.attrList:
			print("Already exited attribute.")
			# print(self.attrList.keys())
		else:
			self.attrList[attributeName] = Attribute(attributeName)
			# print(self.attrList.keys())

	def addValueInAttribute(self, attributeName, time, value):
		if attributeName in self.attrList:
			self.attrList[attributeName].addPoint(time, value)
			# self.attrList[attributeName].printAllPoint()
		else:
			self.createAttribute(attributeName)
			self.attrList[attributeName].addPoint(time, value)
			# self.attrList[attributeName].printAllPoint()

	def addValueMapInAttributeMap(self, attributeValueMap, time):
		for attribute, vlaue in zip(attributeValueMap.keys(), attributeValueMap.values()):
			self.addValueInAttribute(attribute, time, vlaue)

	def deleteValueInAttribute(self, attributeName, time):
		if attributeName in self.attrList:
			self.attrList[attributeName].deletePoint(time)
			# self.attrList[attributeName].printAllPoint()
		else:
			print("Invalid. First create the attribute.")
			print(self.attrList)

	def getValueFromTimeInAttribute(self, attributeName, accessTime):
		if attributeName in self.attrList:
			return self.attrList[attributeName].getValue(accessTime)
		else:
			return 0




class Attribute:
	def __init__(self, name):
		self.name = name
		# self.dict = collections.OrderedDict()
		self.dict = {}

	def __isEmpty(self):
		return self.dict.__len__() is 0

	def __isClose(self, closeTime, inputTime, rel_tol=1e-09, abs_tol=0.0):
		return (abs(closeTime - inputTime) <= max(rel_tol * max(abs(closeTime), abs(inputTime)), abs_tol)), closeTime

	def __isIn(self, inputTime):
		if self.__isEmpty():
			return False, inputTime
		else:
			closeTime  = inputTime if inputTime in self.dict else min(self.dict.keys(), key=lambda k: abs(k - inputTime))
			return self.__isClose(closeTime, inputTime)

	def addPoint(self, time, value):
		check, closeTime = self.__isIn(time)
		if check:
			self.dict[closeTime] = value
		else:
			self.dict[time] = value

	def deletePoint(self, time):
		if self.__isEmpty():
			print("Cannot delete. Empty point attribute. Please first add the point.")
			return
		check, closeTime = self.__isIn(time)
		if check:
			del self.dict[closeTime]
		else:
			print("There is not the time in attribute.")
			print("The nearest point is ", closeTime)

	def getValue(self, accessTime):
		if self.__isEmpty():
			print("Empty point attribute. Please first add the point.")
			return 0
		check, closeTime = self.__isIn(accessTime)
		if check:
			return self.dict[closeTime]
		else:
			sortedKeys = sorted(self.dict)
			sortedValuesByKey = []
			for key in sortedKeys:
				sortedValuesByKey.append(self.dict[key])
			return np.interp(accessTime, sortedKeys, sortedValuesByKey)

	def printAllPoint(self):
		print(self.name + " : ")
		print(self.dict)
