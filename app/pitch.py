import math
import numpy as np
import librosa
import time_series

class HeadNodding:
    def __init__(self, audio_file_path):
        self.audio_file_path = audio_file_path
        self.neck_angle_records = []
        self.pitch_records = []
        # y : audio time series     sr : sampling rate of y (default = 22050)
        self.y, self.sr = librosa.load(self.audio_file_path)
        self.wav_length = librosa.get_duration(y = self.y, sr = self.sr)

    def detect_pitch(self):
        onset_offset = 0
        frame_stride = 0.016
        _stride = int(round(self.sr * frame_stride))
        onset_frames = librosa.onset.onset_detect(
            y = self.y, sr = self.sr, hop_length = _stride)

        # time
        time = librosa.frames_to_time(
            onset_frames, sr = self.sr, hop_length = _stride)

        # pitch
        pitches, magnitudes = librosa.piptrack(
            y = self.y, sr = self.sr, fmin = 75, fmax = 1400, hop_length = _stride)
        save_pitch = []

        for i, _ in enumerate(onset_frames):
            onset = onset_frames[i] + onset_offset
            index = magnitudes[:, onset].argmax()
            pitch = pitches[index, onset]
            pitch = max(pitch, 0) # threshold
            save_pitch.append(pitch)
            result = (time[i], save_pitch[i])  # tuple
            self.pitch_records.append(result)

        return self.pitch_records


    def key_pitch_related_nodding(self):
        self.pitch_records += [(self.pitch_records[-1][0] + 0.4, 0)]

        # make time series
        pitch_time_series = time_series.TimeSeries(self.pitch_records)

        # take log of the f0 frequency
        pitch_time_series = pitch_time_series.log()

        # zero-mean for non-zero frequencies
        mean = pitch_time_series.mean(lambda time, value: value > 0)
        pitch_time_series = pitch_time_series.map(
            lambda time, value: (time, (value - mean) if value > 0 else value))

        # moving average
        pitch_time_series = pitch_time_series.moving_average(0.01, 0.8, 'center')

        # multiply
        pitch_time_series = pitch_time_series.multiply(30)

        # resample
        pitch_time_series = pitch_time_series.resample(0.3)


        result = (0, (0, 0, 0))  # initial pose
        self.neck_angle_records.append(result)

        for record in pitch_time_series:  # pose based on pitch
            time, value = record
            result = (time, ((math.pi / 180) * -1.0 * value, 0, 0))  # euler to radian
            self.neck_angle_records.append(result)

        result = (self.wav_length, (0, 0, 0))  # final pose
        self.neck_angle_records.append(result)
        return self.neck_angle_records


    def nodding_interp(self, access_time):
        nodding_time = []
        nodding_value = []

        for i in range(len(self.neck_angle_records)):
            nodding_time.append(self.neck_angle_records[i][0])
            nodding_value.append(self.neck_angle_records[i][1][0])

        result_interp = np.interp(access_time * 0.001, nodding_time, nodding_value)
        result = str(result_interp * 0.3) + " 0.0 0.0"
        return result
    