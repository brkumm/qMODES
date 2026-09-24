#-----------------------------------------------------------------------------
# IMPORTS
import numpy as np
import xarray as xa
from datetime import datetime

from .qMODES_config_parameters import load_qmodes_config

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# MAIN COMPUTATION OF qk VALUES

def compute_qk(mode: str, date: str, k_lb: int,
               k_ub: int, ktot: int, config_file: str, 
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
    #---------- Retrieving config file params ----------
    config_params = load_qmodes_config(config_file)

    #---------- Input Checks ----------
    if mode not in ["EIG", "WIG", "BAL"]:
        raise ValueError(f"Invalid input for 'mode' variable ({mode}). Valid values are 'EIG', 'WIG', or 'BAL'.")

    #---------- Initial Calcs ----------
    if ktot == None:
        ktot = config_params.nK

    vsf_int_infile = config_params.get_default_file_path('vsf_int')
    coef_infile    = config_params.get_default_file_path('coef', date)

    k_lb_str = "0"*(3-len(str(k_lb))) + str(k_lb)
    k_ub_str = "0"*(3-len(str(k_ub))) + str(k_ub)
    ktot_str = "0"*(3-len(str(ktot))) + str(ktot)

    outfile = config_params.get_default_file_path('qk', date, None, k_lb_str, k_ub_str, ktot_str)

    kvals = [i for i in range(k_lb, k_ub+1)]

    #---------- Reading in data that is constant over the loop ----------
    # grid data
    nplev = config_params.nplev
    nlat  = config_params.nlat

    # use first file hough file with k=klb  
    # to retrieve the latitude values.
    sample_grid_file = config_params.get_default_file_path('hough', None, k_lb_str, None, None, None)
    sample_gird_ds = xa.open_dataset(sample_grid_file)
    lat = sample_gird_ds["lat"].values

    # mode index data
    nM = config_params.nM
    nN = config_params.nN

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
        hough_infile = config_params.get_default_file_path("hough", None, kstr, None, None, None)
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