# -*- coding: utf-8 -*-
from collections import OrderedDict
import numpy as np


viseme_blendshapes = ('AAA', 'Eh', 'SI', 'UH', 'O', 'WOO', 'M', 'LNTD', 'UUU', 'SSH',
                      'TTH', 'FFF', 'AHH', 'OHH', 'RRR', 'IEE', 'WWW', 'SSS', 'MBP', 'Rest')
hangul_jamo_map = (
        (u'ㄱ', u'ㄲ', u'ㄴ', u'ㄷ', u'ㄸ', u'ㄹ', u'ㅁ', u'ㅂ', u'ㅃ', u'ㅅ',
         u'ㅆ', u'ㅇ', u'ㅈ', u'ㅉ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ'),
        (u'ㅏ', u'ㅐ', u'ㅑ', u'ㅒ', u'ㅓ', u'ㅔ', u'ㅕ', u'ㅖ', u'ㅗ', u'ㅘ',
         u'ㅙ', u'ㅚ', u'ㅛ', u'ㅜ', u'ㅝ', u'ㅞ', u'ㅟ', u'ㅠ', u'ㅡ', u'ㅢ', u'ㅣ'),
        ('', u'ㄱ', u'ㄲ', u'ㄳ', u'ㄴ', u'ㄵ', u'ㄶ', u'ㄷ', u'ㄹ', u'ㄺ',
         u'ㄻ', u'ㄼ', u'ㄽ', u'ㄾ', u'ㄿ', u'ㅀ', u'ㅁ', u'ㅂ',
        u'ㅄ', u'ㅅ', u'ㅆ', u'ㅇ', u'ㅈ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ')
    )

def decompose_korean_to_jamo(unicode_text):
    result_text = str()
    for grapheme in unicode_text:
        code_point = ord(grapheme)
        if 0xAC00 <= code_point <= 0xD7AF:
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


class TTSData(object):
    def __init__(self, tts_activation):
        self.data = tts_activation
        self.highest_value_idx_by_frame = []
        self.unit = 0.0625  # 62.5ms

    def set_highest_idx(self):
        for i in range(len(self.data[0])):
            tmp = self.data[:, i]
            self.highest_value_idx_by_frame.append(np.where(tmp == max(tmp))[0][0])

    def get_highest_idx(self):
        if len(self.highest_value_idx_by_frame) == 0:
            self.set_highest_idx()
        return self.highest_value_idx_by_frame


def rescale(source_value, source_range):
    normalized_value = max(0.0, source_value - source_range[0]) / \
                       (source_range[1] - source_range[0])
    return normalized_value


