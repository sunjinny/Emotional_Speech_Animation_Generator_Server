# -*- coding: utf-8 -*-
from collections import OrderedDict

# from praatio import tgio
import numpy as np


visemeBlendshapes = ('AAA', 'Eh', 'SI', 'UH', 'O', 'WOO', 'M', 'LNTD', 'UUU', 'SSH', 'TTH', 'FFF', 'AHH', 'OHH', 'RRR', 'IEE', 'WWW', 'SSS', 'MBP', 'Rest')
hangul_jamo_map = (
		(u'ㄱ', u'ㄲ', u'ㄴ', u'ㄷ', u'ㄸ', u'ㄹ', u'ㅁ', u'ㅂ', u'ㅃ', u'ㅅ', u'ㅆ', u'ㅇ', u'ㅈ', u'ㅉ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ',
		u'ㅎ'),
		(u'ㅏ', u'ㅐ', u'ㅑ', u'ㅒ', u'ㅓ', u'ㅔ', u'ㅕ', u'ㅖ', u'ㅗ', u'ㅘ', u'ㅙ', u'ㅚ', u'ㅛ', u'ㅜ', u'ㅝ', u'ㅞ', u'ㅟ', u'ㅠ',
		u'ㅡ', u'ㅢ', u'ㅣ'),
		('', u'ㄱ', u'ㄲ', u'ㄳ', u'ㄴ', u'ㄵ', u'ㄶ', u'ㄷ', u'ㄹ', u'ㄺ', u'ㄻ', u'ㄼ', u'ㄽ', u'ㄾ', u'ㄿ', u'ㅀ', u'ㅁ', u'ㅂ',
		u'ㅄ', u'ㅅ', u'ㅆ', u'ㅇ', u'ㅈ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ')
	)

def decompose_korean_to_jamo(unicode_text):
	# refer this page to understand korean Unicode: http://d2.naver.com/helloworld/76650
	hangul_jamo_map = (
		(u'ㄱ', u'ㄲ', u'ㄴ', u'ㄷ', u'ㄸ', u'ㄹ', u'ㅁ', u'ㅂ', u'ㅃ', u'ㅅ', u'ㅆ', u'ㅇ', u'ㅈ', u'ㅉ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ',
		u'ㅎ'),
		(u'ㅏ', u'ㅐ', u'ㅑ', u'ㅒ', u'ㅓ', u'ㅔ', u'ㅕ', u'ㅖ', u'ㅗ', u'ㅘ', u'ㅙ', u'ㅚ', u'ㅛ', u'ㅜ', u'ㅝ', u'ㅞ', u'ㅟ', u'ㅠ',
		u'ㅡ', u'ㅢ', u'ㅣ'),
		('', u'ㄱ', u'ㄲ', u'ㄳ', u'ㄴ', u'ㄵ', u'ㄶ', u'ㄷ', u'ㄹ', u'ㄺ', u'ㄻ', u'ㄼ', u'ㄽ', u'ㄾ', u'ㄿ', u'ㅀ', u'ㅁ', u'ㅂ',
		u'ㅄ', u'ㅅ', u'ㅆ', u'ㅇ', u'ㅈ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ')
	)
	result_text = str()
	for grapheme in unicode_text:
		code_point = ord(grapheme)
		if code_point >= 0xAC00 and code_point <= 0xD7AF:
			# [0xAC00, 0xD7AF]: Hangul Syllables
			korean_code_index = code_point - 0xAC00

			initial_jamo_index, korean_code_index = divmod(korean_code_index, 21 * 28)
			medial_jamo_index, final_jamo_index = divmod(korean_code_index, 28)

			initial_jamo = hangul_jamo_map[0][initial_jamo_index]
			medial_jamo = hangul_jamo_map[1][medial_jamo_index]
			final_jamo = hangul_jamo_map[2][final_jamo_index]

			result_text += initial_jamo + medial_jamo + final_jamo
		else:
			result_text += grapheme

	return result_text


