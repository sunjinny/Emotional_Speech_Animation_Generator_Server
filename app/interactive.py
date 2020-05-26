import speech
import io
import numpy as np
import emotion
import os
import json
import random

def generateTTSSpeechAnimation(animationGenerator, sentenceFilePath, ttsActivationFilePath, ttsActivationTimestep = 25, timestepHop =3):
	print("Loading TTS neural activation data...")
	ttsActivation = np.load(ttsActivationFilePath, 'readonly')

	print("Loading TTS sentence text...")
	with io.open(sentenceFilePath, 'r', encoding = 'utf8') as fp:
		lines = fp.read().splitlines()
		jamo = lines[1] if len(lines) >= 2 else speech.decompose_korean_to_jamo(lines[0])
		jamo += ' ' * max(0, ttsActivation.shape[0] - len(jamo))

	print('Animating TTS-neural-activation-based lip synch...')
	lipSyncAnimator = speech.TTSLipSynchAnimator(animationGenerator)
	return lipSyncAnimator.process_prolonged_sound(jamo, ttsActivation, ttsActivationTimestep, timestepHop)

def generateEmotionAnimation(animationGenerator,emotionDirPath, emotionStrengths, audioSize):

	print('Loading emotion data...')
	emotionAnimations = []
	weights = []
	for emotionName, emotionWeight in emotionStrengths.items():
		randomNumber = random.randrange(0, 3)
		emotionFilePath = os.path.join(emotionDirPath, '%s_%d.json' % (emotionName, randomNumber))
		#emotionFilePath = os.path.join(emotionDirPath, '%s_2.json' %emotionName)
		with open(emotionFilePath, 'r') as fp:
			data = json.load(fp, encoding = 'utf-8')
			data['keys'] = {int(key): value for key, value in data['keys'].items()}
			emotionAnimations.append(data)
			weights.append(emotionWeight)

	print('Animating emotion...')
	emotionAnimator = emotion.EmotionAnimator(animationGenerator)
	emotionAnimator.makeEmotion(0.0, emotionAnimations, weights, audioSize)