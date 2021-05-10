from xml.etree.ElementTree import Element, SubElement, dump, ElementTree
import blending

def generate_output_file_in_speech_and_emotion(speech_animation, emotion_animation, audio_size, fps, input_gender, input_hair, min_m, max_m, pitch_info, emotion_strengths):
    relation_of_m_x, relation_of_m_y = blending.calculating_relation(min_m, max_m)
    _animation = Element("animation")
    _animation.attrib["name"] = "speech_emotion_animation"
    gender = Element("gender")
    gender.attrib["gender"] = input_gender
    _animation.append(gender)
    hair_model = Element("hair_model")
    hair_model.attrib["hair_model"] = input_hair
    _animation.append(hair_model)
    _emotion_strengths = Element("emotion_strength")
    for key, value in emotion_strengths.items():
        emotion = SubElement(_emotion_strengths, "emotion")
        emotion.attrib["emotion"] = str(key)
        emotion.attrib["strength"] = str(value)
    _animation.append(_emotion_strengths)
    keyframe_list = Element("keyframe_list")
    _animation.append(keyframe_list)

    # key is 0
    key = Element("key")
    key.attrib["t"] = str(0)
    keyframe_list.append(key)
    ordered_bs_weight = ""
    speech_coeff_animation = blending.calculating_speech_coefficient(relation_of_m_x, relation_of_m_y, 0)
    for bs_name in emotion_animation.ordered_bs_list:
        ordered_bs_weight = blending.blending_emotion_and_speech(ordered_bs_weight, bs_name, emotion_animation, speech_animation, 0, speech_coeff_animation)
    face_weights = Element("face_weights")
    face_weights.text = ordered_bs_weight
    key.append(face_weights)
    # head nodding
    ordered_hn_weight = ""
    ordered_hn_weight = pitch_info.nodding_interp(0)
    head_nodding_weights = Element("headNodding")
    head_nodding_weights.text = ordered_hn_weight
    key.append(head_nodding_weights)

    for i in range(0, (int)(audio_size), (int)(1000 / fps)):
        if i == 0:
            continue
        # key is greater than 0
        sub_key = SubElement(keyframe_list, "key")
        sub_key.attrib["t"] = str(i)
        speech_coeff_animation = blending.calculating_speech_coefficient(relation_of_m_x, relation_of_m_y, speech_animation.get_value_from_time_in_attribute('M', i))
        ordered_bs_weight = ""
        for bs_name in emotion_animation.ordered_bs_list:
            ordered_bs_weight = blending.blending_emotion_and_speech(ordered_bs_weight, bs_name, emotion_animation, speech_animation, i, speech_coeff_animation)
        face_weights = Element("face_weights")
        face_weights.text = ordered_bs_weight
        sub_key.append(face_weights)
        # head nodding
        ordered_hn_weight = ""
        ordered_hn_weight = pitch_info.nodding_interp(i)
        head_nodding_weights = Element("headNodding")
        head_nodding_weights.text = ordered_hn_weight
        sub_key.append(head_nodding_weights)

    def indent(elem, level=0):
        i = "\n" + level * "	"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "	"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    indent(_animation)
    dump(_animation)
    ElementTree(_animation).write("animation_data.xml", encoding='utf-8', xml_declaration=True)

def generate_output_file_in_speech(animation, audio_size, fps, input_gender, input_hair, pitch_info, emotion_strengths):
    _animation = Element("animation")
    _animation.attrib["name"] = "speech_animation"
    gender = Element("gender")
    gender.attrib["gender"] = input_gender
    _animation.append(gender)
    hair_model = Element("hair_model")
    hair_model.attrib["hair_model"] = input_hair
    _animation.append(hair_model)
    _emotion_strengths = Element("emotion_strength")
    for key, value in emotion_strengths.items():
        emotion = SubElement(_emotion_strengths, "emotion")
        emotion.attrib["emotion"] = str(key)
        emotion.attrib["strength"] = str(value)
    _animation.append(_emotion_strengths)
    keyframe_list = Element("keyframe_list")
    _animation.append(keyframe_list)
    key = Element("key")
    key.attrib["t"] = str(0)
    keyframe_list.append(key)
    ordered_bs_weight = ""
    for bs_name in animation.ordered_bs_list:
        if bs_name in animation.attr_list:
            ordered_bs_weight = ordered_bs_weight + str(animation.get_value_from_time_in_attribute(bs_name, 0)) + " "
        else:
            ordered_bs_weight = ordered_bs_weight + "0.0 "
    face_weights = Element("face_weights")
    face_weights.text = ordered_bs_weight
    key.append(face_weights)
    # head nodding
    ordered_hn_weight = pitch_info.nodding_interp(0)
    head_nodding_weights = Element("headNodding")
    head_nodding_weights.text = ordered_hn_weight
    key.append(head_nodding_weights)
    # key is greater than 0
    for i in range(0, (int)(audio_size), (int)(1000 / fps)):
        if i is 0:
            continue
        sub_key = SubElement(keyframe_list, "key")
        sub_key.attrib["t"] = str(i)
        ordered_bs_weight = ""
        for bs_name in animation.ordered_bs_list:
            if bs_name in animation.attr_list:
                ordered_bs_weight = ordered_bs_weight + str(animation.get_value_from_time_in_attribute(bs_name, i)) + " "
            else:
                ordered_bs_weight = ordered_bs_weight + "0.0 "
        face_weights = Element("face_weights")
        face_weights.text = ordered_bs_weight
        sub_key.append(face_weights)
        # head nodding
        ordered_hn_weight = pitch_info.nodding_interp(i)
        head_nodding_weights = Element("headNodding")
        head_nodding_weights.text = ordered_hn_weight
        sub_key.append(head_nodding_weights)

    def indent(elem, level=0):
        i = "\n" + level * "	"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "	"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    indent(_animation)
    dump(_animation)
    ElementTree(_animation).write("animation_data.xml", encoding='utf-8', xml_declaration=True)
    