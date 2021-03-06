'''
Created on Aug 29, 2013

@author: fleitner
'''

class Sequence:

    def __init__(self, strain_name):
        self.strain_name = strain_name

    def set_attributes(self, sequence_name, start, length, compliment_reverse, sequence_string, total_length):
        self.sequence_name = sequence_name
        self.start = start
        self.end = eval(start) + eval(length) - 1
        self.length = length
        self.compliment_reverse = compliment_reverse
        self.sequence_string = sequence_string
        self.total_length = total_length

    @property
    def length(self):
        return self.__length

    @property
    def start(self):
        return self.__start

    @property
    def strain_name(self):
        return self.__strain_name

    @property
    def sequence_name(self):
        return self.__sequence_name

    @property
    def end(self):
        return self.__end

    @property
    def compliment_reverse(self):
        return self.__compliment_reverse

    @property
    def sequence(self):
        return self.__sequence

    @property
    def total_length(self):
        return self.__total_length

    @property
    def sequence_string(self):
        return self.__sequence_string

    @start.setter
    def start(self, value):
        self._start = value

    @length.setter
    def length(self, value):
        self._length = value

    @end.setter
    def length(self, value):
        self._end = value

    @sequence_string.setter
    def sequence_string(self, value):
        self._sequence_string = value