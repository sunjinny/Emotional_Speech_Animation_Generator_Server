import operator
import math

class TimeSeries:
	def __init__(self, records):
		self.records = sorted(records, key = operator.itemgetter(0))
		self.sampleCache = {}

	def sample(self, time):
		if time in self.sampleCache:
			return self.sampleCache[time]

		currentRecord = None
		previousRecord = self.records[0]
		for currentRecord in self.records:
			if currentRecord[0] >= time:
				break
			previousRecord = currentRecord

		if currentRecord is previousRecord:
			# if this is true, it must be the first or last
			# do not interpolate if the record is the first or last
			sampleValue = currentRecord[1]
		else:
			# interpolate two adjacent samples in linear manner
			ratio = (time - previousRecord[0]) / (currentRecord[0] - previousRecord[0])
			sampleValue = ratio * currentRecord[1] + (1.0 - ratio) * previousRecord[1]

		self.sampleCache[time] = sampleValue
		return sampleValue

	def __getitem__(self, item):
		return self.records[item]

	def mean(self, selector = lambda time, value: True):
		count = 0
		summation = 0

		for record in self.records:
			time, value = record
			if selector(time, value):
				summation += value
				count += 1

		return (summation / count) if count > 0 else 0

	def map(self, operation):
		resultRecords = []
		for record in self.records:
			time, value = record
			resultRecord = operation(time, value)
			if resultRecord:
				resultRecords.append(resultRecord)

		return TimeSeries(resultRecords)

	def log(self):
		return self.map(lambda time, value: (time, math.log(1 + value)))

	def multiply(self, scale):
		return self.map(lambda time, value: (time, scale * value))

	def meanToZero(self):
		mean = self.mean()
		return self.map(lambda time, value: (time, value - mean))

	def movingAverage(self, stepInterval, windowTimeSpan, windowAlignment ='center'):
		def windowedAverage(time):
			windowSize = int(windowTimeSpan / stepInterval + 0.5)
			if windowSize <= 0:
				return 0

			if windowAlignment == 'center':
				windowLeftSpan = windowSize // 2
				windowRightSpan = windowSize - windowLeftSpan
			elif windowAlignment == 'right':
				windowLeftSpan = windowSize - 1
				windowRightSpan = 1
			elif windowAlignment == 'left':
				windowLeftSpan = 0
				windowRightSpan = windowSize
			else:
				raise ValueError("Bad window_align value")

			summation = 0
			for stepIndex in range(-windowLeftSpan, windowRightSpan):
				sampleTime = time + stepIndex * stepInterval
				summation += self.sample(sampleTime)

			return summation / windowSize

		startingTime = self.records[0][0]
		timeRange = self.records[-1][0] - startingTime
		lastStep = int(timeRange / stepInterval + 0.5)

		resultRecords = []
		for stepIndex in range(0, lastStep + 1):
			time = startingTime + stepIndex * stepInterval
			resultRecords.append((time, windowedAverage(time)))

		return TimeSeries(resultRecords)

	def resample(self, stepInterval):
		startingTime = self.records[0][0]
		timeRange = self.records[-1][0] - startingTime
		last_step = int(timeRange / stepInterval + 0.5)

		resultRecords = []
		for stepIndex in range(0, last_step + 1):
			sampleTime = startingTime + stepIndex * stepInterval
			resultRecords.append((sampleTime, self.sample(sampleTime)))

		return TimeSeries(resultRecords)