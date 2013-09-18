'''
Created on Sep 04, 2013

@author: fleitner
'''

from sql.interaction_mappingposition import get_all_positions
from sql.interaction_mappingposition import build_block
from data_handling.block import Block
from datetime import datetime, timedelta

def get_blocks():
    blocks = []
    times = []

    mapping_positions = get_all_positions()
    for mapping in mapping_positions:
        start_time = datetime.now()
        block =  build_block(mapping.start_pan, None, mapping.name_strain, mapping.name_sequence, mapping.name_sequence_pan)
        time_needed = datetime.now() - start_time
        print time_needed
        if block.offset != None:
            if block.length > 0:
                blocks.append(block.length)
                times.append(time_needed)

    print "blocks for pan:"
    print "max length: ", max(blocks)
    print "min length: ", min(blocks)
    print "total length: ", sum(blocks)
    print "average length: ", (sum(blocks) / len(blocks))
    print "total blocks: ", len(blocks)
    print "=========================="
    print "max time: ", max(times)
    print "min time: ", min(times)
    print "total: ", sum(times, timedelta())
    print "average time: ", sum(times, timedelta()) / len(times)