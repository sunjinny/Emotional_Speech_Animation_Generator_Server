import math

class EmotionAnimator:
	def __init__(self, animationGenerator):
		# type: (model_manipulator.MayaModelManipulator) -> None

		self.animationGenerator = animationGenerator

	def makeEmotion(self, startTime, emotionAnimations, weights, endTime):
		# type: (float, tuple, tuple) -> None

		def combineSequences(weights):
			weights = [math.log(weight + 1.0, 2) for weight in weights]
			weightSum = sum(weights)
			# weightSum = sum([1.0 if weight > 0.0 else 0.0 for weight in weights])

			resultingSequence = {}
			for emotionAnimation, weight in zip(emotionAnimations, weights):
				sourceFps = emotionAnimation['fps']
				sourceSequence = emotionAnimation['keys']

				weightRatio = weight / weightSum if weightSum != 0.0 else 0.0
				for frame, animationKey in sourceSequence.items():
					if frame not in resultingSequence:
						resultingSequence[frame] = {}

					for name, value in animationKey.items():
						if name not in resultingSequence[frame]:
							resultingSequence[frame][name] = 0.0

						resultingSequence[frame][name] += value * weight * weightRatio

			return resultingSequence

		fps = emotionAnimations[0]['fps']
		combinedSequence = combineSequences(weights)

		seqTime = 0

		for frame, animationKey in combinedSequence.items():
			time = startTime + frame / float(fps)
			time = time * 1000

			keyValueDict = animationKey  # type: dict
			self.animationGenerator.addValueMapInAttributeMap(keyValueDict, time)

			if seqTime < time:
				seqTime = time

		while endTime > seqTime :
			restartTime = seqTime
			for frame, animationKey in combinedSequence.items():
				time = restartTime + frame / float(fps)
				time = time * 1000
				keyValueDict = animationKey  # type: dict
				self.animationGenerator.addValueMapInAttributeMap(keyValueDict, time)
				if seqTime < time:
					seqTime = time
