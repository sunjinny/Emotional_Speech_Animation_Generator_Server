def calculatingRelation(minM, maxM):
	if minM == 0 and maxM == 0:
		return 0, 0.9 # x = 0, y = 0.9
	elif (minM - maxM) == 0:
		x = 0
	else:
		x = -0.1 / (minM - maxM)
	y = 1 - (maxM * x)
	return x, y

def calculatingSpeechCoefficient(x, y, m):
	return (m * x) + y


def blendingEmotionAndSpeech(orderedBSWeight, bsName, emotionAnimation, speechAnimation, time, speechCoeffAnimation):
	if emotionAnimation.BSPart[bsName] == 'eye':
		if bsName in emotionAnimation.attrList:
			orderedBSWeight = orderedBSWeight + str(emotionAnimation.getValueFromTimeInAttribute(bsName, time)) + " "
		else:
			orderedBSWeight = orderedBSWeight + "0.0 "
	# elif emotionAnimation.BSPart[bsName] == 'lips':
	# 	if bsName in emotionAnimation.attrList:
	# 		orderedBSWeight = orderedBSWeight + str(emotionAnimation.getValueFromTimeInAttribute(bsName, time)) + " "
	# 	else:
	# 		orderedBSWeight = orderedBSWeight + "0.0 "
	else:
		# Only Speech
		# if bsName in speechAnimation.attrList:
		# 	orderedBSWeight = orderedBSWeight + str(speechAnimation.getValueFromTimeInAttribute(bsName, time)) + " "
		# else:
		# 	orderedBSWeight = orderedBSWeight + "0.0 "

		# Using coefficient
		currentBSWeight = 0
		# if bsName == "MBP" or bsName == "M":
		# 	if bsName in speechAnimation.attrList:
		# 		orderedBSWeight = orderedBSWeight + str(speechAnimation.getValueFromTimeInAttribute(bsName, time)) + " "
		# 	else:
		# 		orderedBSWeight = orderedBSWeight + "0.0 "
		if bsName in emotionAnimation.attrList:
			currentBSWeight = currentBSWeight + emotionAnimation.getValueFromTimeInAttribute(bsName, time) * (1 - speechCoeffAnimation)
		else:
			currentBSWeight = 0.0
		if bsName in speechAnimation.attrList:
			currentBSWeight = currentBSWeight + speechAnimation.getValueFromTimeInAttribute(bsName, time) * speechCoeffAnimation
		else:
			currentBSWeight = currentBSWeight + 0.0
		orderedBSWeight = orderedBSWeight + str(currentBSWeight) + " "

	return orderedBSWeight