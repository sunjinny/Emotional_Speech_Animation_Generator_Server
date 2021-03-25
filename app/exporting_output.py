from xml.etree.ElementTree import Element, SubElement, dump, ElementTree
import blending
from animation import Animation

def generateOutputFileInSpeechAndEmotion(speechAnimation, emotionAnimation, audioSize, fps, inputGender, inputHair, minM, maxM, pitchInfo, emotionStrengths):
	relationOfM_x, relationOfM_y = blending.calculatingRelation(minM, maxM)
	animation = Element("animation")
	animation.attrib["name"] = "speech_emotion_animation"
	gender = Element("gender")
	gender.attrib["gender"] = inputGender
	animation.append(gender)
	hairModel = Element("hair_model")
	hairModel.attrib["hair_model"] = inputHair
	animation.append(hairModel)
	emotion_strengths = Element("emotion_strength")
	for key, value in emotionStrengths.items():
		emotion = SubElement(emotion_strengths, "emotion")
		emotion.attrib["emotion"] = str(key)
		emotion.attrib["strength"] = str(value)
	animation.append(emotion_strengths)
	keyframeList = Element("keyframeList")
	animation.append(keyframeList)

	# key is 0
	key = Element("key")
	key.attrib["t"] = str(0)
	keyframeList.append(key)
	orderedBSWeight = ""
	speechCoeffAnimation = blending.calculatingSpeechCoefficient(relationOfM_x, relationOfM_y, 0)
	for bsName in emotionAnimation.orderedBSList:
		orderedBSWeight = blending.blendingEmotionAndSpeech(orderedBSWeight, bsName, emotionAnimation, speechAnimation, 0, speechCoeffAnimation)
	faceWeights = Element("faceWeights")
	faceWeights.text = orderedBSWeight
	key.append(faceWeights)
	# head nodding
	orderedHNWeight = ""
	orderedHNWeight = pitchInfo.noddingInterp(0)
	headNoddingWeights = Element("headNodding")
	headNoddingWeights.text = orderedHNWeight
	key.append(headNoddingWeights)

	for i in range(0, (int)(audioSize), (int)(1000 / fps)):
		if i is 0:
			continue
		# key is greater than 0
		sub_key = SubElement(keyframeList, "key")
		sub_key.attrib["t"] = str(i)
		speechCoeffAnimation = blending.calculatingSpeechCoefficient(relationOfM_x, relationOfM_y, speechAnimation.getValueFromTimeInAttribute('M', i))
		orderedBSWeight = ""
		for bsName in emotionAnimation.orderedBSList:
			orderedBSWeight = blending.blendingEmotionAndSpeech(orderedBSWeight, bsName, emotionAnimation, speechAnimation, i, speechCoeffAnimation)
		faceWeights = Element("faceWeights")
		faceWeights.text = orderedBSWeight
		sub_key.append(faceWeights)
		# head nodding
		orderedHNWeight = ""
		orderedHNWeight = pitchInfo.noddingInterp(i)
		headNoddingWeights = Element("headNodding")
		headNoddingWeights.text = orderedHNWeight
		sub_key.append(headNoddingWeights)

	def indent(elem, level=0):
		i = "\n" + level * "	"
		if len(elem):
			if not elem.text or not elem.text.strip():
				elem.text = i + "	"
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
			for elem in elem:
				indent(elem, level + 1)
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
		else:
			if level and (not elem.tail or not elem.tail.strip()):
				elem.tail = i

	indent(animation)
	dump(animation)
	ElementTree(animation).write("animation_data.xml", encoding='utf-8', xml_declaration=True)




def generateOutputFileInSpeech(Animation, audioSize, fps, inputGender, inputHair, pitchInfo, emotionStrengths):
	animation = Element("animation")
	animation.attrib["name"] = "speech_animation"
	gender = Element("gender")
	gender.attrib["gender"] = inputGender
	animation.append(gender)
	hairModel = Element("hair_model")
	hairModel.attrib["hair_model"] = inputHair
	animation.append(hairModel)
	emotion_strengths = Element("emotion_strength")
	for key, value in emotionStrengths.items():
		emotion = SubElement(emotion_strengths, "emotion")
		emotion.attrib["emotion"] = str(key)
		emotion.attrib["strength"] = str(value)
	animation.append(emotion_strengths)
	keyframeList = Element("keyframeList")
	animation.append(keyframeList)
	key = Element("key")
	key.attrib["t"] = str(0)
	keyframeList.append(key)
	orderedBSWeight = ""
	for bsName in Animation.orderedBSList:
		if bsName in Animation.attrList:
			orderedBSWeight = orderedBSWeight + str(Animation.getValueFromTimeInAttribute(bsName, 0)) + " "
		else:
			orderedBSWeight = orderedBSWeight + "0.0 "
	faceWeights = Element("faceWeights")
	faceWeights.text = orderedBSWeight
	key.append(faceWeights)
	# head nodding
	orderedHNWeight = ""
	orderedHNWeight = pitchInfo.noddingInterp(0)
	headNoddingWeights = Element("headNodding")
	headNoddingWeights.text = orderedHNWeight
	key.append(headNoddingWeights)
	# key is greater than 0
	for i in range(0, (int)(audioSize), (int)(1000 / fps)):
		if i is 0:
			continue
		sub_key = SubElement(keyframeList, "key")
		sub_key.attrib["t"] = str(i)
		orderedBSWeight = ""
		for bsName in Animation.orderedBSList:
			if bsName in Animation.attrList:
				orderedBSWeight = orderedBSWeight + str(Animation.getValueFromTimeInAttribute(bsName, i)) + " "
			else:
				orderedBSWeight = orderedBSWeight + "0.0 "
		faceWeights = Element("faceWeights")
		faceWeights.text = orderedBSWeight
		sub_key.append(faceWeights)
		# head nodding
		orderedHNWeight = ""
		orderedHNWeight = pitchInfo.noddingInterp(i)
		headNoddingWeights = Element("headNodding")
		headNoddingWeights.text = orderedHNWeight
		sub_key.append(headNoddingWeights)

	def indent(elem, level=0):
		i = "\n" + level * "	"
		if len(elem):
			if not elem.text or not elem.text.strip():
				elem.text = i + "	"
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
			for elem in elem:
				indent(elem, level + 1)
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
		else:
			if level and (not elem.tail or not elem.tail.strip()):
				elem.tail = i

	indent(animation)
	dump(animation)
	ElementTree(animation).write("animation_data.xml", encoding='utf-8', xml_declaration=True)