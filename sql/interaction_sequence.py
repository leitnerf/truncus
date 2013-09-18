'''
Created on Sep 12, 2013

@author: fleitner
'''
from sql import DBSession
from sql.genomesequence import GenomeSequence
from data_handling.sequence import Sequence
from sqlalchemy import *


session = DBSession

#insert sequence
def insert_sequence(pan_sequence, second_sequence, debug = False):
    insert_sql = GenomeSequence(pan_sequence.sequence_string)
    query = session.add(insert_sql)
    if debug:
        print query
    session.commit()
    return insert_sql.unique_id()

#get sequence
def get_sequence(sequence_id, debug = False):
    query = session.query(GenomeSequence).filter(GenomeSequence.sequence_id == sequence_id)
    if debug:
        print query
    result = query.first()
    return result