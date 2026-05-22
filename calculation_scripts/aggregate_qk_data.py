#-----------------------------------------------------------------------------
# IMPORTS
from qMODES import get_QMODES_OUTPUT_DATA_DIR, get_QMODES_PARAMETERS_FILE
from qMODES import get_qk_files_with_date_and_ktot
from qMODES import check_qk_files_have_all_modes, check_qk_files_cover_ktot_range, combine_qk_files_from_list
from qMODES import template_qk_fname

import os
import yaml
import argparse
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# IMPORTING DEFAULT ktot VALUE FROM PARAMETER FILE
with open(get_QMODES_PARAMETERS_FILE(), 'r') as param_file:
    params = yaml.safe_load(param_file)

default_ktot = params['mode_parameters']['nK']

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# READING COMMAND LINE ARGUMENTS USING argparse
parser = argparse.ArgumentParser(description='This script is used to aggregate qk datafiles that are from the same date but cover different k values.')
parser.add_argument('-d','--date', help='Date to comput the qk values for', required=True)
parser.add_argument('--ktot', help='Total number of k values', type=int, default=default_ktot  )
parser.add_argument('--rm_old', help='include to remove old files after creating aggregate file', action='store_true')

args   = parser.parse_args()
date   = args.date
ktot   = args.ktot
rm_old = args.rm_old

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# MAIN 

# Getting all qk files in QMODES_QKDATA_DIR that have date and ktot
# specified from argparse arguments.

ktot_str = "0"*(3-len(str(ktot))) + str(ktot)

file_list = get_qk_files_with_date_and_ktot(date, ktot_str)
combined_outfile = template_qk_fname(get_QMODES_OUTPUT_DATA_DIR(), date) 


# Check if file_list covers all of the k values
cover_ktot_range = check_qk_files_cover_ktot_range(file_list, ktot)
files_have_all_modes = check_qk_files_have_all_modes(file_list)

if cover_ktot_range and files_have_all_modes:
    combine_qk_files_from_list(file_list, combined_outfile)

elif not cover_ktot_range:
    print(f"Not all k values are covered for the date {date}")

elif not files_have_all_modes:
    print("ERROR: all files must contain EIG, WIG, and BAL modes.")

if rm_old:
    print("THE FOLLOWING FILES HAVE BEEN REMOVED:")
    for fname in file_list:
        os.remove(fname)
        print(f"\t{fname}")


#-----------------------------------------------------------------------------
