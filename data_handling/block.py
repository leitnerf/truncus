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
    def end(end):
        return self.__end

    @property
    def length(length):
        return self.__length

    @property
    def offset(offset):
        return self.__offset
