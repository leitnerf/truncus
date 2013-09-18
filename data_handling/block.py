'''
Created on Sep 05, 2013

@author: fleitner
'''

class Block:

    def __init__(self, start, end, length, offset, sequence_id = 0):
        self.start = start
        self.end = end
        self.length = length
        self.offset = offset
        self.sequence_id = sequence_id

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def length(self):
        return self.__length

    @property
    def offset(self):
        return self.__offset

    @property
    def sequence_id(self):
        return self.__sequence_id

    @sequence_id.setter
    def sequence_id(self, value):
        self._sequence_id = value