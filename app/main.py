import interactive
import animation
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import exporting_output
import pitch


app = Flask(__name__)

@app.route('/emotional-facial-animation/interactive')
def renderFile():
	return render_template('interactive.html')

@app.route('/emotional-facial-animation/rest/generate-animation', methods = ['GET', 'POST'])
def uploadFiles():
	if 'sentence_jaso' not in request.files:
		return 'sentence_jaso is not given', 400
	if 'sentence_neural_timing' not in request.files:
		return 'sentence_neural_timing is not given', 400
	if 'sentence_audio_wav' not in request.files:
		return 'sentence_audio_wav is not given', 400

	# dict = request.form
	# for key in dict:
	# 	print key
	# 	print 'form key ' + dict[key]

	sentenceFile = request.files['sentence_jaso']
	sentenceFilePath = "./"+secure_filename(sentenceFile.filename)
	sentenceFile.save(sentenceFilePath)

	ttsActivationFile = request.files['sentence_neural_timing']
	ttsActivationFilePath = "./"+secure_filename(ttsActivationFile.filename)
	ttsActivationFile.save(ttsActivationFilePath)

	audioFile = request.files['sentence_audio_wav']
	audioFilePath = "./"+secure_filename(audioFile.filename)
	audioFile.save(audioFilePath)

	speaker_gender = request.form['speaker_gender']
	if int(speaker_gender) == 30001:
		gender = '_boy'
	elif int(speaker_gender) == 30002:
		gender = '_girl'
	else:
		return 'Invalid gender', 400

	hair_model = request.form.get('hair_model', None)
	hairList = ['0', '1']
	if hair_model is None:
		hair_model = '0'
	elif hair_model not in hairList:
		return 'Invalid hair_model', 400


	timestepHop = 3
	ttsActivationTimestep = 25

	animationGenerator_speech = animation.Animation('./classifiedBsNameList'+gender+'.txt')

	try:
		audioSize, minM, maxM = interactive.generateTTSSpeechAnimation(animationGenerator_speech, sentenceFilePath, ttsActivationFilePath, ttsActivationTimestep, timestepHop)
	except IOError:
		return 'Invaild File', 400
	except UnicodeDecodeError:
		return 'Invaild File, UnicodeDecodeError', 400
	audioSize = audioSize * ttsActivationTimestep

	pitchInfo = pitch.HeadNodding(audioFilePath)
	pitchInfo.detect_pitch()
	pitchInfo.keyPitchRelatedNodding()

	animationGenerator_emotion = animation.Animation('./classifiedBsNameList'+gender+'.txt')
	emotionList = ['10001', '10002', '10003', '10004', '10006', '10007']
	emotionStrengths = {}
	emotionCheck = 0
	for emotionNum in emotionList:
		emotionStrengths[emotionNum] = float(request.form['emotion_strength['+emotionNum+']'])
		if emotionStrengths[emotionNum] > emotionCheck:
			emotionCheck = emotionStrengths[emotionNum]

	emotionDirPath = './emotion_animation_keys.blendshape' + gender + '/'
	interactive.generateEmotionAnimation(animationGenerator_emotion, emotionDirPath, emotionStrengths, audioSize)

	for key, value in emotionStrengths.items():
		if value == 0.0:
			emotionStrengths[key] = 0.0
		elif value > 0.0 and value <= 0.5:
			emotionStrengths[key] = 0.5
		else:
			emotionStrengths[key] = 1.0

	fps = 60
	if emotionCheck == 0:
		exporting_output.generateOutputFileInSpeech(animationGenerator_speech, int(audioSize), fps, speaker_gender, hair_model, pitchInfo, emotionStrengths)
	else:
		exporting_output.generateOutputFileInSpeechAndEmotion(animationGenerator_speech, animationGenerator_emotion, audioSize, fps, speaker_gender, hair_model, minM, maxM, pitchInfo, emotionStrengths)


	return send_file('./animation_data.xml', mimetype='application/xml')

if __name__ =="__main__":
	app.run(debug = True)
