#--------------------------------------------------------------------------
# File:          Calculate_qmodes.py
# Author:        Bradley Kumm (bkumm@wisc.edu) 
# Last Modified: 2023/09/29 (YYYY/MM/DD)
# Description:   Script that calculates the omega  modes using the
#                calculation from the Zagar-Neduhal 2023 manuscript for 
#                omega.
#
# Notes:         WARNING!!! The input file must be a netCDF files!!!
#               
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
#IMPORTS
import time
import argparse
import xarray as xa
import numpy as np
from datetime import datetime

#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
#READING IN COMMAND LINE ARGUMENTS (frequently changed params only)

parser = argparse.ArgumentParser(description="This script calculates the qk values for a specified date")
parser.add_argument('-d', '--date', help='date to calculate in YYYYMMDD format', required=True)
parser.add_argument('-k', '--k_lower_bound', help='high pass filter that only allows k modes above the given value to be included in the sums', type=int, default=0)
parser.add_argument('--noMRG', help='command line flag that, if included, removes the n=0 mode for BAL component',action='store_true')
args = parser.parse_args()

date      = args.date
k_lb_orig = args.k_lower_bound 
k_lb      = k_lb_orig
noMRG     = args.noMRG
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
#USER INPUTS AND CONSTANTS

# author details for output file
author_name = "USER's NAME"
author_email = "USER's EMAIL"

# Mode, Mode Number, and Grid Data
Mode_list = ['EIG','WIG','BAL']

#Fourier Space Parameters
#Hard coding these in for now ... should read in from config/ files later
nK = 351 #number of K modes
nM = 60  #number of M modes
nN = 200 #number of N modes

# Input and Output File Data
grid_infile      = "../../input_data/ERA_Data/ERA_FILE_HERE.nc" # sample file to get grid parameters, and ERA file should work if you want to use the same grid

qk_dir           = "../../MODES_Data/qmodes/"
qk_infile        = qk_dir + f"qk_{date}0000000.nc"
qk_noMRG_infile  = qk_dir + f"qk_noMRG_{date}0000000.nc"
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# READING INPUT DATA

#Reading in Grid Data
grid_ds        = xa.open_dataset(grid_infile)
lon            = grid_ds["lon"].values

#Reading in Data for Calculations

qk_ds  = xa.open_dataset(qk_infile)

lat  = qk_ds["lat"  ].values
plev = qk_ds["vgrid_int"].values

nlon           = lon.shape[0]
nlat           = lat.shape[0]
nplev          = plev.shape[0]
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# MAIN LOOP

dtnow = datetime.now()
tic = time.perf_counter()

for imode in Mode_list:

    #Reading in q_k fourier coefficient data
    if imode == 'BAL' and noMRG: qk_ds = xa.open_dataset(qk_noMRG_infile)
    else: qk_ds = xa.open_dataset(qk_infile)

    qk_mode = qk_ds[f"qk_{imode}"].values 
    
    #Initalizing q_mode
    q_mode  = np.zeros(( nplev, nlat, nlon))

    # Main Loop
    for ilon in range(nlon):
        
        if k_lb == 0:
            q_mode[:,:,ilon] += qk_mode[0,0,:,:]
            k_lb += 1 #shift k_lb by one so loop below calculates remaining terms in sum

        # k!= 0 terms of longitude fourier expansion or terms starting from the lower bound
        for kk in range(k_lb,nK):
            q_mode[:,:,ilon] += 2.0 * ( qk_mode[0,kk,:,:] * np.cos(float(kk) * np.radians(lon[ilon])) - qk_mode[1,kk,:,:] * np.sin(float(kk) * np.radians(lon[ilon])) )



    # SAVING DATA TO NETCDF FILE

    coords    = {'plev': ( ['plev'     ], plev ),
                 'lat' : ( ['lat'      ], lat  ),
                 'lon' : ( ['lon'      ], lon  ) }

    data_vars = {f'q_{imode}' :([ 'plev', 'lat', 'lon'], q_mode,
                        { 'long_name':f'{imode} Part of q'}) }

    attrs     = {'creation_date':dtnow.strftime("%m/%d/%Y, %H:%M:%S"),
                 'author':author_name,
                 'email' :author_email}

    ds        = xa.Dataset(data_vars=data_vars,
                           coords=coords,
                           attrs=attrs)

    k_lb_str = str(0)*(3-len(str(k_lb_orig))) + str(k_lb_orig)

    outfile  = f"../../output_data/qMODES_Data/qmodes"
    if noMRG:          outfile += f"_noMRG"
    if k_lb_orig != 0: outfile += f"_k{k_lb_str}-{nK}"
    outfile += f"_{date}0000000.nc"


    ds.to_netcdf(outfile, mode='a')
    print(f"q_{imode} data saved to:\n\t{outfile}")
    if noMRG: print(f"WARNING: THIS IS A noMRG FILE")

toc = time.perf_counter()
print(f"time to complete main loop = {(toc - tic)/60.0} min")
#--------------------------------------------------------------------------
