'''
Created on Sep 04, 2013

@author: fleitner
'''


from data_handling.block import Block
from sql.interaction_mappingposition import build_block, get_all_positions

def position_details_strain (position, strain_name, second_sequence_name, pan_sequence_name):
    block =  build_block(None, position, strain_name, second_sequence_name, pan_sequence_name)
    print "Position on strain: %i" % position
    if block != None:
        print "Start block strain: %s" % block.start
        print "End block strain: %s" % block.end
        print "Length of block: %s" % block.length
        if block.offset == None:
            print "Position on pan: -1" 
        else:
            print "Offset: %s" % block.offset
            print "Position on pan: %s" % (position - block.offset)
    else:
        print "Not found."
    print "========================================"

def position_details_pan (position, strain_name, second_sequence_name, pan_sequence_name):
    block =  build_block(position, None,  strain_name, second_sequence_name, pan_sequence_name)
    print "Position on pan genome: %i" % position
    if block != None:
        print "Start block pan: %s" % block.start
        print "End block pan: %s" % block.end
        print "Length of block: %s" % block.length
        if block.offset == None:
            print "Position on strain: -1" 
        else:
            print "Offset: %s" % block.offset
            print "Position on strain: %s" % (position - block.offset)
    else:
        print "Not found."
    print "========================================"

def all_positions():
    row_count = 0
    mapping_positions = get_all_positions()
    for mapping in mapping_positions:
        row_count += 1
        print "pangenome: %s, strain: %s, name-strain: %s, name-sequence: %s, name-sequence-pan: %s" % (mapping.start_pan, mapping.start_strain, mapping.name_strain, mapping.name_sequence, mapping.name_sequence_pan)
    print "Total rows: %i" % row_count
    print "========================================"