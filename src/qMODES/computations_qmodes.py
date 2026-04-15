#-----------------------------------------------------------------------------
# File:          computations_qmodes.py
# Author:        Bradley Kumm (brkumm@gmail.com)
# Last Modified: 2026/04/15 (YYYY/MM/DD)
# Description:   Main function used to compute the EIG, WIG, BAL/ROT and M 
#                modal moisture values.
#
# Notes:         
#               
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
# IMPORTS
from .read_environment_variables import get_QMODES_QKDATA_DIR, get_QMODES_QMODESDATA_DIR
from .parameters   import nK, nplev, nlat, nlon
from .templates    import template_qk_fname, template_qmodes_fname, template_qmodes_with_klb_kub_ktot_fname
from .sample_files import sample_ERA_file

import numpy    as np
import xarray   as xa
from   datetime import datetime
#------------------------------------------------------------------------------



#--------------------------------------------------------------------------
# MAIN COMPUTATION OF qmodes VALUES

def compute_qmodes(mode, date, k_lb, k_ub, ktot=None, author_name=None, author_email=None):
    """
    Function that computes the moisture modal values from the qk 
    (longitudnal Fourier components) that are stored in the corresponding 
    qkdir files. 


    REQUIRED INPUTS:
        mode:         which mode is being computed (EIG, WIG, or ROT/BAL)
        date:         date to perform the calculation for expressed as a 
                      string in YYYYMMDD format

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

    #---------- Initial Variable Setup ----------
    klb_str = "0"*(3-len(str(k_lb)))  + str(k_lb)
    kub_str = "0"*(3-len(str(k_ub)))  + str(k_ub)
    ktot_str = "0"*(3-len(str(ktot))) + str(ktot)

    kvals       = np.array( [i for i in range(k_lb, k_ub+1)] )
    Mode_list   = ['EIG','WIG','BAL']
    grid_infile = sample_ERA_file()
    qk_infile   = f"{get_QMODES_QKDATA_DIR()}/{template_qk_fname(date)}"


    #---------- Reading Input Data ----------
    grid_ds = xa.open_dataset(grid_infile)
    lon     = grid_ds["lon"].values
    qk_ds   = xa.open_dataset(qk_infile)
    lat     = qk_ds["lat"].values
    plev    = qk_ds["vgrid_int"].values


    #---------- Main Loop ----------

    dtnow = datetime.now()
    
    #Reading in q_k fourier coefficient data
    qk_ds = xa.open_dataset(qk_infile)
    qk_mode = qk_ds[f"qk_{mode}"].values 
        
    #Initalizing q_mode
    q_mode  = np.zeros((nplev, nlat, nlon))
    
    # Main Loop
    for ilon in range(nlon):
                
        for kk in kvals:

            # k=0 term in Fourier expansion
            if kk == 0:
                q_mode[:,:,ilon] += qk_mode[0,kk,:,:]

            # k!=0 terms
            else:
                q_mode[:,:,ilon] += 2.0 * ( qk_mode[0,kk,:,:] * np.cos(float(kk) * np.radians(lon[ilon])) - qk_mode[1,kk,:,:] * np.sin(float(kk) * np.radians(lon[ilon])) )
    
    
    # SAVING DATA TO NETCDF FILE
    
    coords    = {'k_mode' : ( ['k_mode'], np.array(kvals) ),
                 'plev'   : ( ['plev'], plev ),
                 'lat'    : ( ['lat' ], lat  ),
                 'lon'    : ( ['lon' ], lon  ) }
    
    data_vars = {f'q_{mode}' :([ 'plev', 'lat', 'lon'], q_mode,
                        { 'long_name':f'{mode} Part of q'}) }
    
    attrs     = {'creation_date':dtnow.strftime("%m/%d/%Y, %H:%M:%S")}

    if author_name  != None: attrs['author'] = author_name,
    if author_email != None: attrs['email' ] = author_email
    
    ds        = xa.Dataset(data_vars = data_vars,
                           coords    = coords,
                           attrs     = attrs)
    
    
    outfile = f"{get_QMODES_QMODESDATA_DIR()}/{template_qmodes_with_klb_kub_ktot_fname(date, klb_str, kub_str, ktot_str)}"
    
    
    ds.to_netcdf(outfile, mode='a')
    print(f"q_{mode} data saved to:\n\t{outfile}")

    return

#--------------------------------------------------------------------------
