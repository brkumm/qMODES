#-----------------------------------------------------------------------------
# File:          combine_qk.py
# Author:        Bradley Kumm (brkumm@gmail.com
# Last Modified: 2026/04/03 (YYYY/MM/DD)
# Description:   Functions used to agrogate the qk values. 
#
# Notes:         
#               
#------------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# IMPORTS
import xarray as xa
import numpy as xp
import glob
import os

from .read_environment_variables import get_QMODES_QMODESDATA_DIR
from .templates import template_combine_qmodes_file_pattern
from .parameters import nK
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# FUNCTIONS


#----- Functions to check if necessary files exist -----
def get_klb_kub_ktot_from_qmodes_filename(filename):

    # current filename example: qk_201808010000000_klb_002_kub_003_ktot_351.nc
    # input should only be the filename ... no path info.

    rep_filename = filename.replace("-", "_")
    filename_split_list = rep_filename.split("_")

    klb  = filename_split_list[3]
    kub  = filename_split_list[5]
    ktot = filename_split_list[7].split(".")[0]

    return int(klb), int(kub), int(ktot)


def get_qmodes_files_with_date_and_ktot(date, ktot):
    
    pattern = f"{get_QMODES_MODES_DIR()}/{template_combine_qmodes_file_pattern(date, ktot)}"

    return glob.glob(pattern)


def check_qmodes_files_cover_ktot_range(file_list, ktot=nK):

    ktot_range = set([i for i in range(ktot)])

    for fname in file_list:
        klb, kub, _ = get_klb_kub_ktot_from_qmodes_filename( os.path.basename(fname) )

        for ik in range(klb, kub+1):
            if ik in ktot_range: ktot_range.remove(ik)
            else:
                print(f"ERROR: To combine qk files no files should overlap in k values or be greater than {ktot}.\n{ik} violates one of both of these.")
    # if all values removed from ktot one time range is covered
    if not ktot_range: 
        return True

    else:
        print("ERROR: Not all k values are covered by the following files")
        for fname in file_list: print(f"\tfname")
        return False

def check_qmodes_files_have_all_modes(file_list):

    var_set = {"q_EIG","q_WIG","q_BAL"}
    is_first_error = True

    for fname in file_list:

        fname_ds = xa.open_dataset(fname)
        var_set = {"q_EIG","q_WIG","q_BAL"}
        for var in list( fname_ds.data_vars.keys() ):

            if var in var_set: 
                var_set.remove(var)

            else:

                if is_first_error:
                    print("ERROR: The following errors were found while examining qk files")
                    is_first_error = False

                print(f"\t{fname}: {var}  data variable found when data vars should only include qk_EIG, qk_WIG, or qk_BAL")

        if var_set:

            if is_first_error:
                    print("ERROR: The following errors were found while examining qk files")
                    is_first_error = False

            print(f"\t{fname}: Doesn't have all necessary modes")
        print("\n")

    if is_first_error: return True
    else: return False



#----- Function to combine files -----

def combine_qmodes_files_from_list(file_list, output_filename):
    # initializing combined dataset to first file in file_list
    file_ds = xa.open_dataset(file_list[0])
    combined_ds = file_ds.copy(deep=True)

    # adding data from each of the remaining files to combined_ds
    for fname in flie_list[1:]:
        file_ds = xa.open_dataset(fname)
        combined_ds = combined_ds + file_ds

    combined_ds.to_netcdf(output_filename)

    print(f"Files combined and saved to:\n\t{output_filename}")

    return

#-----------------------------------------------------------------------------