class TextgridLipSynchAnimator:
	def __init__(self, modelManipulator):
		"""

		:type modelManipulator: flagship.speech_animation.maya_model_manipulator.MayaModelManipulator
		"""
		self.modelManipulator = modelManipulator

		# Phoneme to viseme mapping
		self.visemeMap = {'AE': 'Eh', 'EY': 'Eh', 'EH': 'Eh',
			'AA': 'AHH', 'AO': 'AHH', 'AY': 'AHH', 'AW': 'AHH',
			'UW': 'WWW', 'W': 'WWW', 'WH': 'WWW',
			'R': 'RRR',
			'DH': 'TTH', 'TH': 'TTH',
			'F': 'FFF', 'V': 'FFF',
			'UX': 'UUU', 'UH': 'UUU', 'HH': 'UUU', 'H': 'UUU',
			'OW': 'OHH', 'OY': 'OHH',
			'IY': 'SI', 'IH': 'SI', 'Y': 'SI', 'EL': 'SI',
			'S': 'SSS', 'Z': 'SSS',
			'JH': 'SSH', 'CH': 'SSH', 'SH': 'SSH', 'ZH': 'SSH',
			'M': 'MBP', 'B': 'MBP', 'P': 'MBP', 'EM': 'MBP',
			'AX': 'UH', 'IX': 'UH', 'AXR': 'UH', 'ER': 'UH', 'AH': 'UH', 'Q': 'UH',
			'D': 'LNTD', 'DX': 'LNTD', 'EN': 'LNTD', 'L': 'LNTD', 'N': 'LNTD', 'NX': 'LNTD', 'T': 'LNTD',
			'G': 'IEE', 'K': 'IEE', 'NG': 'IEE',
			'sil': 'Rest', 'sp': 'Rest',
			u'ㄱ': 'IEE', u'ㅋ': 'IEE', u'ㄲ': 'IEE', u'ㅇ': 'IEE', u'ㄳ': 'IEE', u'ㄺ': 'IEE', u'ㅎ': 'IEE',
			u'ㄷ': 'LNTD', u'ㅌ': 'LNTD', u'ㄸ': 'LNTD', u'ㄴ': 'LNTD', u'ㄹ': 'LNTD', u'ㄵ': 'LNTD',
			u'ㄶ': 'LNTD', u'ㄽ': 'LNTD', u'ㄾ': 'LNTD', u'ㅀ': 'LNTD', u'ㄼ': 'LNTD',
			u'ㅁ': 'M', u'ㅂ': 'M', u'ㅍ': 'M', u'ㅃ': 'M', u'ㄻ': 'M', u'ㄿ': 'M', u'ㅄ': 'M',
			u'ㅅ': 'SSS', u'ㅆ': 'SSS', u'ㅈ': 'SSH', u'ㅊ': 'SSH', u'ㅉ': 'SSH',
			u'ㅐ': 'Eh', u'ㅔ': 'Eh', u'ㅏ': 'AAA', u'ㅜ': 'WOO', u'ㅗ': 'O', u'ㅡ': 'SI', u'ㅣ': 'SI',
			u'ㅢ': 'SI', u'ㅓ': 'UH'}

		self.diphthongMap = {u'ㅑ': [u'ㅣ', u'ㅏ'], u'ㅕ': [u'ㅣ', u'ㅓ'], u'ㅛ': [u'ㅣ', u'ㅗ'], u'ㅠ': [u'ㅣ', u'ㅜ'],
			u'ㅒ': [u'ㅣ', u'ㅐ'], u'ㅖ': [u'ㅣ', u'ㅔ'],
			u'ㅘ': [u'ㅗ', u'ㅏ'], u'ㅚ': [u'ㅗ', u'ㅣ'], u'ㅙ': [u'ㅗ', u'ㅐ'],
			u'ㅝ': [u'ㅜ', u'ㅓ'], u'ㅟ': [u'ㅜ', u'ㅣ'], u'ㅞ': [u'ㅜ', u'ㅔ']}

		self.consonantList = ['RRR', 'SSH', 'LNTD']  # 수정 : "SSS" 삭제

	# def process(self, textgridFilePath):
	# 	weight = 0.65

	# 	# Get TextGrid file from the Penn Phonetic Forced Alignment Toolkit through cygwins
	# 	textgrid = tgio.openTextgrid(textgridFilePath)

	# 	# Get phone tier
	# 	phoneTier = textgrid.tierDict['phone']

	# 	for startingTime, endingTime, phoneme in phoneTier.entryList:
	# 		# Key-framing the viseme blendshape
	# 		self._insertPhonemeAnimation(startingTime, endingTime, phoneme, 0.0, weight)

	def _insertPhonemeAnimation(self, startingTime, endingTime, phoneme, weightViseme, weightOtherVisemes):
		if phoneme in self.diphthongMap:
			diphthong = self.diphthongMap[phoneme]

			self._keyViseme(self.visemeMap[diphthong[0]], weightViseme, weightOtherVisemes, startingTime)
			postTime = startingTime + (endingTime - startingTime) * (2 / 3.0)
			self._keyViseme(self.visemeMap[diphthong[1]], weightViseme, weightOtherVisemes, postTime)

		else:
			weight = weightViseme
			visemeName = self.visemeMap[phoneme]

			if visemeName in self.consonantList:
				# weight = weight*0.85
				return

			if visemeName == 'Rest':
				weight = weight * 0.4

			self._keyViseme(visemeName, weight, weightOtherVisemes, startingTime)

	def _keyViseme(self, visemeName, weight, weightOthers, timing):
		weightMap = {}
		for blendshapeName in visemeBlendshapes:
			weightMap['blendshape.%s' % blendshapeName] = weightOthers

		weightMap['blendshape.%s' % visemeName] = weight

		self.modelManipulator.setBlendshapeWeights(weightMap, timing = timing, inTangentType = 'spline', outTangentType = 'spline', refresh = False)


