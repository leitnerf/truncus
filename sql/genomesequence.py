'''
Created on Sep 12, 2013

@author: fleitner
'''
from sqlalchemy.schema import Column, Sequence
from sqlalchemy.types import Integer, CLOB
from sql import Base


class GenomeSequence(Base):
    __tablename__ = "sequence" 
    
    sequence_id = Column('sequence_id', Integer, Sequence('sequence_seq'), primary_key=True)
    sequence_string = Column('sequence_string', CLOB)
    
    def __init__(self, sequence_string):
        self.sequence_string = sequence_string

    def unique_id(self):
        return self.sequence_id