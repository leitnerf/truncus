'''
Created on Aug 30, 2013

@author: fleitner
'''


from data_handling.print_data import position_details_strain, position_details_pan, all_positions
from data_handling.file_handling import data_import
from data_handling.sequence import Sequence
from data_handling.data_interaction import get_blocks
from datetime import datetime
import sys, getopt

def main(argv):
    alignment_file = ''
    try:
        opts, args = getopt.getopt(argv, "a:p:s:")
    except getopt.GetoptError:
        print "truncus.py -a <alignmentfile> -p pangenome-name -s strain-name "
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-a"):
            alignment_file = arg
        elif opt in ("-p"):
            pan_genome_name = arg
        elif opt in ("-s"):
            strain_name = arg
    if (alignment_file != '') and (pan_genome_name != '') and (strain_name != ''):
        from sql import DBSession

        start_time = datetime.now()
        print "Running Import..."
        data_import(alignment_file, pan_genome_name, strain_name)
        print (datetime.now()-start_time)
        print "=========================="

        start_time = datetime.now()
        #print all position
        print "Listening all Locations..."
        all_positions()
        print (datetime.now()-start_time)
        print "=========================="

        #position_details_strain(5, 'W303', 'scaffold-0', 'chrVII')
        #position_details_pan(10, 'W303', 'scaffold-0', 'chrVII')
        start_time = datetime.now()

        #print block statistic
        print "Getting Statistic..."
        get_blocks()
        print (datetime.now()-start_time)
        print "=========================="

if __name__ == "__main__":
   main(sys.argv[1:])
