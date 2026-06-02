#-----------------------------------------------------------------------------
# File:          computations_vsf_int.py
# Author:        Bradley Kumm (brkumm@gmail.com)
# Last Modified: 2026/05/14 (YYYY/MM/DD)
# Description:   Various functions used to compute the integrated Vertical
#                Structure Function (VSF) values from an input VSF data file.
#
# Notes:         
#               
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
# IMPORTS
from .get_environment_variables import get_QMODES_INPUT_DATA_DIR, get_QMODES_PARAMETERS_FILE, get_QMODES_PARAMETERS_FILE
from .templates    import template_vsf_fname, template_vsf_int_fname

import yaml 
import numpy    as np
import xarray   as xa
from   datetime import datetime
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#MAIN COMPUTATION OF INTEGRATED VERTICAL STRUCTURE FUNCTION 

def compute_vsf_int(input_data_dir: str =get_QMODES_INPUT_DATA_DIR(),
                    parameter_file: str =get_QMODES_PARAMETERS_FILE(), 
                    author_name: str =None, author_email: str =None) -> None:
    """
    Function that computes the integrated vertical structure function (VSF)
    values, which are computed as:

    vsf_int(p;m) = int_0^p vsf(p';m) dp'

    The integration is performed using an averaging of the left and right 
    riemannan sums. Previously this was doneusing simpsons method, but this
    is the method used bythe Zagar group so I switched to their method for
    consistancy.

    REQUIRED INPUTS:
        

    OPTIONAL INPUTS:
        author_name: name of author (stored in outputfile metadata)
        author_email: email of author (stored in outputfile metadata)

    """

    #-------------------- Setting Computation Parameters --------------------
    # Input and output files
    vsf_infile  = template_vsf_fname(input_data_dir)
    output_file = template_vsf_int_fname(input_data_dir)

    # Reading in values from parameters file
    with open(parameter_file, 'r') as param_file:
        params = yaml.safe_load(param_file)

    ps0 = params['physical_constants']['ps0']

    # reading in vsf data
    vsf_ds     = xa.open_dataset(vsf_infile)
    vsf        = vsf_ds["vsf"].values
    vgrid      = vsf_ds["vgrid"].values
    mp         = len(vgrid)
    nM         = vsf_ds.sizes["num_vmode"]
    #------------------------------- Main Loop -------------------------------

    #Initializing vsfint array
    vsfint_temp = np.zeros([nM,mp+1]) #Allocation of matrix that will contain all integrals for all vertical modes

    dz = np.zeros(mp + 1)
    
    for k in range(1, mp):
        dz[k] = vgrid[k - 1] - vgrid[k]
    
    dz[mp] = 2.0 * vgrid[mp - 1]
    dz[0]  = 2.0 * (ps0 - vgrid[0])
    
    for k in range(1, mp + 1):
        dp = 0.5 * (dz[mp - k] + dz[mp + 1 - k])
        for m in range(0, nM):
            vsfint_temp[m, k] = vsfint_temp[m, k - 1] + vsf[m, mp - k] * dp
    
    vsf_int = vsfint_temp[:, 1:] #
    vmodes  = np.array([i for i in range(nM)])


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
