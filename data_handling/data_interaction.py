'''
Created on Sep 04, 2013

@author: fleitner
'''

from sql.interaction_mappingposition import get_all_positions
from sql.interaction_mappingposition import build_block
from data_handling.block import Block


def get_blocks():
    blocks = []

    mapping_positions = get_all_positions()
    for mapping in mapping_positions:
        block =  build_block(mapping.start_pan, None, mapping.name_strain, mapping.name_sequence, mapping.name_sequence_pan)
        if block.offset != None:
            if block.length > 0:
                blocks.append(block.length)

    print "max length: ", max(blocks)
    print "min length: ", min(blocks)
    print "average length: ", (sum(blocks) / len(blocks))
    print "total blocks: ", len(blocks)