#------------------------------------------------------------------------------
# IMPORTS
import yaml
import numpy    as np
import xarray   as xa
from   datetime import datetime

from .qMODES_config_parameters import load_qmodes_config

#------------------------------------------------------------------------------



#--------------------------------------------------------------------------
# MAIN COMPUTATION OF qmodes VALUES

def compute_qmodes(mode: str, date: str, k_lb: int, k_ub: int, ktot: int,
                   config_file: str,
                   author_name: str =None, author_email: str =None):
    """
    Function that computes the moisture modal values from the qk 
    (longitudnal Fourier components) that are stored in the corresponding 
    qkdir files. 


    REQUIRED INPUTS:
        mode: Which mode is being computed (EIG, WIG, or ROT/BAL)
        date: Date to perform the calculation for expressed as a 
              string in YYYYMMDD format
        k_lb: k index lower bound (inclusive)
        k_ub: k index upper bound (inclusive)

    OPTIONAL INPUTS:
        ktot: Total number of k mode indicices used in this decomposition

        output_data_dir: qMODES output data directory (or test output dir)
        parameter_file:  qMODES param file (or test param file)

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
    #---------- Opening parameters file ----------
    config_params = load_qmodes_config(config_file)
    #with open(parameter_file, 'r') as param_file:
    #    params = yaml.safe_load(param_file)
    
    #---------- Input Checks ----------
    if mode not in ["EIG", "WIG", "BAL"]:
        raise ValueError(f"Invalid input for 'mode' variable ({mode}). Valid values are 'EIG', 'WIG', or 'BAL'.")

    #---------- Initial Variable Setup ----------
    if ktot == None:
        ktot = params['mode_parameters']['nK']

    nplev = config_params.nplev
    nlat  = config_params.nlat
    nlon  = config_params.nlon

    klb_str = "0"*(3-len(str(k_lb)))  + str(k_lb)
    kub_str = "0"*(3-len(str(k_ub)))  + str(k_ub)
    ktot_str = "0"*(3-len(str(ktot))) + str(ktot)

    kvals     = np.array( [i for i in range(k_lb, k_ub+1)] )
    grid_file = config_params.get_default_file_path('ERA_q', date)

    qk_infile = config_params.get_default_file_path('qk', date, None, klb_str, 
                                                    kub_str, ktot_str)
    
    outfile = config_params.get_default_file_path('qmodes', date, None, klb_str, 
                                                  kub_str, ktot_str)

    #---------- Reading Input Data --------
    grid_ds = xa.open_dataset(grid_file)
    lon     = grid_ds["lon"].values

    qk_ds   = xa.open_dataset(qk_infile)
    qk_mode = qk_ds[f"qk_{mode}"].values 
    lat     = qk_ds["lat"].values
    plev    = qk_ds["vgrid_int"].values
    
    #---------- Main Loop ----------
    dtnow = datetime.now()
  
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
                q_mode[:,:,ilon] += 2.0 * ( 
                      qk_mode[0,kk-k_lb,:,:] * np.cos(float(kk) * np.radians(lon[ilon])) 
                    - qk_mode[1,kk-k_lb,:,:] * np.sin(float(kk) * np.radians(lon[ilon])) 
                    )
    
    # SAVING DATA TO NETCDF FILE
    coords    = {'k_mode': ( ['k_mode'], np.array(kvals) ),
                 'plev'  : ( ['plev'], plev ),
                 'lat'   : ( ['lat' ], lat  ),
                 'lon'   : ( ['lon' ], lon  ) }
    
    data_vars = {f'q_{mode}' :([ 'plev', 'lat', 'lon'], q_mode,
                        { 'long_name':f'{mode} Part of q'}) }
    
    attrs     = {'creation_date':dtnow.strftime("%m/%d/%Y, %H:%M:%S")}

    if author_name  != None: attrs['author'] = author_name,
    if author_email != None: attrs['email' ] = author_email
    
    ds        = xa.Dataset(data_vars = data_vars,
                           coords    = coords,
                           attrs     = attrs)
    
    ds.to_netcdf(outfile, mode='a')
    print(f"q_{mode} data saved to:\n\t{outfile}")

    return
#--------------------------------------------------------------------------