class TTSLipSynchAnimator:
    def __init__(self, animation_generator):
        self.animation_generator = animation_generator

        # Phoneme to viseme mapping
        self.viseme_map = {
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
            'D': 'LNTD', 'DX': 'LNTD', 'EN': 'LNTD', 'L': 'LNTD',
            'N': 'LNTD', 'NX': 'LNTD', 'T': 'LNTD',
            'G': 'IEE', 'K': 'IEE', 'NG': 'IEE',
            'sil': 'Rest', 'sp': 'Rest',
            u'ㄱ': 'IEE', u'ㅋ': 'IEE', u'ㄲ': 'IEE', u'ㅇ': 'IEE',
            u'ㄳ': 'IEE', u'ㄺ': 'IEE', u'ㅎ': 'IEE',
            u'ㄷ': 'LNTD', u'ㅌ': 'LNTD', u'ㄸ': 'LNTD', u'ㄴ': 'LNTD', u'ㄹ': 'LNTD', u'ㄵ': 'LNTD',
            u'ㄶ': 'LNTD', u'ㄽ': 'LNTD', u'ㄾ': 'LNTD', u'ㅀ': 'LNTD', u'ㄼ': 'LNTD',
            u'ㅁ': 'M', u'ㅂ': 'M', u'ㅍ': 'M', u'ㅃ': 'M', u'ㄻ': 'M', u'ㄿ': 'M', u'ㅄ': 'M',
            u'ㅅ': 'SSS', u'ㅆ': 'SSS', u'ㅈ': 'SSH', u'ㅊ': 'SSH', u'ㅉ': 'SSH',
            u'ㅐ': 'Eh', u'ㅔ': 'Eh', u'ㅏ': 'AAA', u'ㅜ': 'WOO', u'ㅗ': 'O', u'ㅡ': 'SI', u'ㅣ': 'SI',
            u'ㅢ': 'SI', u'ㅓ': 'UH',
            u'ㅑ': 'AAA', u'ㅕ': 'UH', u'ㅛ': 'O', u'ㅠ': 'WOO', u'ㅒ': 'Eh', u'ㅖ': 'Eh',
            u'ㅘ': (u'ㅗ', u'ㅏ'), u'ㅚ': (u'ㅗ', u'ㅣ'), u'ㅙ': (u'ㅗ', u'ㅐ'),
            u'ㅝ': (u'ㅜ', u'ㅓ'), u'ㅟ': (u'ㅜ', u'ㅣ'), u'ㅞ': (u'ㅜ', u'ㅔ'),
        }

        self.consonant_list = ['RRR', 'SSH', 'LNTD']

        self.max_weight = 0.65
        self.min_weight = 0.0

    def process(self, jamo, tts_activation, tts_activation_timestep, timestep_hop = 1):
        tts = TTSData(tts_activation)
        spf_unit = tts_activation_timestep

        min_m, max_m = 0, 0

        if len(tts.data) != len(jamo):
            raise ValueError('(Length Error) Given text is incorrect: %d (tts) != %d (jamo)'
                             % (len(tts.data), len(jamo)))

        for f in range(len(tts.data[0])):
            f2 = (f // timestep_hop) * timestep_hop
            jamo_list = OrderedDict()

            for i, _ in enumerate(jamo):
                viseme_name = 'Rest'

                if jamo[i] in self.viseme_map:
                    viseme_name = self.viseme_map[jamo[i]]

                if viseme_name in jamo_list:
                    jamo_list[viseme_name] += tts.data[i, f2]
                else:
                    jamo_list[viseme_name] = tts.data[i, f2]

            for i in range(len(jamo_list)):
                weight = jamo_list.values()[i]
                if type(jamo_list.keys()[i]) is tuple:
                    self._key_single_viseme(self.viseme_map[jamo_list.keys()[i][0]],
                                            weight * self.max_weight, f2 * spf_unit)
                    post_time = (f2 * spf_unit) + (spf_unit * (2 / 3.0))
                    self._key_single_viseme(self.viseme_map[jamo_list.keys()[i][1]],
                                            weight * self.max_weight, post_time)
                else:
                    if jamo_list.keys()[i] == 'Rest':
                        jamo_list['Rest'] *= 0.4
                    self._key_single_viseme(jamo_list.keys()[i],
                                            weight * self.max_weight,
                                            f2 * spf_unit)
                    if jamo_list.keys()[i] == 'M':
                        if (weight * self.max_weight) < min_m:
                            min_m = (weight * self.max_weight)
                        if (weight * self.max_weight) > max_m:
                            max_m = (weight * self.max_weight)

        return len(tts.data[0]), min_m, max_m
        # size of audio, minimum blendshape weight of M, maximum blendshape weight of M


    def process_prolonged_sound(self,
                                jamo,
                                tts_activation,
                                tts_activation_timestep,
                                timestep_hop = 1):
        syllable = []
        for i, _ in enumerate(jamo):
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


        tts = TTSData(tts_activation)
        spf_unit = tts_activation_timestep

        min_m, max_m = 0, 0

        if len(tts.data) != len(jamo):
            raise ValueError('(Length Error) Given text is incorrect: %d (tts) != %d (jamo)'
                             % (len(tts.data), len(jamo)))

        for f in range(len(tts.data[0])):
            f2 = (f // timestep_hop) * timestep_hop
            jamo_list = OrderedDict()

            for i, _ in enumerate(jamo):
                viseme_name = 'Rest'

                if jamo[i] in self.viseme_map:
                    viseme_name = self.viseme_map[jamo[i]]

                    try:
                        if syllable[i] == 'last': # if jongsung
                            if jamo[i] == u'ㅅ' or jamo[i] == u'ㅆ' \
                                    or jamo[i] == u'ㅈ' or  jamo[i] == u'ㅊ':
                                if jamo[i+1] != u'ㅇ':
                                    viseme_name = self.viseme_map[u'ㄷ']
                            elif jamo[i] == u'ㄺ':
                                if jamo[i+1] == u'ㄱ':
                                    viseme_name = self.viseme_map[u'ㄱ']
                            elif jamo[i] == u'ㄼ':
                                if jamo[i-1] == u'ㅂ' and jamo[i-2] == u'ㅏ':
                                    viseme_name = self.viseme_map[u'ㅂ']
                            elif jamo[i] == u'ㄷ':
                                if jamo[i+1] == u'ㅇ' or jamo[i+1] == u'ㅎ':
                                    if jamo[i+2] == u'ㅣ':
                                        viseme_name = self.viseme_map[u'ㅈ']
                            elif jamo[i] == u'ㅌ':
                                if jamo[i+1] == u'ㅇ' and jamo[i+1] == u'ㅣ':
                                    viseme_name = self.viseme_map[u'ㅊ']

                        elif syllable[i] == 'first':
                            if jamo[i] == u'ㅎ':
                                if jamo[i-1] == u'ㄱ' or jamo[i-1] == u'ㄷ' \
                                        or jamo[i-1] == u'ㅂ' or jamo[i-1] == u'ㅈ':
                                    viseme_name = self.viseme_map[jamo[i-1]]
                    except:
                        pass

                if viseme_name in jamo_list:
                    jamo_list[viseme_name] += tts.data[i, f2]
                else:
                    jamo_list[viseme_name] = tts.data[i, f2]

            for i in range(len(jamo_list)):
                weight = list(jamo_list.values())[i]
                if type(list(jamo_list.keys())[i]) is tuple:
                    self._key_single_viseme(self.viseme_map[list(jamo_list.keys())[i][0]],
                                            weight * self.max_weight, f2 * spf_unit)
                    post_time = (f2 * spf_unit) + (spf_unit * (2 / 3.0))
                    self._key_single_viseme(self.viseme_map[list(jamo_list.keys())[i][1]],
                                            weight * self.max_weight, post_time)
                else:
                    if list(jamo_list.keys())[i] == 'Rest':
                        jamo_list['Rest'] *= 0.4
                    self._key_single_viseme(list(jamo_list.keys())[i],
                                            weight * self.max_weight,
                                            f2 * spf_unit)
                    if list(jamo_list.keys())[i] == 'M':
                        if (weight * self.max_weight) < min_m:
                            min_m = (weight * self.max_weight)
                        if (weight * self.max_weight) > max_m:
                            max_m = (weight * self.max_weight)

        return len(tts.data[0]), min_m, max_m
        # size of audio, minimum blendshape weight of M, maximum blendshape weight of M


    def _key_all_visemes(self, weight, timing):
        weight_map = {}
        for blendshape_name in viseme_blendshapes:
            weight_map['blendshape.%s' % blendshape_name] = weight

        self.animation_generator.set_blendshape_weights(weight_map,
                                                      timing = timing,
                                                      inTangentType ='spline',
                                                      outTangentType ='spline',
                                                      refresh = False)

    def _key_single_viseme(self, viseme_name, weight, timing):
        self.animation_generator.add_value_in_attribute(attribute_name = viseme_name,
                                                     time = timing,
                                                     value = weight)
