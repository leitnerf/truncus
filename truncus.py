'''
Created on Aug 30, 2013

@author: fleitner
'''


from data_handling.print_data import position_details_strain, position_details_pan, all_positions
from data_handling.file_handling import data_import
from data_handling.sequence import Sequence
from data_handling.data_interaction import get_blocks
from sql.interaction_mappingposition import random_row
from datetime import datetime, timedelta
import sys, getopt, random

def main(argv):
    alignment_file = ''
    print_statistic = False
    random_points = False
    random_length = 0
    count = 0
    times = []
    try:
        opts, args = getopt.getopt(argv, "a:p:s:dr")
    except getopt.GetoptError:
        print "truncus.py -a <alignmentfile> -p pangenome-name -s strain-name -d print some data -r retrieve 1000 random points"
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-a"):
            alignment_file = arg
        elif opt in ("-p"):
            pan_genome_name = arg
        elif opt in ("-s"):
            strain_name = arg
        elif opt in ("-d"):
            print_statistic = True
        elif opt in ("-g"):
            print_statistic = True
        elif opt in ("-r"):
            random_points = True

    if (alignment_file != '') and (pan_genome_name != '') and (strain_name != ''):
        from sql import DBSession
        start_time = datetime.now()
        print "Running Import..."
        data_import(alignment_file, pan_genome_name, strain_name)
        print (datetime.now()-start_time)
        print "=========================="
    elif print_statistic == True:
        start_time = datetime.now()
        #print all position
        print "Listening all Locations..."
        all_positions()
        print (datetime.now()-start_time)
        print "=========================="
        start_time = datetime.now()
        #print block statistic
        print "Getting Statistic..."
        get_blocks()
        print (datetime.now()-start_time)
        print "=========================="
    elif random_points == True:
        how_many_points = 1000
        print "Getting %s random points..." % how_many_points
        while (count < how_many_points):
            start_position, name_strain, name_sequence, name_sequence_pan = random_row()
            random_length = random.randint(0,61)
            position_to_find = start_position + random_length
            start_time = datetime.now()
            position_details_pan(position_to_find, name_strain, name_sequence, name_sequence_pan)
            time_needed = datetime.now() - start_time
            print time_needed
            times.append(time_needed)
            count += 1
        print "max time: ", max(times)
        print "min time: ", min(times)
        print "total: ", sum(times, timedelta())
        print "average time: ", sum(times, timedelta()) / len(times)

if __name__ == "__main__":
   main(sys.argv[1:])
