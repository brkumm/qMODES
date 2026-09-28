#-----------------------------------------------------------------------------
# IMPORTS
from qMODES import load_qmodes_config
from qMODES import get_qmodes_files_with_date_and_ktot, combine_qmodes_files_from_list
from qMODES import check_qmodes_files_have_all_modes, check_qmodes_files_cover_ktot_range 

import os
import argparse
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# READING COMMAND LINE ARGUMENTS USING argparse
parser = argparse.ArgumentParser(description='This script is used to aggregate qmodes datafiles that are from the same date but cover different k values.')
parser.add_argument('--config', help="Absolute path to the config file used in the run that generated the data.", required=True)
parser.add_argument('-d','--date', help='Date to comput the qmodes values for', required=True)
parser.add_argument('--klb', help='k value lower bound', type=int, required=True)
parser.add_argument('--kub', help='k value upper bound', type=int, required=True)
parser.add_argument('--ktot', help='Total number of k values', type=int, required=True)
parser.add_argument('--rm_old', help='include to remove old files after creating aggregate file', action='store_true')

args        = parser.parse_args()
config_file = args.config
date        = args.date
klb         = args.klb
kub         = args.kub
ktot        = args.ktot
rm_old      = args.rm_old

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# MAIN 

config_params = load_qmodes_config(config_file)

# Getting all qk files in QMODES_QKDATA_DIR that have date and ktot values
# specified in argparse arguments.

klb_str  = "0"*(3-len(str(klb)))  + str(klb)
kub_str  = "0"*(3-len(str(kub)))  + str(kub)
ktot_str = "0"*(3-len(str(ktot))) + str(ktot)
combined_outfile = config_params.get_default_file_path("qmodes", date, "", klb_str, kub_str, ktot_str)

file_list = get_qmodes_files_with_date_and_ktot(date, ktot_str, config_file)

# Check if file_list covers all of the k values
cover_ktot_range     = check_qmodes_files_cover_ktot_range(file_list, config_file)
files_have_all_modes = check_qmodes_files_have_all_modes(file_list)

if cover_ktot_range and files_have_all_modes:
    combine_qmodes_files_from_list(file_list, combined_outfile )

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
