#-----------------------------------------------------------------------------
# File:          combine_qk.py
# Author:        Bradley Kumm (brkumm@gmail.com)
# Last Modified: 2026/04/15 (YYYY/MM/DD)
# Description:   Functions used to aggregate the qmodes files. 
#
# Notes:         
#               
#------------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# IMPORTS
from .get_environment_variables import get_QMODES_OUTPUT_DATA_DIR, get_QMODES_PARAMETERS_FILE
from .templates import template_combine_qmodes_file_pattern

import yaml
import os
import glob
import xarray as xa
import numpy as np
from datetime import datetime
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# FUNCTIONS
def get_klb_kub_ktot_from_qmodes_filename(filename):
    # input should only be the filename ... no path info.
    rep_filename = filename.replace("-", "_")
    filename_split_list = rep_filename.split("_")

    klb  = filename_split_list[3]
    kub  = filename_split_list[5]
    ktot = filename_split_list[7].split(".")[0]

    return int(klb), int(kub), int(ktot)


def get_qmodes_files_with_date_and_ktot(date: str, ktot_str: int, 
                                        qmodesdir:str = get_QMODES_OUTPUT_DATA_DIR()):
    
    pattern = template_combine_qmodes_file_pattern(qmodesdir, date, ktot_str)
    return glob.glob(pattern)


def check_qmodes_files_cover_ktot_range(file_list: list[str], ktot:int =None,
                                        parameter_file:str =get_QMODES_PARAMETERS_FILE()):
    
    if ktot == None:
        with open(parameter_file, 'r') as param_file:
            params = yaml.safe_load(param_file)
        ktot=params['mode_parameters']['nK']

    ktot_range = set([i for i in range(ktot)])

    for fname in file_list:
        klb, kub, _ = get_klb_kub_ktot_from_qmodes_filename( os.path.basename(fname) )

        for ik in range(klb, kub+1):
            if ik in ktot_range: ktot_range.remove(ik)
            else:
                print(f"ERROR: To combine qmodes files no files should overlap in k values or be greater than {ktot}.\n{ik} violates one of both of these.")
    # if all values removed from ktot one time range is covered
    if not ktot_range: 
        return True

    else:
        print("ERROR: Not all k values are covered by the following files")
        for filename in file_list: 
            print(f"\t{filename}")
        return False


def check_qmodes_files_have_all_modes(file_list: list[str]):

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
                    print("ERROR: The following errors were found while examining qmodes files")
                    is_first_error = False

                print(f"\t{fname}: {var}  data variable found when data vars should only include qk_EIG, qk_WIG, or qk_BAL")

        if var_set:

            if is_first_error:
                    print("ERROR: The following errors were found while examining qmodes files")
                    is_first_error = False

            print(f"\t{fname}: Doesn't have all necessary modes")

    print("\n")

    if is_first_error: return True
    else: return False


def combine_qmodes_files_from_list(file_list: list[str], outfile: str):
    # initializing combined dataset to first file in file_list
    # Going to try writing one mode at a time to see how much memory is used

    modes_list = ["q_EIG", "q_WIG", "q_BAL"]
    dtnow = datetime.now()

    ds = xa.open_dataset(file_list[0])
    plev = ds["plev"].values
    lat  = ds["lat"].values
    lon  = ds["lon"].values

    nplev = len(plev)
    nlat  = len(lat)
    nlon  = len(lon)

    q_mode_sum  = np.zeros((nplev, nlat, nlon))

    for mode in modes_list:

        print(f"computing data for {mode}")
        q_mode_sum  = np.zeros((nplev, nlat, nlon))

        for fname in file_list:
            q_mode_ds = xa.open_dataset(fname)
            q_mode_sum += q_mode_ds[mode].values
            q_mode_ds.close()
        
        # SAVING DATA TO NETCDF FILE    
        coords    = {'plev'   : ( ['plev'], plev ),
                     'lat'    : ( ['lat' ], lat  ),
                     'lon'    : ( ['lon' ], lon  ) }
    
        data_vars = {f'{mode}' :([ 'plev', 'lat', 'lon'], q_mode_sum,
                      { 'long_name':f'{mode} Part of q'}) }
    
        attrs     = {'creation_date':dtnow.strftime("%m/%d/%Y, %H:%M:%S")}
    
        ds        = xa.Dataset(data_vars = data_vars,
                               coords    = coords,
                               attrs     = attrs)
        
        ds.to_netcdf(outfile, mode='a', engine="netcdf4")
        ds.close()
    
    print(f"Data saved to:\n\t{outfile}")
    
    return
#-----------------------------------------------------------------------------
