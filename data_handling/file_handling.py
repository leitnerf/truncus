'''
Created on Aug 28, 2013

@author: fleitner
'''

from data_handling.import_interaction import alignment_handling 
from data_handling.sequence import Sequence

def data_import(file_name, pan_genome_name, strain_name):

    #read alignment_file
    f = open_file(file_name)
    if f == None:
        print "File %s can't be opened." % file_name_alignment
    else:
        pan_sequence = Sequence(pan_genome_name)
        second_sequence = Sequence(strain_name)
        read_file(f, 'alignment', pan_sequence, second_sequence, False)
        close_file(f)

def open_file(file_name):
    try:
        f = open(file_name)
    except:
        return None
    return f

def close_file(f):
    f.close()

#read file line by line
def read_file(f, file_content, pan_sequence, second_sequence, debug = False):
    new_sequence = True
    sequence_data = 0
    for line in f:
        if debug:
            print "%s" % line
        if file_content == 'alignment':
            new_sequence, pan_sequence, second_sequence  = alignment_handling(line, pan_sequence, second_sequence, new_sequence)
