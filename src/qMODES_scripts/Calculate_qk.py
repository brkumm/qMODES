#--------------------------------------------------------------------------
# File:          Calculate_omegak.py
# Author:        Bradley Kumm (bkumm@wisc.edu) 
# Last Modified: 2023/11/20 (YYYY/MM/DD)
# Description:   Script that calculates the omegak coefficients as 
#                described in the Zagar-Neduhal 2023 manuscript.
#
# Notes:         WARNING!!! The input file must be a netCDF files!!!
#                Doing this calculation to make sure that I am combining
#                the hough functions, coefficients, etc... correctly 
#                because the q values that I getting from doing the same
#                procedure don't look right ... might need to add 
#                y (latitude) dependance.
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
#IMPORTS

import os
import time
import argparse
import numpy    as np
import xarray   as xa
from datetime import datetime

#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
#READING IN COMMAND LINE ARGUMENTS AND INITIAL CALCS
# (frequently changed params only)

# Getting command line arguments
parser = argparse.ArgumentParser(description="This script calculates the omegakk values for a specified date")
parser.add_argument('-d', '--date', help='date to calculate in YYYYMMDD format', required=True)
parser.add_argument('-m', '--mode', help='mode to perform calculation for (EIG, WIG, or BAL)', required=True)
parser.add_argument('--noMRG', help='command line flag that, if included, removes the n=0 mode for BAL component',action='store_true')
args = parser.parse_args()

date  = args.date
mode  = args.mode
noMRG = args.noMRG

# Initial calcs
outdir  = "../../output_data/qk_data/"
outfile = outdir + f"qk_{date}0000000.nc"
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# INPUT DATA CHECKS

# Checking mode input from command line
if mode not in ["EIG","WIG","BAL"]:
    print("EXITING: --mode command line flag must be EIG, WIG, or BAL")
    exit()

# Checking noMRG logic
if noMRG:
    #Exit if trying to use noMRG for non BAL mode
    if not mode == 'BAL':
        print("EXITING: --noMRG command line flag can only be included if BAL mode is chosen.")
    
    #checking to see if EIG and WIG already computed and stored in outfile
    #should only compute BAL with noMRG after EIG and WIG already computed 
    #(for file naming logic)
    test_ds = xa.open_dataset(outfile)
    test_ds_vars = [i for i in test_ds.data_vars]
    if 'qk_EIG' not in test_ds_vars or 'qk_WIG' not in test_ds_vars:
        print(f"EXITING: MUST compute EIG and WIG first if computing BAL with noMRG")
        exit()
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
#PARAMETERS AND INITIAL CALCS (params that aren't changed frequently,
#  i.e. same for all jobs in single run)

# author details for output file
author_name = "USER's NAME"
author_email = "USER's EMAIL"

#Fourier Space Parameters 
#Hard coding these in for now ... should read in from config/ files later
nK = 351 #number of K modes
nM = 60  #number of M modes
nN = 200 #number of N modes

# Input Data Directories and Files
vsf_int_infile = "../../input_data/MODES_data/vsf_int/vsf_int.data.nc"
hough_dir      = "../../input_data/MODES_data/hough/"
coef_infile    = f"../../input_data/MODES_data/coef/Hough_coeff_M60_F320_{date}0000000.nc" # Trailing zeros are for time, only one time per day for now

#Initial calcs
sample_hough_infile = "../../input_data/MODES_data/hough/...SAMPLE_HOUGH_FILE.wn00000.nc";
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# READING IN GRID DATA
sample_hough_ds = xa.open_dataset(sample_hough_infile)
lat             = sample_hough_ds["lat"].values
nlat            = lat.shape[0]

#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# READING IN OTHER PRELIMINARY DATA

# Reading in hough_coef data
coef_ds = xa.open_dataset(coef_infile)
coefs   = coef_ds[mode].values

# Reading in vsf_int data
vsf_int_ds = xa.open_dataset(vsf_int_infile)
vsf_int    = vsf_int_ds["vsf_int"].values
vgrid_int  = vsf_int_ds["vgrid_int"].values
nplev      = vgrid_int.shape[0]
#--------------------------------------------------------------------------



#-------------------------------------------------------------------------
# MAIN LOOP

# initalize qk
qk = np.zeros((2, nK, nplev, nlat))

#initalize freq and hough
hough    = np.zeros((nM,3,nN,nlat)) 
freq_EIG = np.zeros((nN,nM))
freq_WIG = np.zeros((nN,nM))
freq_BAL = np.zeros((nN,nM))

#different modes have different portions of frequency values in files
#defining upper and lower frequency index bounds

#initalizing for EIG mode bounds
freq_lb = 0
freq_ub = nN

#changing to proper bounds if mode isn't EIG
if mode == "WIG":
    freq_lb = nN
    freq_ub = 2*nN
elif mode == "BAL":
    freq_lb = 2*nN
    freq_ub = 3*nN


# Main Loop

#initalizing values used in loop
RE_inner_sum = 0
IM_inner_sum = 0
n_lb         = int(noMRG) 

tic = time.perf_counter()

for kk in range(nK):
    
    #print(f"\t{kk+1} out of {nK}")
    
    #read in Hough Function data
    # Hough files are stored by "k" index
    kstr = "0"*(3-len(str(kk)))+str(kk)
    hough_infile = hough_dir + f"hough_F320_M60.wn00{kstr}.nc"
    hough_ds   = xa.open_dataset(hough_infile)
    hough  = hough_ds[f"{mode}"].values

    for iplev in range(nplev):

        for mm in range(nM):
            
            #re-initializing inner sums
            RE_inner_sum = 0
            IM_inner_sum = 0

            #calculating the n portion of the sum (the "inner sum") starting from the lower bound n_lb 
            for nn in range(n_lb,nN):
                RE_inner_sum += coefs[0,0,kk,mm,nn] * hough[mm,2,:,nn] # [2,:,mm,nn] -- reordered indexing
                IM_inner_sum += coefs[0,1,kk,mm,nn] * hough[mm,2,:,nn] # [2,:,mm,nn] -- reordered indexing

            qk[0,kk,iplev,:] +=  vsf_int[mm,iplev] * RE_inner_sum
            qk[1,kk,iplev,:] +=  vsf_int[mm,iplev] * IM_inner_sum 

toc = time.perf_counter()
print(f"time to complete main loop = {(toc - tic)/60.0} min")
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# SAVING DATA TO NETCDF FILE

dtnow = datetime.now()

coords    = {'k_mode'    : ( ['k_mode'    ], np.array(range(nK)) ),
             'vgrid_int' : ( ['vgrid_int' ], vgrid_int           ),
             'lat'       : ( ['lat'       ], lat                 )  }

data_vars = {f'qk_{mode}' :(['Re+Im', 'k_mode', 'vgrid_int', 'lat'], qk,
                    { 'long_name':f'{mode} Part of specific humidity'})      }

if noMRG:
    data_vars.update({'noMRG':True})


attrs     = {'creation_date':dtnow.strftime("%m/%d/%Y, %H:%M:%S"),
             'author':author_name,
             'email' :author_email}

ds        = xa.Dataset(data_vars=data_vars,
                       coords=coords,
                       attrs=attrs)

if noMRG:
    outfile = outdir + f"qk_noMRG_{date}0000000.nc"

ds.to_netcdf(outfile, mode='a')
print(f"qk_{mode} data saved to:\n\t{outfile}")

if noMRG:
    print(f"WARNING: This is a noMRG file!!!!!")
#--------------------------------------------------------------------------