class TTSData(object):
	def __init__(self, ttsActivation):
		self.data = ttsActivation
		self.highestValueIdxByFrame = []
		self.unit = 0.0625  # 62.5ms

		# def lenJamo(self): return len(self.data)
		# def lenFrame(self): return len(self.data[0])

	def setHighestIdx(self):
		for i in range(len(self.data[0])):
			tmp = self.data[:, i]
			self.highestValueIdxByFrame.append(np.where(tmp == max(tmp))[0][0])

	def getHighestIdx(self):
		if len(self.highestValueIdxByFrame) == 0:
			self.setHighestIdx()
		return self.highestValueIdxByFrame

		# def getValueByFrame(self, fr): return self.data[:,fr]


def rescale(sourceValue, sourceRange):
	normalizedValue = max(0.0, sourceValue - sourceRange[0]) / (sourceRange[1] - sourceRange[0])
	return normalizedValue


class TTSLipSynchAnimator:
	def __init__(self, animationGenerator):
		"""

		:param animationGenerator:
		:type animationGenerator: flagship.speech_animation.maya_model_manipulator.MayaModelManipulator
		"""
		self.animationGenerator = animationGenerator

		# Phoneme to viseme mapping
		self.visemeMap = {
			'AE': 'Eh', 'EY': 'Eh', 'EH': 'Eh',
			'AA': 'AHH', 'AO': 'AHH', 'AY': 'AHH', 'AW': 'AHH',
			'UW': 'WWW', 'W': 'WWW', 'WH': 'WWW',
			'R': 'RRR',
			'DH': 'TTH', 'TH': 'TTH',
			'F': 'FFF', 'V': 'FFF',
			'UX': 'UUU', 'UH': 'UUU', 'HH': 'UUU', 'H': 'UUU',
			'OW': 'OHH', 'OY': 'OHH',
			'IY': 'SI', 'IH': 'SI', 'Y': 'SI', 'EL': 'SI',
			'S': 'SSS', 'Z': 'SSS',
			'JH': 'SSH', 'CH': 'SSH', 'SH': 'SSH', 'ZH': 'SSH',
			'M': 'MBP', 'B': 'MBP', 'P': 'MBP', 'EM': 'MBP',
			'AX': 'UH', 'IX': 'UH', 'AXR': 'UH', 'ER': 'UH', 'AH': 'UH', 'Q': 'UH',
			'D': 'LNTD', 'DX': 'LNTD', 'EN': 'LNTD', 'L': 'LNTD', 'N': 'LNTD', 'NX': 'LNTD', 'T': 'LNTD',
			'G': 'IEE', 'K': 'IEE', 'NG': 'IEE',
			'sil': 'Rest', 'sp': 'Rest',
			u'ㄱ': 'IEE', u'ㅋ': 'IEE', u'ㄲ': 'IEE', u'ㅇ': 'IEE', u'ㄳ': 'IEE', u'ㄺ': 'IEE', u'ㅎ': 'IEE',
			u'ㄷ': 'LNTD', u'ㅌ': 'LNTD', u'ㄸ': 'LNTD', u'ㄴ': 'LNTD', u'ㄹ': 'LNTD', u'ㄵ': 'LNTD',
			u'ㄶ': 'LNTD', u'ㄽ': 'LNTD', u'ㄾ': 'LNTD', u'ㅀ': 'LNTD', u'ㄼ': 'LNTD',
			u'ㅁ': 'M', u'ㅂ': 'M', u'ㅍ': 'M', u'ㅃ': 'M', u'ㄻ': 'M', u'ㄿ': 'M', u'ㅄ': 'M',
			u'ㅅ': 'SSS', u'ㅆ': 'SSS', u'ㅈ': 'SSH', u'ㅊ': 'SSH', u'ㅉ': 'SSH',
			u'ㅐ': 'Eh', u'ㅔ': 'Eh', u'ㅏ': 'AAA', u'ㅜ': 'WOO', u'ㅗ': 'O', u'ㅡ': 'SI', u'ㅣ': 'SI',
			u'ㅢ': 'SI', u'ㅓ': 'UH',
			u'ㅑ': 'AAA', u'ㅕ': 'UH', u'ㅛ': 'O', u'ㅠ': 'WOO', u'ㅒ': 'Eh', u'ㅖ': 'Eh',
			u'ㅘ': (u'ㅗ', u'ㅏ'), u'ㅚ': (u'ㅗ', u'ㅣ'), u'ㅙ': (u'ㅗ', u'ㅐ'),
			u'ㅝ': (u'ㅜ', u'ㅓ'), u'ㅟ': (u'ㅜ', u'ㅣ'), u'ㅞ': (u'ㅜ', u'ㅔ'),
			# u'ㅑ': (u'ㅣ', u'ㅏ'), u'ㅕ': (u'ㅣ', u'ㅓ'), u'ㅛ': (u'ㅣ', u'ㅗ'), u'ㅠ': (u'ㅣ', u'ㅜ'),
			# u'ㅒ': (u'ㅣ', u'ㅐ'), u'ㅖ': (u'ㅣ', u'ㅔ'),
		}

		self.consonantList = ['RRR', 'SSH', 'LNTD']  # 수정 : "SSS" 삭제

		self.maxWeight = 0.65
		self.minWeight = 0.0

	def process(self, jamo, ttsActivation, ttsActivationTimestep, timestepHop = 1):
		tts = TTSData(ttsActivation)
		spfUnit = ttsActivationTimestep

		minM, maxM = 0, 0

		if len(tts.data) != len(jamo):
			raise ValueError('(Length Error) Given text is incorrect: %d (tts) != %d (jamo)' % (len(tts.data), len(jamo)))

		for f in range(len(tts.data[0])):
			f2 = (f // timestepHop) * timestepHop
			jamoList = OrderedDict()

			for i in range(len(jamo)):
				visemeName = 'Rest'

				if jamo[i] in self.visemeMap:
					visemeName = self.visemeMap[jamo[i]]

				if visemeName in jamoList:
					jamoList[visemeName] += tts.data[i, f2]
				else:
					jamoList[visemeName] = tts.data[i, f2]

			# self._keyAllVisemes(self.minWeight, f * spfUnit)
			for i in range(len(jamoList)):
				weight = jamoList.values()[i]
				# weight = rescale(weight, (0.25, 1.0))
				# if (jamoList.values()[i] * self.maxWeight) > 0.01: # Denoising
				if type(jamoList.keys()[i]) is tuple:
					self._keySingleViseme(self.visemeMap[jamoList.keys()[i][0]], weight * self.maxWeight, f2 * spfUnit)
					postTime = (f2 * spfUnit) + (spfUnit * (2 / 3.0))
					self._keySingleViseme(self.visemeMap[jamoList.keys()[i][1]], weight * self.maxWeight, postTime)
				else:
					if jamoList.keys()[i] == 'Rest':
						jamoList['Rest'] *= 0.4
					self._keySingleViseme(jamoList.keys()[i], weight * self.maxWeight, f2 * spfUnit)
					if jamoList.keys()[i] == 'M':
						if (weight * self.maxWeight) < minM:
							minM = (weight * self.maxWeight)
						if (weight * self.maxWeight) > maxM:
							maxM = (weight * self.maxWeight)



		return len(tts.data[0]), minM, maxM # size of audio, minimum blendshape weight of M, maximum blendshape weight of M

	def process_prolonged_sound(self, jamo, ttsActivation, ttsActivationTimestep, timestepHop = 1):

		syllable = []
		for i in range(len(jamo)):
			if jamo[i] in hangul_jamo_map[1]: # vowel
				syllable.append('middle')
			elif jamo[i] in hangul_jamo_map[2]: # consonant
				if i == 0:
					syllable.append('first')
				elif syllable[i-1] == 'rest':
					syllable.append('first')
				elif syllable[i-1] == 'first':
					syllable[i-1] = 'last'
					syllable.append('first')
				else:
					syllable.append('first')
			else : # rest
				syllable.append('rest')
				if syllable[i-1] == 'first':
					syllable[i-1] = 'last'


		tts = TTSData(ttsActivation)
		spfUnit = ttsActivationTimestep

		minM, maxM = 0, 0

		if len(tts.data) != len(jamo):
			raise ValueError('(Length Error) Given text is incorrect: %d (tts) != %d (jamo)' % (len(tts.data), len(jamo)))

		highestIdxList = tts.getHighestIdx()

		for f in range(len(tts.data[0])):
			f2 = (f // timestepHop) * timestepHop
			jamoList = OrderedDict()

			for i in range(len(jamo)):
				visemeName = 'Rest'

				if jamo[i] in self.visemeMap:
					visemeName = self.visemeMap[jamo[i]]

					try:
						if syllable[i] == 'last': # if jongsung
							if jamo[i] == u'ㅅ' or jamo[i] == u'ㅆ' or jamo[i] == u'ㅈ' or  jamo[i] == u'ㅊ':
								if jamo[i+1] != u'ㅇ':
									visemeName = self.visemeMap[u'ㄷ']
							elif jamo[i] == u'ㄺ':
								if jamo[i+1] == u'ㄱ':
									visemeName = self.visemeMap[u'ㄱ']
							elif jamo[i] == u'ㄼ':
								if jamo[i-1] == u'ㅂ' and jamo[i-2] == u'ㅏ':
									visemeName = self.visemeMap[u'ㅂ']
							elif jamo[i] == u'ㄷ':
								if jamo[i+1] == u'ㅇ' or jamo[i+1] == u'ㅎ':
									if jamo[i+2] == u'ㅣ':
										visemeName = self.visemeMap[u'ㅈ']
							elif jamo[i] == u'ㅌ':
								if jamo[i+1] == u'ㅇ' and jamo[i+1] == u'ㅣ':
									visemeName = self.visemeMap[u'ㅊ']

						elif syllable[i] == 'first':
							if jamo[i] == u'ㅎ':
								if jamo[i-1] == u'ㄱ' or jamo[i-1] == u'ㄷ' or jamo[i-1] == u'ㅂ' or jamo[i-1] == u'ㅈ':
									visemeName = self.visemeMap[jamo[i-1]]
					except:
						pass


				if visemeName in jamoList:
					jamoList[visemeName] += tts.data[i, f2]
				else:
					jamoList[visemeName] = tts.data[i, f2]

			# self._keyAllVisemes(self.minWeight, f * spfUnit)
			for i in range(len(jamoList)):
				weight = list(jamoList.values())[i]
				# weight = rescale(weight, (0.25, 1.0))
				# if (jamoList.values()[i] * self.maxWeight) > 0.01: # Denoising
				if type(list(jamoList.keys())[i]) is tuple:
					self._keySingleViseme(self.visemeMap[list(jamoList.keys())[i][0]], weight * self.maxWeight, f2 * spfUnit)
					postTime = (f2 * spfUnit) + (spfUnit * (2 / 3.0))
					self._keySingleViseme(self.visemeMap[list(jamoList.keys())[i][1]], weight * self.maxWeight, postTime)
				else:
					if list(jamoList.keys())[i] == 'Rest':
						jamoList['Rest'] *= 0.4
					self._keySingleViseme(list(jamoList.keys())[i], weight * self.maxWeight, f2 * spfUnit)
					if list(jamoList.keys())[i] == 'M':
						if (weight * self.maxWeight) < minM:
							minM = (weight * self.maxWeight)
						if (weight * self.maxWeight) > maxM:
							maxM = (weight * self.maxWeight)



		return len(tts.data[0]), minM, maxM # size of audio, minimum blendshape weight of M, maximum blendshape weight of M


	def _keyAllVisemes(self, weight, timing):
		weightMap = {}
		for blendshapeName in visemeBlendshapes:
			weightMap['blendshape.%s' % blendshapeName] = weight

		self.animationGenerator.setBlendshapeWeights(weightMap, timing = timing, inTangentType ='spline', outTangentType ='spline', refresh = False)

	def _keySingleViseme(self, visemeName, weight, timing):
		weightMap = {'blendshape.%s' % visemeName: weight}

		# self.animationGenerator.setBlendshapeWeights(weightMap, timing = timing, inTangentType ='spline', outTangentType ='spline', refresh = False)
		self.animationGenerator.addValueInAttribute(attributeName = visemeName, time = timing, value = weight)
