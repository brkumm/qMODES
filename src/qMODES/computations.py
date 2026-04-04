#-----------------------------------------------------------------------------
# File:          qMODES_Calculations.py
# Author:        Bradley Kumm (brkumm@gmail.com
# Last Modified: 2026/01/12 (YYYY/MM/DD)
# Description:   Various functions used to perform global atmospheric 
#                moisture decomposition computations found in the paper:
#                "Moisture decomposition with normal modes in global data: 
#                balanced and unbalanced components" by Kumm et al. 
#                submitted to JGR Atmospheres in 2025.
#
# Notes:         
#               
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
# IMPORTS

import numpy    as np
import xarray   as xa
from   datetime import datetime

from .parameters   import nK, nM, nN, nplev, nlat, nlon, ps0
from .templates    import template_vsf_fname, template_vsf_int_fname, template_hough_fname, template_coef_fname, template_qk_fname, template_qmodes_fname
from .sample_files import sample_ERA_file, sample_hough_file

#------------------------------------------------------------------------------



#--------------------------------------------------------------------------
# MAIN COMPUTATION OF qmodes VALUES

def compute_qmodes(mode, date, outdir, qk_dir, author_name=None, author_email=None):
    """
    Function that computes the moisture modal values from the qk 
    (longitudnal Fourier components) that are stored in the corresponding 
    qkdir files. 


    REQUIRED INPUTS:
        mode:         which mode is being computed (EIG, WIG, or ROT/BAL)
        date:         date to perform the calculation for expressed as a 
                      string in YYYYMMDD format
        outdir:       directory to store the data after the computation is 
                      performed
        qk_dir:       directory where the qk files are stored

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

    #---------- Initial Variable Setup ----------
    Mode_list = ['EIG','WIG','BAL']
    grid_infile = sample_ERA_file()
    qk_infile   = f"{qk_dir}/{template_qk_fname(date)}"


    #---------- Reading Input Data ----------
    grid_ds = xa.open_dataset(grid_infile)
    lon     = grid_ds["lon"].values
    qk_ds   = xa.open_dataset(qk_infile)
    lat     = qk_ds["lat"  ].values
    plev    = qk_ds["vgrid_int"].values


    #---------- Main Loop ----------

    dtnow = datetime.now()

    for imode in Mode_list:
    
        #Reading in q_k fourier coefficient data
        qk_ds = xa.open_dataset(qk_infile)
        qk_mode = qk_ds[f"qk_{imode}"].values 
        
        #Initalizing q_mode
        q_mode  = np.zeros((nplev, nlat, nlon))
    
        # Main Loop
        for ilon in range(nlon):
            
            #k=0 (constant) term in fourier expansion
            q_mode[:,:,ilon] += qk_mode[0,0,:,:]
    
            # k!= 0 terms of longitude fourier expansion or terms starting from the lower bound
            for kk in range(1,nK):
                q_mode[:,:,ilon] += 2.0 * ( qk_mode[0,kk,:,:] * np.cos(float(kk) * np.radians(lon[ilon])) - qk_mode[1,kk,:,:] * np.sin(float(kk) * np.radians(lon[ilon])) )
    
    
    
        # SAVING DATA TO NETCDF FILE
    
        coords    = {'plev': ( ['plev'], plev ),
                     'lat' : ( ['lat' ], lat  ),
                     'lon' : ( ['lon' ], lon  ) }
    
        data_vars = {f'q_{imode}' :([ 'plev', 'lat', 'lon'], q_mode,
                            { 'long_name':f'{imode} Part of q'}) }
    
        attrs     = {'creation_date':dtnow.strftime("%m/%d/%Y, %H:%M:%S")}
        if author_name  != None: attrs['author'] = author_name,
        if author_email != None: attrs['email' ] = author_email
    
        ds        = xa.Dataset(data_vars=data_vars,
                               coords=coords,
                               attrs=attrs)
    
    
        outfile += f"{outdir}/{template_qmodes_fname(date)}"
    
    
        ds.to_netcdf(outfile, mode='a')
        print(f"q_{imode} data saved to:\n\t{outfile}")

#--------------------------------------------------------------------------
