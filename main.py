'''
Created on Aug 30, 2013

@author: fleitner
'''


from data_handling.print_data import position_details_strain, position_details_pan, all_positions
from data_handling.file_handling import open_file, close_file, read_file
from data_handling.sequence import Sequence

file_name_alignment = '../truncus/alignment_data/s288c_w303_generic.maf.txt'

#read alignment_file
f = open_file(file_name_alignment)
if f == None:
    print "File %s can't be opened." % file_name_alignment
else:
    pan_sequence = Sequence('S288C')
    second_sequence = Sequence('W303')
    read_file(f, 'alignment', pan_sequence, second_sequence, False)
    close_file(f)


#print some things
all_positions()
position_details_strain(19, 'W303', 'scaffold-0', 'chrVII')
position_details_pan(17, 'W303', 'scaffold-0', 'chrVII')