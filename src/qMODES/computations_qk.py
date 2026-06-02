#-----------------------------------------------------------------------------
# File:          computations_qk.py
# Author:        Bradley Kumm (brkumm@gmail.com)
# Last Modified: 2026/04/15 (YYYY/MM/DD)
# Description:   Functions used to compute the qk (meridional Fourier
#                component) values. See Kumm et al. 2026 (currently in review)
#                paper for equations relavent to the computations.
#
# Notes:         
#               
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# IMPORTS
from .get_environment_variables import get_QMODES_INPUT_DATA_DIR, get_QMODES_OUTPUT_DATA_DIR, get_QMODES_PARAMETERS_FILE
from .templates import template_vsf_int_fname, template_hough_fname, template_coef_fname, template_qk_with_klb_kub_ktot_fname

import yaml
import numpy as np
import xarray as xa
from datetime import datetime

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# MAIN COMPUTATION OF qk VALUES

def compute_qk(mode: str, date: str, k_lb: int, k_ub: int, ktot: int = None, 
               input_data_dir: str = get_QMODES_INPUT_DATA_DIR(), 
               output_data_dir: str = get_QMODES_OUTPUT_DATA_DIR(), 
               parameter_file: str = get_QMODES_PARAMETERS_FILE(), 
               author_name: str = None, author_email: str = None) -> None:
    """
    Function that computes longitudnal fourier components for moisture 
    EIG, WIG, and ROT modes from global dry modal decomposition value 
    (coefficients, integrated VSF, and hough function values).


    REQUIRED INPUTS:
        mode: which mode is being computed (EIG, WIG, or ROT/BAL)
        date: date to perform the calculation for expressed as a 
              string in YYYYMMDD format
        k_lb: k index lower bound (inclusive)
        k_ub: k index upper bound (inclusive)

    OPTIONAL INPUTS:
        ktot: Total number of k-modes.

        input_data_dir:  qMODES input data dir.
        output_data_dir: qMODES output data dir.
        parameter_file: File where parameters are stored.
        
        author_name: Name of author (stored in outputfile metadata)
        author_email: Email of author (stored in outputfile metadata)

    IMPORTANT NOTE!!!
        The factor of the background moisture derivative is left out of 
        the qk and qmodes computations to have extra flexibility in how
        to account for this term, latitude dependent vs indepent bkg 
        etc... This factor needs to be accounted for before you will 
        obtain correct moisture anomoly values. I recommend using the 
        qMODES package data reader functions or at least looking at them
        to see how this is done.  

    """
    #---------- Opening parameters file ----------
    with open(parameter_file, 'r') as param_file:
        params = yaml.safe_load(param_file)

    #---------- Input Checks ----------
    if mode not in ["EIG", "WIG", "BAL"]:
        print("EXITING: 'mode' value must be EIG, WIG, or BAL")
        exit()

    if ktot == None:
        ktot = params['mode_parameters']['nK']

    #---------- Initial Calcs ----------
    vsf_int_infile = template_vsf_int_fname(input_data_dir)
    coef_infile    = template_coef_fname(input_data_dir, date)

    k_lb_str = "0"*(3-len(str(k_lb))) + str(k_lb)
    k_ub_str = "0"*(3-len(str(k_ub))) + str(k_ub)
    ktot_str = "0"*(3-len(str(ktot))) + str(ktot)

    outfile = template_qk_with_klb_kub_ktot_fname(output_data_dir, date, 
                                                  k_lb_str, k_ub_str, 
                                                  ktot_str)

    kvals = [i for i in range(k_lb, k_ub+1)]

    #---------- Reading in data that is constant over the loop ----------
    # grid data
    nplev = params['grid_parameters']['nplev']
    nlat  = params['grid_parameters']['nlat']

    sample_gird_ds = xa.open_dataset(params['sample_files']['grid_file'])
    lat = sample_gird_ds["lat"].values

    # mode index data
    nM = params['mode_parameters']['nM']
    nN = params['mode_parameters']['nN']

    # hough_coef data
    coef_ds = xa.open_dataset(coef_infile)
    coefs   = coef_ds[mode].values
    
    # vsf_int data
    vsf_int_ds = xa.open_dataset(vsf_int_infile)
    vsf_int    = vsf_int_ds["vsf_int"].values
    vgrid_int  = vsf_int_ds["vgrid_int"].values

    #---------- Main Loop ----------
    # Loop parameters
    nREIM = 2 # number of indicies for Re+Im 
    nHvec = 3 # number of indicies for Hough vector

    # Initalize qk and hough
    qk    = np.zeros((nREIM, len(kvals), nplev, nlat))
    hough = np.zeros((nM,nHvec,nN,nlat)) 

    # Initalizing RE & IM components of inner sum
    RE_inner_sum = 0
    IM_inner_sum = 0
        
    # Main loop
    for ik, kk in enumerate(kvals):
        
        # Read in Hough Function data
        kstr         = "0"*(3-len(str(kk)))+str(kk)
        hough_infile = template_hough_fname(input_data_dir, kstr)
        hough_ds     = xa.open_dataset(hough_infile)
        hough        = hough_ds[f"{mode}"].values
    
        for iplev in range(nplev):
            for mm in range(nM):
                
                # Reset inner sum values
                RE_inner_sum = 0
                IM_inner_sum = 0
    
                # Calculating the "inner" (n index) portion of the sum 
                for nn in range(nN):
                    RE_inner_sum += coefs[0,0,kk,mm,nn] * hough[mm,2,:,nn]
                    IM_inner_sum += coefs[0,1,kk,mm,nn] * hough[mm,2,:,nn]
    
                qk[0,ik,iplev,:] +=  vsf_int[mm,iplev] * RE_inner_sum
                qk[1,ik,iplev,:] +=  vsf_int[mm,iplev] * IM_inner_sum

        hough_ds.close()

    #---------- Saving Data to outfile ----------
    # Meta Data info
    dtnow = datetime.now()
    attrs     = {'creation_date':dtnow.strftime("%m/%d/%Y, %H:%M:%S")}
    
    if author_name  != None: attrs['author'] = author_name
    if author_email != None: attrs['email']  = author_email

    #Coordinates and data for dataset creation
    coords    = {'k_mode'    : ( ['k_mode'], np.array(kvals)),
                 'vgrid_int' : ( ['vgrid_int'], vgrid_int),
                 'lat'       : ( ['lat'], lat)  }
    
    data_vars = {f'qk_{mode}' :( ['Re+Im', 'k_mode', 'vgrid_int', 'lat'], qk,
                 {'long_name':f'{mode} Part of specific humidity'}) }
    
    # Creatign dataset and saving as a netCDF file
    ds        = xa.Dataset(data_vars=data_vars,
                           coords=coords,
                           attrs=attrs)
    
    ds.to_netcdf(outfile, mode='a')
    print(f"qk_{mode} data saved to:\n\t{outfile}")

    return

#-----------------------------------------------------------------------------