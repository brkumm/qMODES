#--------------------------------------------------------------------------
# File:          get_environment_variables.py
# Author:        Bradley Kumm (brkumm@gmail.com) 
# Last Modified: 2026/05/14 (YYYY/MM/DD)
# Description:   Script that retrieves the qMODES env vars.
#
# Notes:         To add later:
#					- 
#
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# IMPORTS

import os
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# FUNCTIONS THAT READ IN ENV VARS

# functions to retrieve directories
def get_QMODES_INPUT_DATA_DIR() -> str:
    return os.getenv("QMODES_INPUT_DATA_DIR")

def get_QMODES_OUTPUT_DATA_DIR() -> str:
    return os.getenv("QMODES_OUTPUT_DATA_DIR")

def get_QMODES_TEST_INPUT_DATA_DIR() -> str:
    return os.getenv("QMODES_TEST_INPUT_DATA_DIR")

def get_QMODES_TEST_OUTPUT_DATA_DIR() -> str:
    return os.getenv("QMODES_TEST_OUTPUT_DATA_DIR")

# Functinos to retrieve parameter files
def get_QMODES_PARAMETERS_FILE() -> str:
    return os.getenv("QMODES_PARAMETERS_FILE")

def get_QMODES_TEST_PARAMETERS_FILE() -> str:
    return os.getenv("QMODES_TEST_PARAMETERS_FILE")

# Other ENV Vars
def get_QMODES_SUPPRESS_NEW_USER_WARNINGS() -> bool:
    if os.getenv("QMODES_SUPPRESS_NEW_USER_WARNINGS") == "True":
        return True
    else:
        return False

#--------------------------------------------------------------------------
