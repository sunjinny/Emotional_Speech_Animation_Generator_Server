import numpy as np

# save in milliseconds
class Animation:
    def __init__(self, blendshape_list_path):
        self.attr_list = {}
        self.ordered_bs_list = list()
        self.bs_part = dict()
        data = open(blendshape_list_path)
        for bs in data.read().split():
            part = bs.split(',')
            self.bs_part[part[1]] = part[0]
            self.ordered_bs_list.append(part[1])

    def create_attribute(self, attribute_name):
        if attribute_name in self.attr_list:
            print("Already exited attribute.")
        else:
            self.attr_list[attribute_name] = Attribute(attribute_name)

    def add_value_in_attribute(self, attribute_name, time, value):
        if attribute_name in self.attr_list:
            self.attr_list[attribute_name].add_point(time, value)
        else:
            self.create_attribute(attribute_name)
            self.attr_list[attribute_name].add_point(time, value)

    def add_value_map_in_attribute_map(self, attribute_value_map, time):
        for attribute, vlaue in zip(attribute_value_map.keys(), attribute_value_map.values()):
            self.add_value_in_attribute(attribute, time, vlaue)

    def delete_value_in_attribute(self, attribute_name, time):
        if attribute_name in self.attr_list:
            self.attr_list[attribute_name].delete_point(time)
        else:
            print("Invalid. First create the attribute.")
            print(self.attr_list)

    def get_value_from_time_in_attribute(self, attribute_name, access_time):
        if attribute_name in self.attr_list:
            return self.attr_list[attribute_name].get_value(access_time)
        return 0


class Attribute:
    def __init__(self, name):
        self.name = name
        self.dict = {}

    def __is_empty(self):
        return self.dict.__len__() == 0

    def __is_close(self, close_time, input_time, rel_tol=1e-09, abs_tol=0.0):
        return (abs(close_time - input_time) <= max(rel_tol * max(abs(close_time), abs(input_time)), abs_tol)), \
               close_time

    def __is_in(self, input_time):
        if self.__is_empty():
            return False, input_time
        close_time  = input_time if input_time in self.dict \
            else min(self.dict.keys(), key=lambda k: abs(k - input_time))
        return self.__is_close(close_time, input_time)

    def add_point(self, time, value):
        check, close_time = self.__is_in(time)
        if check:
            self.dict[close_time] = value
        else:
            self.dict[time] = value

    def delete_point(self, time):
        if self.__is_empty():
            print("Cannot delete. Empty point attribute. Please first add the point.")
            return
        check, close_time = self.__is_in(time)
        if check:
            del self.dict[close_time]
        else:
            print("There is not the time in attribute.")
            print("The nearest point is ", close_time)

    def get_value(self, access_time):
        if self.__is_empty():
            print("Empty point attribute. Please first add the point.")
            return 0
        check, close_time = self.__is_in(access_time)
        if check:
            return self.dict[close_time]
        sorted_keys = sorted(self.dict)
        sorted_values_by_key = []
        for key in sorted_keys:
            sorted_values_by_key.append(self.dict[key])
        return np.interp(access_time, sorted_keys, sorted_values_by_key)

    def print_all_point(self):
        print(self.name + " : ")
        print(self.dict)
