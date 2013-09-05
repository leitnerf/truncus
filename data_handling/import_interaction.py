'''
Created on Aug 28, 2013

@author: fleitner
'''

from sql.interaction_mappingposition import insert_position, delete_position, position_start_block, position_end_block
from data_handling.sequence import Sequence

#read alignment file (maf file format) and process data
def alignment_handling(line, pan_sequence, second_sequence, new_sequence, debug = False):
    if line.startswith('s'):
        #check if the first or second sequence is processed
        if new_sequence:
            pan_sequence = split_sequence_line(line, pan_sequence)
            new_sequence = False
        else:
            second_sequence = split_sequence_line(line, second_sequence)
            #TO-DO: check for gaps, etc.: sequences will only be checked for same length; if both sequences have the same
            #amount of e.g. gaps, etc they still will be stored! 
            #also '-' is not included in the length of an alignment; see special_cases.txt
            if (pan_sequence.length == second_sequence.length) and (pan_sequence.sequence == second_sequence.sequence) and (pan_sequence.compliment_reverse == '+') and (second_sequence.compliment_reverse == '+') :
                insert_sequence_pos(pan_sequence, second_sequence)         
            #TO-DO: two sequences are aligned but at least one of them is having a deletion, gap, compliment reverse,...; see special_cases.txt
            else:
                sequence_mismatch()
            #check if beginning of sequence is mapped -> map position 0 to -1
            check_mapping_sequence_start(pan_sequence, second_sequence)
            #TO-DO: check if end of sequence is mapped -> map position x to -3 and remove last position which is mapped to -1
            #check_mapping_sequence_end(pan_sequence, second_sequence)
            new_sequence = True
    return new_sequence, pan_sequence, second_sequence

#check if the start of a sequence is mapped
def check_mapping_sequence_start(pan_sequence, second_sequence):
    block_position_start = position_start_block(0, None, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)
    if block_position_start == None:
        insert_position(0, '-1', second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)    

#get alignment block data from maf file
def split_sequence_line(line, sequence):
    #pieces = line.strip().split('\t')
    pieces = line.strip().split(' ')
    pieces =  remove_whitespace(pieces)
    sequence_name = pieces[1]
    alignment_start = pieces[2]
    alignment_length = pieces[3]
    compliment_reverse_alignment = pieces[4]
    sequence_string = pieces[6]
    total_length = pieces[5]
    sequence.set_attributes(sequence_name, alignment_start, alignment_length, compliment_reverse_alignment, sequence_string, total_length)
    return sequence

#check if mapping already exist and insert into db
def insert_sequence_pos(pan_sequence, second_sequence):
    #check if blocks exist with the given position in pan genome (also in strain?)
    block_position_start = position_start_block(pan_sequence.start, None, second_sequence.strain_name, pan_sequence.sequence_name, second_sequence.sequence_name) 
    block_position_end = position_end_block(pan_sequence.start, None, second_sequence.strain_name, pan_sequence.sequence_name, second_sequence.sequence_name)

    insert_position(pan_sequence.start, second_sequence.start, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)

    print "SAVE"
    #check_start_block_surrounding(pan_sequence, second_sequence)
    check_end_block_surrounding(pan_sequence, second_sequence)

#check if starting block connects to an ending block. if not insert '-1 positions' 
def check_start_block_surrounding(pan_sequence, second_sequence):
    start = eval(pan_sequence.start) - 1
    if start > 0:
        start_block = position_start_block(start, None, second_sequence.strain_name, pan_sequence.sequence_name, second_sequence.sequence_name)
        if start_block == None:
            insert_position(start, '-2', second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)

#check if ending block connects to an starting block. if not insert '-1 positions' 
def check_end_block_surrounding(pan_sequence, second_sequence):
    start = pan_sequence.end + 1
    total_length = eval(pan_sequence.total_length)
    if start < total_length:
        start_block = position_end_block(start, -1, second_sequence.strain_name, pan_sequence.sequence_name, second_sequence.sequence_name)
        if start_block == None:
            insert_position(start, '-1', second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)
    elif start > total_length:
        start_block = position_end_block(start, -1, second_sequence.strain_name, pan_sequence.sequence_name, second_sequence.sequence_name)
        if start_block == None:
            #'-3' marks the end of a sequence
            insert_position(start, '-3', second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)

#length mismatch from maf file but two sequences are still aligned
def sequence_mismatch():
    print "MISMATCH"

#remove whitespace from a given string
def remove_whitespace(pieces):
    sanitized_line = []
    for piece in pieces:
        if piece != '':
          sanitized_line.append(piece)
    return sanitized_line
