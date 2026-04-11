#-----------------------------------------------------------------------------
# IMPORTS
import argparse
import xarray as xa
from qMODES import get_QMODES_QMODESDATA_DIR
from qMODES import nK
from qMODES import get_klb_kub_ktot_from_qmodes_filename, get_qmodes_files_with_date_and_ktot
from qMODES import check_qmodes_files_have_all_modes, check_qmodes_files_cover_ktot_range, combine_qmodes_files_from_list
from qMODES import template_qmodes_fname

#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
# READING COMMAND LINE ARGUMENTS USING argparse
parser = argparse.ArgumentParser(description='This script is used to aggregate qmodes datafiles that are from the same date but cover different k values.')
parser.add_argument('-d','--date', help='Date to comput the qmodes values for', required=True)
parser.add_argument('--ktot', help='Total number of k values', type=int, default=nK  )
parser.add_argument('--rm_old', help='include to remove old files after creating aggregate file', type=int, default=nK )

args   = parser.parse_args()
date   = args.date
ktot   = args.ktot
rm_old = args.rm_old

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# MAIN 

# Getting all qk files in QMODES_QKDATA_DIR that have date and ktot values
# specified in argparse arguments.

ktot_str = "0"*(3-len(str(ktot))) + str(ktot)
combined_outfile = f"{get_QMODES_QMODESDATA_DIR()}/{template_qmodes_fname(date)}"

file_list = get_qmodes_files_with_date_and_ktot(date, ktot_str)

# Check if file_list covers all of the k values

cover_ktot_range     = check_qmodes_files_cover_ktot_range(file_list)
files_have_all_modes = check_qmodes_files_have_all_modes(file_list)

if cover_ktot_range and files_have_all_modes:
    combine_qmodes_files_from_list(file_list, combined_outfile )

elif not cover_ktot_range:
    print(f"Not all k values are covered for the date {date}")

elif not files_have_all_modes:
    print("ERROR: all files must contain EIG, WIG, and BAL modes.")
#-----------------------------------------------------------------------------
