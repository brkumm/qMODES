#-----------------------------------------------------------------------------
# File:          computations_qk.py
# Author:        Bradley Kumm (brkumm@gmail.com
# Last Modified: 2026/01/12 (YYYY/MM/DD)
# Description:   Functions used to compute the qk values, meridional Fourier
#                components. See Kumm et al. 2026 (currently in review) paper
#                for equations relavent to the computations.
#
# Notes:         
#               
#------------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# IMPORTS

import numpy as np
import xarray as xa
from   datetime import datetime

from .read_environment_variables import get_QMODES_VSFINT_DIR, get_QMODES_COEF_DIR, get_QMODES_HOUGH_DIR, get_QMODES_QKDATA_DIR
from .templates import template_vsf_int_fname, template_hough_fname, template_coef_fname, template_qk_with_klb_kub_ktot_fname
from .parameters import nK, nM, nN, nlat, nplev
from .sample_files import sample_hough_file
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------

# MAIN COMPUTATION OF qk VALUES

def compute_qk(mode, date, k_lb, k_ub, ktot=None, author_name=None, author_email=None):
    """
    Function that computes longitudnal fourier components for moisture 
    EIG, WIG, and ROT modes from global dry modal decomposition value 
    (coefficients, integrated VSF, and hough function values) 


    REQUIRED INPUTS:
        mode: which mode is being computed (EIG, WIG, or ROT/BAL)
        date: date to perform the calculation for expressed as a 
              string in YYYYMMDD format
        k_lb: k index lower bound (inclusive)
        k_ub: k index upper bound (inclusive)

    OPTIONAL INPUTS:
        author_name:  name of author (stored in outputfile metadata)
        author_email: email of author (stored in outputfile metadata)

    IMPORTANT NOTE!!!
        The factor of the background moisture derivative is left out of 
        the qk and qmodes computations to have extra flexibility in how
        to account for this term, latitude dependent vs indepent bkg 
        etc... This factor needs to be accounted for before you will 
        obtain correct moisture anomoly values. I recommend using the 
        qMODES package data reader functions or at least looking at them
        to see how this is done.  

    """

    #---------- Input Checks ----------

    if mode not in ["EIG", "WIG", "BAL"]:
        print("EXITING: --mode command line flag must be EIG, WIG, or BAL")
        exit()

    if ktot == None:
        ktot = nK

    #---------- Initial Calcs ----------
    outdir      = get_QMODES_QKDATA_DIR()
    vsf_int_dir = get_QMODES_VSFINT_DIR()
    coef_dir    = get_QMODES_COEF_DIR()
    hough_dir   = get_QMODES_HOUGH_DIR()

    vsf_int_infile = f"{vsf_int_dir}/{template_vsf_int_fname()}"
    coef_infile    = f"{coef_dir}/{template_coef_fname(date)}"

    k_lb_str = "0"*(3-len(str(k_lb))) + str(k_lb)
    k_ub_str = "0"*(3-len(str(k_ub))) + str(k_ub)
    ktot_str = "0"*(3-len(str(nK)))   + str(nK)

    outfile = f"{outdir}/{template_qk_with_klb_kub_ktot_fname(date, k_lb_str, k_ub_str, ktot_str)}"

    kvals = [i for i in range(k_lb, k_ub+1)]


    #---------- Reading In Grid & Preliminary Data ----------
    sample_hough_ds = xa.open_dataset(sample_hough_file())
    lat             = sample_hough_ds["lat"].values

    # Reading in hough_coef data
    coef_ds = xa.open_dataset(coef_infile)
    coefs   = coef_ds[mode].values
    
    # Reading in vsf_int data
    vsf_int_ds = xa.open_dataset(vsf_int_infile)
    vsf_int    = vsf_int_ds["vsf_int"].values
    vgrid_int  = vsf_int_ds["vgrid_int"].values


    #---------- Main Loop ----------
    # initalize qk and hough
    qk    = np.zeros((2, len(kvals), nplev, nlat))
    hough = np.zeros((nM,3,nN,nlat))

    
    #initalizing values used in loop
    RE_inner_sum = 0
    IM_inner_sum = 0
        
    #Loop
    for ik in range(len(kvals)):
        kk = kvals[ik] #kk is the actual k value
        
        #read in Hough Function data
        kstr         = "0"*(3-len(str(kk)))+str(kk)
        hough_infile = f"{hough_dir}/{template_hough_fname(kstr)}"
        hough_ds     = xa.open_dataset(hough_infile)
        hough        = hough_ds[f"{mode}"].values
    
        for iplev in range(nplev):
    
            for mm in range(nM):
                
                #re-initializing inner sums
                RE_inner_sum = 0
                IM_inner_sum = 0
    
                #calculating the n portion of the sum (the "inner sum") 
                for nn in range(nN):
                    RE_inner_sum += coefs[0,0,kk,mm,nn] * hough[mm,2,:,nn] # [2,:,mm,nn] -- reordered indexing
                    IM_inner_sum += coefs[0,1,kk,mm,nn] * hough[mm,2,:,nn] # [2,:,mm,nn] -- reordered indexing
    
                qk[0,ik,iplev,:] +=  vsf_int[mm,iplev] * RE_inner_sum
                qk[1,ik,iplev,:] +=  vsf_int[mm,iplev] * IM_inner_sum 

    #---------- Saving Data to Outputfile ----------

    dtnow = datetime.now()

    coords    = {'k_mode'    : ( ['k_mode'    ], np.array(kvals) ),
                 'vgrid_int' : ( ['vgrid_int' ], vgrid_int       ),
                 'lat'       : ( ['lat'       ], lat             )  }
    
    data_vars = {f'qk_{mode}' :( ['Re+Im', 'k_mode', 'vgrid_int', 'lat'], qk,
                                 {'long_name':f'{mode} Part of specific humidity'} )  }
    
    attrs     = {'creation_date':dtnow.strftime("%m/%d/%Y, %H:%M:%S")}
    
    if author_name  != None: attrs['author'] = author_name
    if author_email != None: attrs['email']  = author_email
    
    ds        = xa.Dataset(data_vars=data_vars,
                           coords=coords,
                           attrs=attrs)
    
    ds.to_netcdf(outfile, mode='a')
    print(f"qk_{mode} data saved to:\n\t{outfile}")

    return

#--------------------------------------------------------------------------
