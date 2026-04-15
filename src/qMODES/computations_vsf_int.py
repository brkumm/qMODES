#-----------------------------------------------------------------------------
# File:          computations_vsf_int.py
# Author:        Bradley Kumm (brkumm@gmail.com)
# Last Modified: 2026/04/15 (YYYY/MM/DD)
# Description:   Various functions used to compute the integrated Vertical
#                Structure Function (VSF) values from an input VSF data file.
#
# Notes:         
#               
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
# IMPORTS
from .read_environment_variables import get_QMODES_VSF_DIR, get_QMODES_VSFINT_DIR
from .parameters   import nM, ps0
from .templates    import template_vsf_fname, template_vsf_int_fname

import numpy    as np
import xarray   as xa
from   datetime import datetime
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#MAIN COMPUTATION OF INTEGRATED VERTICAL STRUCTURE FUNCTION 

def compute_vsf_int(out_dir=None, author_name=None, author_email=None):
    """
    Function that computes the integrated vertical structure function (VSF)
    values, which are computed as:

    vsf_int(p;m) = int_0^p vsf(p';m) dp'.

    The integration is performed using an averaging of the left and right 
    riemannan sums. Previously this was doneusing simpsons method, but this
    is the method used bythe Zagar group so I switched to their method for
    consistancy.

    REQUIRED INPUTS:
        

    OPTIONAL INPUTS:
        author_name: name of author (stored in outputfile metadata)
        author_email: email of author (stored in outputfile metadata)

    """

    #-------------------- Setting Computation Parameters ---------------------

    vsf_dir = get_QMODES_VSF_DIR()
    out_dir = get_QMODES_VSFINT_DIR()

    outfile = f"{out_dir}/{template_vsf_int_fname()}"

    vsf_infile = f"{vsf_dir}/{template_vsf_fname()}"
    vsf_ds     = xa.open_dataset(vsf_infile)
    vsf        = vsf_ds["vsf"].values
    vgrid      = vsf_ds["vgrid"].values
    mp         = len(vgrid)

    vsfint_temp = np.zeros([nM,mp+1]) #Allocation of matrix that will contain all integrals for all vertical modes

    #------------------------------- Main Loop -------------------------------

    dz = np.zeros(mp + 1)
    
    for k in range(1, mp):
        dz[k] = vgrid[k - 1] - vgrid[k]
    
    dz[mp] = 2.0 * vgrid[mp - 1]
    dz[0]  = 2.0 * (ps0 - vgrid[0])
    
    for k in range(1, mp + 1):
        dp = 0.5 * (dz[mp - k] + dz[mp + 1 - k])
        for m in range(0, nM):
            vsfint_temp[m, k] = vsfint_temp[m, k - 1] + vsf[m, mp - k] * dp
    
    vsf_int = vsfint_temp[:, 1:]      # Integrals of all VSFs that are later used to evaluate eq. 33
    vmodes  = np.array([i for i in range(nM)])


    #-------------------- Saving vsf_int Values to Outfile -------------------

    vgrid_int = vgrid[::-1] #ordering switches because integration is done from top of atmosphere to surface
    out_units = 'Pa'
    long_name = 'integrated vertical structure function'
    dtnow     = datetime.now()
    
    coords = { 'vgrid_int': (['vgrid_int' ], vgrid_int),
                  'vmodes'   : (['vmodes'], vmodes ) }
    

    data_vars = {'vsf_int':(['num_vmode', 'vgrid_int'], vsf_int,
                            {'units'    : out_units,
                             'long_name': long_name}) }
    
    attrs = {'creation_date':dtnow.strftime("%m/%d/%Y, %H:%M:%S")}
    if author_name != None: attrs['author name'] = author_name
    if author_email != None: attrs['author email'] = author_email
    
    ds = xa.Dataset(data_vars = data_vars,
                    coords = coords,
                    attrs = attrs)
    
    ds.to_netcdf(outfile)
    print(f"vsf_int computation sucessful!!\n\noutput data saved to:\n\t{outfile}")

    return

#-----------------------------------------------------------------------------
