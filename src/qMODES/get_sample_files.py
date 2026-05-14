#--------------------------------------------------------------------------
# File:          sample_files.py
# Author:        Bradley Kumm (brkumm@gmail.com) 
# Last Modified: 2026/01/14 (YYYY/MM/DD)
# Description:   Script that defines the location of files to be used as 
#                sample files that contain general data that you may want
#                to pull into your script, such as grid data, etc...
#
# Notes:         - Some of these may or may not be useful. Might come back to
#                  delete unuseful ones from the package.
#                - Keeping these as simple as possible... if these files 
#                  don't exist it should throw an error when trying to open
#                  them so it should be straight forward to track down if 
#                  these need to be changed. Maybe add something to the 
#                  __init__.py to check if these files exist and add a 
#                  warning if they don't.
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# IMPORTS
from .get_environment_variables import *
from .templates import *
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# SAMPLE DATA FILES, fill in manually may need to be changed depending on
# projects file structure

def sample_vsf_file():
	return get_QMODES_VSF_DIR() + "/vsf.data.nc"

def sample_vsf_int_file():
	return get_QMODES_VSFINT_DIR() + "/vsf_int.data.nc"

def sample_coef_file():
	return get_QMODES_COEF_DIR() + "/Hough_coeff_M60_F320_201808010000000.nc"

def sample_hough_file():
	return get_QMODES_HOUGH_DIR() + "/hough_F320_M60.wn00000.nc"

def sample_freq_file():
	return get_QMODES_FREQ_DIR() + "/freq_F320_M60.data.wn00000"

def sample_ERA_file():
	return get_QMODES_ERA_DIR() + "/ERA5_20180801_q-t_pl_data.nc"

#--------------------------------------------------------------------------