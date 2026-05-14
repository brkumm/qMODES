#--------------------------------------------------------------------------
# File:          read_environment_variables.py
# Author:        Bradley Kumm (brkumm@gmail.com) 
# Last Modified: 2026/01/14 (YYYY/MM/DD)
# Description:   Script for functions that return the environment variables
#                used by qMODES
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
import os
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# FUNCTIONS USED TO RETRIEVE ENVIRONMENT VARS

def get_QMODES_VSF_DIR():
    return os.getenv("QMODES_VSF_DIR")

def get_QMODES_VSFINT_DIR():
    return os.getenv("QMODES_VSFINT_DIR")

def get_QMODES_ERA_DIR():
	return os.getenv("QMODES_ERA_DIR")

def get_QMODES_MODES_DIR():
	return os.getenv("QMODES_MODES_DIR")

def get_QMODES_COEF_DIR():
	return os.getenv("QMODES_COEF_DIR")

def get_QMODES_HOUGH_DIR():
	return os.getenv("QMODES_HOUGH_DIR")

def get_QMODES_FREQ_DIR():
	return os.getenv("QMODES_FREQ_DIR")

def get_QMODES_QKDATA_DIR():
	return os.getenv("QMODES_QKDATA_DIR")

def get_QMODES_QMODESDATA_DIR():
	return os.getenv("QMODES_QMODESDATA_DIR")

def get_QMODES_PLOTS_DIR():
	return os.getenv("QMODES_PLOTS_DIR")

def get_QMODES_SUPPRESS_NEW_USER_WARNINGS():
    if os.getenv("QMODES_SUPPRESS_NEW_USER_WARNINGS") == "True":
        return True
    else:
        return False
#--------------------------------------------------------------------------
