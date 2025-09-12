#--------------------------------------------------------------------------
# File:          Calculate_Integrated_VSFs.py
# Author:        Bradley Kumm (bkumm@wisc.edu)
# Last Modified: 2023/11/28 (YYYY/MM/DD)
# Description:   Script that precomputes the integrated vertical structure
#                functions, as these don't change between runs.
#                These are calculated as:
#
#                         vsf_int(p;m) = int_0^p vsf(p';m) dp'
#
#                The integration is performed using an averaging of the 
#                left and right riemannan sums. Previously this was done
#                using simpsons method, but this is the method used by
#                Valentino and Nadjeljka so I will switch to using their
#                method for consistancy.
#
# Notes:         WARNING!!! The input file must be a netCDF files!!!
#
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
#IMPORTS

import numpy    as np
import xarray   as xa
from   datetime import datetime

#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
#USER INPUTS

# author info
author_name  = "USER's NAME"
author_email = "USER's EMAIL"

# VSF File
vsf_infile = "../../input_data/MODES_data/vsf/vsf.data.nc" #

# Output File
outfile  = "../../input_data/MODES_data/vsf_int/vsf_int.data.nc" #following Zagar Group naming convention
  
# --------------------------------------------------------------------------
  
  
# --------------------------------------------------------------------------
#  READING IN DATA FROM INPUT FILE(S)

vsf_ds = xa.open_dataset(vsf_infile)
vsf    = vsf_ds["vsf"].values
vgrid  = vsf_ds["vgrid"].values
mp     = len(vgrid)

#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
#INTEGRATING THE VSFs

ps0 = 101325 # Pressure at bottom of the atmosphere grid
num_vmode = 60   # Number of vertical modes (M)
vsfint_temp = np.zeros([num_vmode,mp+1]) #Allocation of matrix that will contain all integrals for all vertical modes

dz = np.zeros(mp+1)
for k in range(1,mp):
    dz[k] = vgrid[k - 1] - vgrid[k]

dz[mp] = 2.0 * vgrid[mp-1]
dz[0]  = 2.0 * (ps0-vgrid[0])

for k in range(1,mp+1):
    dp = 0.5 * (dz[mp - k] + dz[mp + 1 - k])
    print(f"dp = {dp}")
    for m in range(0,num_vmode):
        vsfint_temp[m,k] = vsfint_temp[m,k - 1] + vsf[m,mp - k] * dp

vsf_int = vsfint_temp[:,1:]      # Integrals of all VSFs that are later used to evaluate eq. 33
vmodes  = np.array([i for i in range(num_vmode)])
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# SAVING DATA TO OUTPUT FILE

#defining vgrid_int  to be the pressure coordinates that correspond with the integrated vsfs ...
#name change is useful help track the pressure level indexing (index 0 at top or bottom of atmosphere)

print(f"(vgird[0],vgrid[136]) before filp: ({vgrid[0]},{vgrid[136]})")
vgrid_int = vgrid[::-1]
print(f"(vgird_int[0],vgrid_int[136])  after filp: ({vgrid_int[0]},{vgrid_int[136]})")

out_units = "Pa"
dtnow     = datetime.now()

coords    = {'vgrid_int'  :  ( ['vgrid_int' ], vgrid_int  ),
             'vmodes'     :  ( ['vmodes'], vmodes )  }

data_vars = {'vsf_int':(['num_vmode', 'vgrid_int'], vsf_int,
                  { 'units': out_units,
                    'long_name':'integrated vertical structure function'}) }

attrs     = {'creation_date':dtnow.strftime("%m/%d/%Y, %H:%M:%S"),
             'author':author_name,
             'email' :author_email}

ds        = xa.Dataset(data_vars=data_vars,
                       coords=coords,
                       attrs=attrs)

ds.to_netcdf(outfile)
print(f"output file saved to:\n\t{outfile}")

#--------------------------------------------------------------------------

