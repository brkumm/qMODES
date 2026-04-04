#--------------------------------------------------------------------------
# File:          parameters.py
# Author:        Bradley Kumm (brkumm@gmail.com) 
# Last Modified: 2026/01/14 (YYYY/MM/DD)
# Description:   Script that defines parameters, such as number of vertical
#                modes, used by the rest of the qMODES package.
#
# Notes:         To add later:
#					- functions that pull constants from setup file instead
#                     from this file. This could be useful if you want to 
#                     simultaneously have multiple qMODES projects going 
#                     at once with different parameters. Would recommend  
#                     designing so each "project" has its own directory 
#                     and in the base of that directory there will be a 
#                     JSON file specifying the constants for that project.
#
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# STANDARD NUMERIC AND GRID PARAMETERS

# Fourier Space Parameters 
nK = 351 #number of K modes
nM = 60  #number of M modes
nN = 200 #number of N modes

# Atmospheric Grid Parameters
nplev = 137  # number of pressure levels on the grid
nlat  = 640  # number of latitude values on the grid
nlon  = 1280 # number of longitude values on the grid

# Physical Constants
ps0 = 101325 # Pressure at bottom of the atmospheric grid
Omega = 7.2722e-05 # Rotation rate of earth in rad / sec

#--------------------------------------------------------------------------
