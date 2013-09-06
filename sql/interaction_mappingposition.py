'''
Created on Aug 28, 2013

@author: fleitner
'''
from sql import DBSession
from sql.mappingposition import MappingPosition
from sqlalchemy import *
from data_handling.block import Block


session = DBSession

#return all mapping positions
def get_all_positions(debug = False):
    query = session.query(MappingPosition).order_by(MappingPosition.name_sequence.asc()).order_by(MappingPosition.name_sequence_pan.asc()).order_by(MappingPosition.start_pan.asc())
    result = query.all()
    if debug:
        print query
    return result

#insert a new position
def insert_position(start_pan, start_strain, name_strain, name_sequence, name_sequence_pan, debug = False):
    if debug:
        print "INSERT: start pangenome: %s, start strain: %s" % (start_pan, start_strain)
    insert_sql = MappingPosition(start_pan, start_strain, name_strain, name_sequence, name_sequence_pan)
    query = session.add(insert_sql)
    if debug:
        print query
    session.commit()

#check if an exact position exists
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

#build a complete block for a given position
def build_block(start_pan, start_strain, strain_name, second_sequence_name, pan_sequence_name, debug = False):
    block_position_start = position_start_block(start_pan, start_strain, strain_name, second_sequence_name, pan_sequence_name)
    block_position_end = position_end_block(start_pan, start_strain, strain_name, second_sequence_name, pan_sequence_name)
    #check if position is an exact match
    exact_position = position_exist(start_pan, start_strain, strain_name, second_sequence_name, pan_sequence_name, debug = False)

    if (block_position_start == None) and (block_position_end == None):
        return None
    elif(block_position_start == None) and (block_position_end != None):
        if (start_pan == None) and (start_strain != None):
            return Block(start_strain, -1, 0, None)
        elif (start_pan != None) and (start_strain == None):
            return Block(start_strain, -1, 0, None)
    elif(block_position_start != None) and (block_position_end == None):
        if (start_pan == None) and (start_strain != None):
            return Block(start_pan, -1, 0, None)
        elif (start_pan != None) and (start_strain == None):
            return Block(start_pan, -1, 0, None)

    if (start_pan == None) and (start_strain != None):
        start = block_position_start.start_strain
        end = block_position_end.start_strain - 1
        length = int(block_position_end.start_strain) - int(block_position_start.start_strain) - 1
        offset = int(block_position_start.start_strain) - int(block_position_start.start_pan)
        if exact_position != None:
            start = start_strain
            length = int(block_position_end.start_strain) - int(start_strain) - 1
            offset = (block_position_start.start_pan - block_position_end.start_strain) * -1
        null_mapping = position_exist(start_pan, start, strain_name, second_sequence_name, pan_sequence_name, debug = False)
        if null_mapping != None:
            if null_mapping.start_pan == -1:
                offset = None
                length = 0
        if start == -1:
            offset = None
            length = 0
    elif (start_pan != None) and (start_strain == None):
        start = block_position_start.start_pan
        end = block_position_end.start_pan - 1
        length = int(block_position_end.start_pan) - int(block_position_start.start_pan) - 1
        offset = int(block_position_start.start_pan) - int(block_position_start.start_strain)
        if exact_position != None:
            start = start_pan
            length = int(block_position_end.start_pan) - int(start_pan) - 1
            offset = int(start_pan) - int(block_position_start.start_strain) - int(exact_position.start_strain) - 1
        #check position maps to -1
        null_mapping = position_exist(start, start_strain, strain_name, second_sequence_name, pan_sequence_name, debug = False)
        if null_mapping != None:
            if null_mapping.start_strain == -1: 
                offset = None
                length = 0
        if start == -1:
            offset = None
            length = 0
    return Block(start, end, length, offset)

#return block start from given location 
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

#return end block from given location 
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

#delete a position
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
    