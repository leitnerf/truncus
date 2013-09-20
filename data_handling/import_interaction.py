'''
Created on Aug 28, 2013

@author: fleitner
'''

from sql.interaction_mappingposition import insert_position, delete_position, position_start_block, position_end_block, position_exist, build_block, encase_block
from sql.interaction_sequence import insert_sequence
from sql.genomesequence import GenomeSequence
from data_handling.sequence import Sequence
import difflib


#find the longest common substring of two sequences
def longest_common_substring(s1, s2):
    #can not be used in Python 2.6. to find lcs - see SequenceMatcher Automatic junk heuristic
    #match = difflib.SequenceMatcher(None, a, b)
    #a_start, b_start, length = match.find_longest_match(0, len(a), 0, len(b))

    #http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring
    #very slow
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest, y_longest = 0, 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
          if s1[x - 1] == s2[y - 1]:
              m[x][y] = m[x - 1][y - 1] + 1
              if m[x][y] > longest:
                  longest = m[x][y]
                  x_longest = x
                  y_longest = y
          else:
              m[x][y] = 0
    return (x_longest - longest), (y_longest - longest), longest


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
            if (pan_sequence.length == second_sequence.length) and (pan_sequence.sequence_string == second_sequence.sequence_string) and (pan_sequence.compliment_reverse == '+') and (second_sequence.compliment_reverse == '+') :
                insert_sequence_pos(pan_sequence, second_sequence)         
            #TO-DO: two sequences are aligned but at least one of them is having a deletion, gap, compliment reverse,...; see special_cases.txt
            else:
                #sequence_mismatch()
                #if data does not align perfectly find the longest common substring between two sequences to generate some data
                start_pan_lcs, start_second_lcs, length_lcs = longest_common_substring(pan_sequence.sequence_string, second_sequence.sequence_string)
                pan_sequence.start = int(pan_sequence.start) + start_pan_lcs
                pan_sequence.length = length_lcs
                pan_sequence.end = pan_sequence.start + length_lcs - 1
                second_sequence.start = int(second_sequence.start) + start_second_lcs
                second_sequence.length = length_lcs
                second_sequence.end = second_sequence.start + length_lcs - 1
                pan_sequence.sequence_string = pan_sequence.sequence_string[start_pan_lcs : start_pan_lcs  + length_lcs]
                second_sequence.sequence_string = second_sequence.sequence_string[start_second_lcs : start_second_lcs  + length_lcs]
                insert_sequence_pos(pan_sequence, second_sequence) 
            #check if beginning of pan sequence is mapped -> map position 0 to -1
            check_mapping_sequence_start(pan_sequence, second_sequence)
            #check if end of pan sequence is mapped -> map end position to -1
            check_mapping_sequence_end(pan_sequence, second_sequence)
            new_sequence = True
    return new_sequence, pan_sequence, second_sequence

#check if the end of a sequence is mapped
def check_mapping_sequence_end(pan_sequence, second_sequence):
    last_position = int(pan_sequence.total_length) + 1
    block_position_end = position_end_block(last_position, None, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)
    if block_position_end == None:
        insert_position(last_position, '-1', second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)    

#check if the start of a sequence is mapped
def check_mapping_sequence_start(pan_sequence, second_sequence):
    block_position_start = position_exist(0, None, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)
    if block_position_start == None:
        insert_position('0', '-1', second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)    

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
    sequence_id = ''
    #check if blocks exist with the given position in pan genome, strain
    #get block from strain position
    block_strain = build_block(None, second_sequence.start, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)
    #get block from pan position
    block_pan = build_block(pan_sequence.start, None, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)

    block_encase_pan = encase_block(pan_sequence.start, None, pan_sequence.end, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)
    block_encase_strain = encase_block(None, second_sequence.start, second_sequence.end, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)

    if (block_encase_pan != None) or (block_encase_strain != None):
        print "encase %s, %s, %s, %s, %s" % (pan_sequence.start, second_sequence.start, second_sequence.length, pan_sequence.length, pan_sequence.sequence_string)
    elif (block_strain == None) and (block_pan == None):
        sequence_id = insert_sequence(pan_sequence, second_sequence)
        insert_position(pan_sequence.start, second_sequence.start, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name, sequence_id)
        #map end from pan -> strain
        check_end_block_surrounding(pan_sequence, second_sequence)
        #map end from strain -> pan        
        check_end_block_surrounding_strain(pan_sequence, second_sequence)
    elif (block_strain.length == 0) and (block_pan.length == 0):
        sequence_id = insert_sequence(pan_sequence, second_sequence)
        insert_position(pan_sequence.start, second_sequence.start, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name, sequence_id)
        #map end from pan -> strain
        check_end_block_surrounding(pan_sequence, second_sequence)
        #map end from strain -> pan        
        check_end_block_surrounding_strain(pan_sequence, second_sequence)

#check if starting block connects to an ending block. if not insert '-1 positions' 
def check_start_block_surrounding(pan_sequence, second_sequence):
    start = int(pan_sequence.start) - 1
    if start > 0:
        start_block = position_start_block(start, None, second_sequence.strain_name, pan_sequence.sequence_name, second_sequence.sequence_name)
        if start_block == None:
            insert_position(start, '-2', second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)

#check if ending block connects to an starting block. if not insert '-1 positions' 
def check_end_block_surrounding(pan_sequence, second_sequence):
    start = pan_sequence.end + 1
    total_length = int(pan_sequence.total_length)
    if start < total_length:
        start_block = position_end_block(start, None, second_sequence.strain_name, pan_sequence.sequence_name, second_sequence.sequence_name)
        if start_block == None:
            insert_position(start, '-1', second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)
    #the end of the sequence is reached
    elif start > total_length:
        start_block = position_end_block(start, None, second_sequence.strain_name, pan_sequence.sequence_name, second_sequence.sequence_name)
        if start_block == None:
            #'-1' should we mark the end of a sequence differently?
            insert_position(start, '-1', second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)

#check if ending block connects to an starting block. if not insert '-1 positions' 
def check_end_block_surrounding_strain(pan_sequence, second_sequence):
    start = second_sequence.end + 1
    total_length = int(second_sequence.total_length)
    if start < total_length:
        start_block = position_end_block(None, start, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)
        if start_block == None:
            insert_position('-1', start, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)
    #the end of the sequence is reached
    elif start >= total_length:
        start_block = position_end_block(None, start, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)
        if start_block == None:
            #'-1' should we mark the end of a sequence differently?
            insert_position('-1', start, second_sequence.strain_name, second_sequence.sequence_name, pan_sequence.sequence_name)

#length mismatch from maf file but two sequences are still aligned
#def sequence_mismatch():
#    print "MISMATCH"

#remove whitespace from a given string
def remove_whitespace(pieces):
    sanitized_line = []
    for piece in pieces:
        if piece != '':
          sanitized_line.append(piece)
    return sanitized_line
