import speech
import io
import numpy as np
import emotion
import os
import json
import random

def generate_tts_speech_animation(animation_generator, sentence_file_path, tts_activation_file_path,
                               tts_activation_timestep = 25, timestep_hop =3):
    print("Loading TTS neural activation data...")
    tts_activation = np.load(tts_activation_file_path, 'readonly')

    print("Loading TTS sentence text...")
    with io.open(sentence_file_path, 'r', encoding = 'utf8') as file_path:
        lines = file_path.read().splitlines()
        jamo = lines[1] if len(lines) >= 2 else speech.decompose_korean_to_jamo(lines[0])
        jamo += ' ' * max(0, tts_activation.shape[0] - len(jamo))

    print('Animating TTS-neural-activation-based lip synch...')
    lip_sync_animator = speech.TTSLipSynchAnimator(animation_generator)
    return lip_sync_animator.process_prolonged_sound(jamo, tts_activation,
                                                   tts_activation_timestep, timestep_hop)

def generate_emotion_animation(animation_generator,emotion_dir_path, emotion_strengths, audio_size):
    print('Loading emotion data...')
    emotion_animations = []
    weights = []
    for emotion_name, emotion_weight in emotion_strengths.items():
        random_number = random.randrange(0, 3)
        emotion_file_path = os.path.join(emotion_dir_path,
                                         '%s_%d.json' % (emotion_name, random_number))
        with open(emotion_file_path, 'r') as file_path:
            data = json.load(file_path, encoding = 'utf-8')
            data['keys'] = {int(key): value for key, value in data['keys'].items()}
            emotion_animations.append(data)
            weights.append(emotion_weight)

    print('Animating emotion...')
    emotion_animator = emotion.EmotionAnimator(animation_generator)
    emotion_animator.make_emotion(0.0, emotion_animations, weights, audio_size)
