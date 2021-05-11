import animation
import interactive
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import exporting_output
import pitch


app = Flask(__name__)

@app.route('/emotional-facial-animation/interactive')
def render_file():
    return render_template('interactive.html')

@app.route('/emotional-facial-animation/rest/generate-animation', methods = ['GET', 'POST'])
def upload_files():
    if 'sentence_jaso' not in request.files:
        return 'sentence_jaso is not given', 400
    if 'sentence_neural_timing' not in request.files:
        return 'sentence_neural_timing is not given', 400
    if 'sentence_audio_wav' not in request.files:
        return 'sentence_audio_wav is not given', 400

    sentence_file = request.files['sentence_jaso']
    sentence_file_path = "./"+secure_filename(sentence_file.filename)
    sentence_file.save(sentence_file_path)

    tts_activation_file = request.files['sentence_neural_timing']
    tts_activation_file_path = "./"+secure_filename(tts_activation_file.filename)
    tts_activation_file.save(tts_activation_file_path)

    audio_file = request.files['sentence_audio_wav']
    audio_file_path = "./"+secure_filename(audio_file.filename)
    audio_file.save(audio_file_path)

    speaker_gender = request.form['speaker_gender']
    if int(speaker_gender) == 30001:
        gender = '_boy'
    elif int(speaker_gender) == 30002:
        gender = '_girl'
    else:
        return 'Invalid gender', 400

    hair_model = request.form.get('hair_model', None)
    hair_list = ['0', '1']
    if hair_model is None:
        hair_model = '0'
    elif hair_model not in hair_list:
        return 'Invalid hair_model', 400

    time_step_hop = 3
    tts_activation_timestep = 11.6 #25

    animation_generator_speech = animation.Animation('./classifiedBsNameList'+gender+'.txt')

    try:
        audio_size, min_m, max_m = interactive.generate_tts_speech_animation(
            animation_generator_speech,
            sentence_file_path,
            tts_activation_file_path,
            tts_activation_timestep,
            time_step_hop)
    except IOError:
        return 'Invaild File', 400
    except UnicodeDecodeError:
        return 'Invaild File, UnicodeDecodeError', 400
    audio_size = audio_size * tts_activation_timestep

    pitch_info = pitch.HeadNodding(audio_file_path)
    pitch_info.detect_pitch()
    pitch_info.key_pitch_related_nodding()

    animation_generator_emotion = animation.Animation('./classifiedBsNameList'+gender+'.txt')
    emotion_list = ['10001', '10002', '10003', '10004', '10006', '10007']
    emotion_strengths = {}
    emotion_check = 0
    for emotion_num in emotion_list:
        emotion_strengths[emotion_num] = float(request.form['emotion_strength['+emotion_num+']'])
        if emotion_strengths[emotion_num] > emotion_check:
            emotion_check = emotion_strengths[emotion_num]

    emotion_dir_path = './emotion_animation_keys.blendshape' + gender + '/'
    interactive.generate_emotion_animation(animation_generator_emotion,
                                         emotion_dir_path,
                                         emotion_strengths,
                                         audio_size)

    for key, value in emotion_strengths.items():
        if value == 0.0:
            emotion_strengths[key] = 0.0
        elif 0.0 < value <= 0.5:
            emotion_strengths[key] = 0.5
        else:
            emotion_strengths[key] = 1.0

    fps = 60
    if emotion_check == 0:
        exporting_output.generate_output_file_in_speech(animation_generator_speech,
                                                    int(audio_size),
                                                    fps,
                                                    speaker_gender,
                                                    hair_model,
                                                    pitch_info,
                                                    emotion_strengths)
    else:
        exporting_output.generate_output_file_in_speech_and_emotion(animation_generator_speech,
                                                              animation_generator_emotion,
                                                              audio_size,
                                                              fps,
                                                              speaker_gender,
                                                              hair_model,
                                                              min_m,
                                                              max_m,
                                                              pitch_info,
                                                              emotion_strengths)


    return send_file('./animation_data.xml', mimetype='application/xml')

if __name__ =="__main__":
    app.run(debug = True)
