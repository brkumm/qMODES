#------------------------------------------------------------------------------
# IMPORTS
import numpy    as np
import xarray   as xa
from   datetime import datetime

from .qMODES_config_parameters import load_qmodes_config
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#MAIN COMPUTATION OF INTEGRATED VERTICAL STRUCTURE FUNCTION 

def compute_vsf_int(config_file:str, author_name: str =None, 
                    author_email: str =None) -> None:
    """
    Function that computes the integrated vertical structure function (VSF)
    values. These are computed as follows.

    vsf_int(p;m) = int_0^p vsf(p';m) dp'

    The integration is performed using an averaging of the left and right 
    riemannan sums. Previously this was doneusing simpsons method, but this
    is the method used by the Zagar group so their method is 
    used for consistency.

    REQUIRED INPUTS:
        config_file: path to the config file for this particular run.

    OPTIONAL INPUTS:
        author_name: name of author (stored in outputfile metadata)
        author_email: email of author (stored in outputfile metadata)

    """

    #-------------------- Setting Computation Parameters --------------------
    # Reading in parameters from config_file
    config_params = load_qmodes_config(config_file)

    # extracting relavent values from the config file data
    ps0 = config_params.ps0
    vsf_infile = config_params.get_default_file_path("vsf")
    output_file = config_params.get_default_file_path("vsf_int")

    # Reading in values from the vsf data file
    vsf_ds = xa.open_dataset(vsf_infile)
    vsf = vsf_ds["vsf"].values
    vgrid = vsf_ds["vgrid"].values
    mp = len(vgrid)
    num_vmode = vsf_ds.sizes["num_vmode"]

    # Print warning if data file parameters don't match with values in config file.
    if mp != config_params.nplev:
        print(f"WARNING!!!: Number of pressure levels in data file (mp={mp}) does NOT match value specified in the config file (nplev={config_params.nplev})")
    if num_vmode != config_params.nM:
        print(f"WARNING!!!: Number of vertical modes in data file (num_vmode={num_vmode}) does NOT match value specified in the config file (nM={config_params.nM})")

    #------------------------------- Main Loop -------------------------------

    #Initializing vsfint array
    vsfint_temp = np.zeros([num_vmode,mp+1]) #Allocation of matrix that will contain all integrals for all vertical modes

    dz = np.zeros(mp + 1)
    
    for k in range(1, mp):
        dz[k] = vgrid[k - 1] - vgrid[k]
    
    dz[mp] = 2.0 * vgrid[mp - 1]
    dz[0]  = 2.0 * (ps0 - vgrid[0])
    
    for k in range(1, mp + 1):
        dp = 0.5 * (dz[mp - k] + dz[mp + 1 - k])
        for m in range(0, num_vmode):
            vsfint_temp[m, k] = vsfint_temp[m, k - 1] + vsf[m, mp - k] * dp
    
    vsf_int = vsfint_temp[:, 1:] #
    vmodes  = np.array([i for i in range(num_vmode)])

    #-------------------- Saving vsf_int Values to output_file -------------------

    vgrid_int = vgrid[::-1] #ordering switches because integration is done from top of atmosphere to surface
    out_units = 'Pa'
    long_name = 'integrated vertical structure function'
    dtnow     = datetime.now()
    
    coords = { 'vgrid_int': (['vgrid_int' ], vgrid_int),
                  'num_vmode'   : (['num_vmode'], vmodes ) }
    

    data_vars = {'vsf_int':(['num_vmode', 'vgrid_int'], vsf_int,
                            {'units'    : out_units,
                             'long_name': long_name}) }
    
    attrs = {'creation_date':dtnow.strftime("%m/%d/%Y, %H:%M:%S")}
    if author_name != None: attrs['author name'] = author_name
    if author_email != None: attrs['author email'] = author_email
    
    ds = xa.Dataset(data_vars = data_vars,
                    coords = coords,
                    attrs = attrs)
    
    ds.to_netcdf(output_file)
    print(f"vsf_int computation sucessful!!\n\noutput data saved to:\n\t{output_file}")

    return
#-----------------------------------------------------------------------------
