import math

class EmotionAnimator:
    def __init__(self, animation_generator):
        self.animation_generator = animation_generator

    def make_emotion(self, start_time, emotion_animations, weights, end_time):
        def combine_sequences(weights):
            weights = [math.log(weight + 1.0, 2) for weight in weights]
            weight_sum = sum(weights)

            resulting_sequence = {}
            for emotion_animation, weight in zip(emotion_animations, weights):
                source_sequence = emotion_animation['keys']

                weight_ratio = weight / weight_sum if weight_sum != 0.0 else 0.0
                for frame, animation_key in source_sequence.items():
                    if frame not in resulting_sequence:
                        resulting_sequence[frame] = {}

                    for name, value in animation_key.items():
                        if name not in resulting_sequence[frame]:
                            resulting_sequence[frame][name] = 0.0

                        resulting_sequence[frame][name] += value * weight * weight_ratio

            return resulting_sequence

        fps = emotion_animations[0]['fps']
        combined_sequence = combine_sequences(weights)

        seq_time = 0

        for frame, animation_key in combined_sequence.items():
            time = start_time + frame / float(fps)
            time = time * 1000

            key_value_dict = animation_key  # type: dict
            self.animation_generator.add_value_map_in_attribute_map(key_value_dict, time)
            seq_time = max(seq_time, time)

        while end_time > seq_time :
            restart_time = seq_time
            for frame, animation_key in combined_sequence.items():
                time = restart_time + frame / float(fps)
                time = time * 1000
                key_value_dict = animation_key  # type: dict
                self.animation_generator.add_value_map_in_attribute_map(key_value_dict, time)
                seq_time = max(seq_time, time)
