'''
Created on Sep 05, 2013

@author: fleitner
'''

class Block:

    def __init__(self, start, end, length, offset):
        self.start = start
        self.end = end
        self.length = length
        self.offset = offset

    @property
    def start(start):
        return self.__start

    @property
    def total_length(end):
        return self.__end

    @property
    def total_length(length):
        return self.__lengtht

    @property
    def total_length(offset):
        return self.__offset
