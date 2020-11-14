import math
import numpy as np
import librosa
import time_series
from xml.etree.ElementTree import Element, SubElement, dump, ElementTree

class HeadNodding:
    def __init__(self, audioFilePath):
        self.audioFilePath = audioFilePath


    def detect_pitch(self):
        # y : audio time series     sr : sampling rate of y (default = 22050)
        self.y, self.sr = librosa.load(self.audioFilePath)

        # wav_length
        self.wav_length = librosa.get_duration(y = self.y, sr = self.sr)

        onset_offset = 0 #5
        frame_stride = 0.016
        self._stride = int(round(self.sr * frame_stride))
        self.onset_frames = librosa.onset.onset_detect(y = self.y, sr = self.sr, hop_length = self._stride)

        # time
        self.time = librosa.frames_to_time(self.onset_frames, sr = self.sr, hop_length = self._stride)

        # pitch
        self.pitches, self.magnitudes = librosa.piptrack(y = self.y, sr = self.sr, fmin = 75, fmax = 1400, hop_length = self._stride)
        self.savePitch = []
        self.pitchRecords = []

        for i in range(0, len(self.onset_frames)):
            self.onset = self.onset_frames[i] + onset_offset
            self.index = self.magnitudes[:, self.onset].argmax()
            self.pitch = self.pitches[self.index, self.onset]
            if (self.pitch < 0):
                self.pitch = 0      # threshold
            self.savePitch.append(self.pitch)
            self.result = (self.time[i], self.savePitch[i])  # tuple
            self.pitchRecords.append(self.result)

        return self.pitchRecords


    def keyPitchRelatedNodding(self):
        self.pitchRecords += [(self.pitchRecords[-1][0] + 0.4, 0)]

        # make time series
        self.pitchTimeSeries = time_series.TimeSeries(self.pitchRecords)

        # take log of the f0 frequency
        self.pitchTimeSeries = self.pitchTimeSeries.log()

        # zero-mean for non-zero frequencies
        self.mean = self.pitchTimeSeries.mean(lambda time, value: value > 0)
        self.pitchTimeSeries = self.pitchTimeSeries.map(
            lambda time, value: (time, (value - self.mean) if value > 0 else value))

        # moving average
        self.pitchTimeSeries = self.pitchTimeSeries.movingAverage(0.01, 0.8, 'center')

        # multiply
        self.pitchTimeSeries = self.pitchTimeSeries.multiply(30)

        # resample
        self.pitchTimeSeries = self.pitchTimeSeries.resample(0.3)

        # neck angle
        self.neckAngleRecords = []

        self.result = (0, (0, 0, 0))  # initial pose
        self.neckAngleRecords.append(self.result)

        for record in self.pitchTimeSeries:  # pose based on pitch
            time, value = record
            # self.result = (time, (-1.0 * value, 0, 0))  # euler
            self.result = (time, ((math.pi / 180) * -1.0 * value, 0, 0))  # euler to radian
            self.neckAngleRecords.append(self.result)

        self.result = (self.wav_length, (0, 0, 0))  # final pose
        self.neckAngleRecords.append(self.result)
        return self.neckAngleRecords


    def noddingInterp(self, accessTime):
        self.noddingTime = []
        self.noddingValue = []

        for i in range(len(self.neckAngleRecords)):
            self.noddingTime.append(self.neckAngleRecords[i][0])
            self.noddingValue.append(self.neckAngleRecords[i][1][0])

        self.result_interp = np.interp(accessTime * 0.001, self.noddingTime, self.noddingValue)
        self.result = str(self.result_interp) + " 0.0 0.0"
        return self.result