import operator
import math

class TimeSeries:
    def __init__(self, records):
        self.records = sorted(records, key = operator.itemgetter(0))
        self.sample_cache = {}

    def sample(self, time):
        if time in self.sample_cache:
            return self.sample_cache[time]

        current_record = None
        previous_record = self.records[0]
        for current_record in self.records:
            if current_record[0] >= time:
                break
            previous_record = current_record

        if current_record is previous_record:
            # if this is true, it must be the first or last
            # do not interpolate if the record is the first or last
            sample_value = current_record[1]
        else:
            # interpolate two adjacent samples in linear manner
            ratio = (time - previous_record[0]) / (current_record[0] - previous_record[0])
            sample_value = ratio * current_record[1] + (1.0 - ratio) * previous_record[1]

        self.sample_cache[time] = sample_value
        return sample_value

    def __getitem__(self, item):
        return self.records[item]

    def mean(self, selector = lambda time, value: True):
        count = 0
        summation = 0

        for record in self.records:
            time, value = record
            if selector(time, value):
                summation += value
                count += 1

        return (summation / count) if count > 0 else 0

    def map(self, operation):
        result_records = []
        for record in self.records:
            time, value = record
            result_record = operation(time, value)
            if result_record:
                result_records.append(result_record)

        return TimeSeries(result_records)

    def log(self):
        return self.map(lambda time, value: (time, math.log(1 + value)))

    def multiply(self, scale):
        return self.map(lambda time, value: (time, scale * value))

    def moving_average(self, step_interval, window_time_span, window_alignment ='center'):
        def windowed_average(time):
            window_size = int(window_time_span / step_interval + 0.5)
            if window_size <= 0:
                return 0

            if window_alignment == 'center':
                window_left_span = window_size // 2
                window_right_span = window_size - window_left_span
            elif window_alignment == 'right':
                window_left_span = window_size - 1
                window_right_span = 1
            elif window_alignment == 'left':
                window_left_span = 0
                window_right_span = window_size
            else:
                raise ValueError("Bad window_align value")

            summation = 0
            for step_index in range(-window_left_span, window_right_span):
                sample_time = time + step_index * step_interval
                summation += self.sample(sample_time)

            return summation / window_size

        starting_time = self.records[0][0]
        time_range = self.records[-1][0] - starting_time
        last_step = int(time_range / step_interval + 0.5)

        result_records = []
        for step_index in range(0, last_step + 1):
            time = starting_time + step_index * step_interval
            result_records.append((time, windowed_average(time)))

        return TimeSeries(result_records)

    def resample(self, step_interval):
        starting_time = self.records[0][0]
        time_range = self.records[-1][0] - starting_time
        last_step = int(time_range / step_interval + 0.5)

        result_records = []
        for step_index in range(0, last_step + 1):
            sample_time = starting_time + step_index * step_interval
            result_records.append((sample_time, self.sample(sample_time)))

        return TimeSeries(result_records)
