#-----------------------------------------------------------------------------
# IMPORTS
import argparse
import xarray as xa
from qMODES import get_QMODES_QKDATA_DIR
from qMODES import nK
from qMODES import get_klb_kub_ktot_from_qk_filename, get_qk_files_with_date_and_ktot
from qMODES import check_qk_files_have_all_modes, check_qk_files_cover_ktot_range, combine_qk_files_from_list
from qMODES import template_qk_fname

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# READING COMMAND LINE ARGUMENTS USING argparse
parser = argparse.ArgumentParser(description='This script is used to generate pressure level contour plots for an event over a specific region (originally Madison WI )')
parser.add_argument('-d','--date', help='Date to comput the qk values for', required=True)
parser.add_argument('--ktot', help='Total number of k values', type=int, default=nK  )
parser.add_argument('--rm_old', help='include to remove old files after creating aggregate file', type=int, default=nK )

args   = parser.parse_args()
date   = args.date
ktot   = args.ktot
rm_old = args.rm_old

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# MAIN 

# Getting all files qk files in QMODES_QKDATA_DIR that have date and ktot
# specified from argparse arguments.

file_list = get_qk_files_with_date_and_ktot(date, ktot)

#for fname in file_list:
#    print(fname)

# Check if file_list covers all of the k values

#print(check_qk_files_cover_ktot_range(file_list))

cover_ktot_range = check_qk_files_cover_ktot_range(file_list, 4)
files_have_all_modes = check_qk_files_have_all_modes(file_list)

if cover_ktot_range and files_have_all_modes:
    aggregate_ds = xa.open_mfdataset(file_list, combine="by_coords")
    aggregate_ds.to_netcdf( f"{get_QMODES_QKDATA_DIR()}/{template_qk_fname(date)}" )

elif not cover_ktot_range:
    print(f"Not all k values are covered for the date {date}")

elif not files_have_all_modes:
    print("ERROR: all files must contain EIG, WIG, and BAL modes.")

#-----------------------------------------------------------------------------
