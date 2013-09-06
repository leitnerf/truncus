'''
Created on Aug 27, 2013

@author: fleitner
'''
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from sql import Base


class MappingPosition(Base):
    __tablename__ = "mappingposition" 
    
    start_pan = Column('start_pan', Integer, primary_key=True)
    start_strain = Column('start_strain', Integer, primary_key=True)
    name_strain = Column('name_strain', String, primary_key=True)
    name_sequence = Column('name_sequence', String, primary_key=True)
    name_sequence_pan = Column('name_sequence_pan', String, primary_key=True)
    
    def __init__(self, start_pan, start_strain, name_strain, name_sequence, name_sequence_pan):
        self.start_pan = start_pan
        self.start_strain = start_strain
        self.name_strain = name_strain
        self.name_sequence = name_sequence
        self.name_sequence_pan = name_sequence_pan
        
