'''
Created on Aug 28, 2013

@author: fleitner
'''
from sql import DBSession
from sql.mappingposition import MappingPosition
from sqlalchemy import *
from data_handling.block import Block


session = DBSession

def get_all_positions(debug = False):
    query = session.query(MappingPosition).order_by(MappingPosition.start_pan.asc())
    result = query.all()
    if debug:
        print query
    return result

def insert_position(start_pan, start_strain, name_strain, name_sequence, name_sequence_pan, debug = False):
    if debug:
        print "INSERT: start pangenome: %s, start strain: %s" % (start_pan, start_strain)
    insert_sql = MappingPosition(start_pan, start_strain, name_strain, name_sequence, name_sequence_pan)
    query = session.add(insert_sql)
    if debug:
        print query
    session.commit()

def position_exist(start_pan, start_strain, name_strain, name_sequence, name_sequence_pan, debug = False):
    #check if exact position exists
    if (start_pan != None) and (start_strain != None):
        query = session.query(MappingPosition).filter(MappingPosition.start_pan==start_pan).filter(MappingPosition.start_strain==start_strain).filter(MappingPosition.name_strain==name_strain).filter(MappingPosition.name_sequence==name_sequence).filter(MappingPosition.name_sequence_pan==name_sequence_pan)
    #check if given position in strain exist
    elif (start_pan == None) and (start_strain != None):
        query = session.query(MappingPosition).filter(MappingPosition.start_strain==start_strain).filter(MappingPosition.name_strain==name_strain).filter(MappingPosition.name_sequence==name_sequence).filter(MappingPosition.name_sequence_pan==name_sequence_pan)
    #check if given position in pan genome exist
    elif (start_pan != None) and (start_strain == None):    
        query = session.query(MappingPosition).filter(MappingPosition.start_pan==start_pan).filter(MappingPosition.name_strain==name_strain).filter(MappingPosition.name_sequence==name_sequence).filter(MappingPosition.name_sequence_pan==name_sequence_pan)
    else:
        return None
    if debug:
        print query
    result = query.first()
    return result

def build_block(start_pan, start_strain, strain_name, second_sequence_name, pan_sequence_name, debug = False):
    block_position_start = position_start_block(start_pan, start_strain, strain_name, second_sequence_name, pan_sequence_name)
    block_position_end = position_end_block(start_pan, start_strain, strain_name, second_sequence_name, pan_sequence_name)
    #check if position is an exact match
    exact_position = position_exist(start_pan, start_strain, strain_name, second_sequence_name, pan_sequence_name, debug = False)
    if (block_position_start == None) or (block_position_end == None):
        return None

    if (start_pan == None) and (start_strain != None):
        start = block_position_start.start_strain
        end = block_position_end.start_strain - 1
        length = block_position_end.start_strain - block_position_start.start_strain - 1
        offset = block_position_start.start_strain - block_position_start.start_pan - 1
        if exact_position != None:
            start = start_strain
            length = block_position_end.start_strain - start_strain
            offset = start_strain
        null_mapping = position_exist(start_pan, start, strain_name, second_sequence_name, pan_sequence_name, debug = False)
        if null_mapping != None:
            if null_mapping.start_pan == -1:
                offset = None
    elif (start_pan != None) and (start_strain == None):
        start = block_position_start.start_pan
        end = block_position_end.start_pan - 1
        length = block_position_end.start_pan - block_position_start.start_pan - 1
        offset = block_position_start.start_pan - block_position_start.start_strain
        #check position maps to -1
        if exact_position != None:
            start = start_pan
            length = block_position_end.start_pan - start_pan - 1
            offset = start_pan
        null_mapping = position_exist(start, start_strain, strain_name, second_sequence_name, pan_sequence_name, debug = False)
        if null_mapping != None:
            if null_mapping.start_strain == -1:
                offset = None
    return Block(start, end, length, offset)

#check return start location of block from given location 
def position_start_block(start_pan, start_strain, name_strain, name_sequence, name_sequence_pan, debug = False):
    if (start_pan == None) and (start_strain != None):
        query = session.query(MappingPosition).order_by(MappingPosition.start_strain.desc()).filter(MappingPosition.start_strain<start_strain).filter(MappingPosition.name_strain==name_strain).filter(MappingPosition.name_sequence==name_sequence).filter(MappingPosition.name_sequence_pan==name_sequence_pan)
    elif (start_pan != None) and (start_strain == None):
        query = session.query(MappingPosition).order_by(MappingPosition.start_pan.desc()).filter(MappingPosition.start_pan<start_pan).filter(MappingPosition.name_strain==name_strain).filter(MappingPosition.name_sequence==name_sequence).filter(MappingPosition.name_sequence_pan==name_sequence_pan)
    else:
        return None
    if debug:
        print query
    result = query.first()
    return result

#check return end location of block from given location 
def position_end_block(start_pan, start_strain, name_strain, name_sequence, name_sequence_pan, debug = False):
    if (start_pan == None) and (start_strain != None):
        query = session.query(MappingPosition).order_by(MappingPosition.start_strain.asc()).filter(MappingPosition.start_strain>start_strain).filter(MappingPosition.name_strain==name_strain).filter(MappingPosition.name_sequence==name_sequence).filter(MappingPosition.name_sequence_pan==name_sequence_pan)
    elif (start_pan != None) and (start_strain == None):
        query = session.query(MappingPosition).order_by(MappingPosition.start_pan.asc()).filter(MappingPosition.start_pan>start_pan).filter(MappingPosition.name_strain==name_strain).filter(MappingPosition.name_sequence==name_sequence).filter(MappingPosition.name_sequence_pan==name_sequence_pan)
    else:
        return None
    if debug:
        print query
    result = query.first()
    return result

def delete_position(start_pan, start_strain, name_strain, name_sequence, name_sequence_pan, debug = False):
    if debug:
        print "DELETE: start pangenome: %s, start strain: %s" % (start_pan, start_strain)
    if (start_pan != None) and (start_strain != None):
        query = session.query(MappingPosition).filter(MappingPosition.start_pan==start_pan).filter(MappingPosition.start_strain==start_strain).filter(MappingPosition.name_strain==name_strain).filter(MappingPosition.name_sequence==name_sequence).filter(MappingPosition.name_sequence_pan==name_sequence_pan)
    elif (start_pan != None) and (start_strain == None):
        query = session.query(MappingPosition).filter(MappingPosition.start_pan==start_pan).filter(MappingPosition.name_strain==name_strain).filter(MappingPosition.name_sequence==name_sequence).filter(MappingPosition.name_sequence_pan==name_sequence_pan)
    elif (start_pan == None) and (start_strain != None):
        query = session.query(MappingPosition).filter(MappingPosition.start_strain==start_strain).filter(MappingPosition.name_strain==name_strain).filter(MappingPosition.name_sequence==name_sequence).filter(MappingPosition.name_sequence_pan==name_sequence_pan)

    if debug:
        print query
    result = query.delete()
    