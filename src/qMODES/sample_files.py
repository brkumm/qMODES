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
from .read_environment_variables import *
from .templates import * 
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# SAMPLE DATA FILES, fill in manually may need to be changed depending on
# projects file structure

def sample_vsf_file():
	return f"{get_QMODES_VSF_DIR()}/{template_vsf_fname()}"

def sample_vsf_int_file():
	return f"{get_QMODES_VSFINT_DIR()}/{template_vsf_int_fname()}"

def sample_coef_file():
	return f"{get_QMODES_COEF_DIR()}/{template_coef_fname("20180801")}"

def sample_hough_file():
	return f"{get_QMODES_HOUGH_DIR()}/{template_hough_fname("000")}"

def sample_freq_file():
	return f"{get_QMODES_FREQ_DIR()}/{template_freq_fname("000")}"

def sample_ERA_file():
	return f"{get_QMODES_ERA_DIR()}/{template_ERA_fname("20180801")}"

#--------------------------------------------------------------------------
