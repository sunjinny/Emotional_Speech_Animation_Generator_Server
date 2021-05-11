def calculating_relation(min_m, max_m):
    if min_m == 0 and max_m == 0:
        return 0, 0.5
    if (min_m - max_m) == 0:
        x = 0
    else:
        x = -0.4 / (min_m - max_m)
    y = 1 - (max_m * x)
    return x, y

def calculating_speech_coefficient(x, y, m):
    return (m * x) + y

def blending_emotion_and_speech(ordered_bs_weight,
                                bs_name,
                                emotion_animation,
                                speech_animation,
                                time,
                                speech_coeff_animation):
    if emotion_animation.bs_part[bs_name] == 'eye':
        if bs_name in emotion_animation.attr_list:
            ordered_bs_weight = ordered_bs_weight + \
                                str(emotion_animation.get_value_from_time_in_attribute(bs_name, time))\
                                + " "
        else:
            ordered_bs_weight = ordered_bs_weight + "0.0 "
    else:
        current_bs_weight = 0
        if bs_name in emotion_animation.attr_list:
            current_bs_weight = current_bs_weight + \
                                emotion_animation.get_value_from_time_in_attribute(bs_name, time) \
                                * (1 - speech_coeff_animation)
        else:
            current_bs_weight = 0.0
        if bs_name in speech_animation.attr_list:
            current_bs_weight = current_bs_weight + \
                                speech_animation.get_value_from_time_in_attribute(bs_name, time) \
                                * speech_coeff_animation
        else:
            current_bs_weight = current_bs_weight + 0.0
        ordered_bs_weight = ordered_bs_weight + str(current_bs_weight) + " "

    return ordered_bs_weight
