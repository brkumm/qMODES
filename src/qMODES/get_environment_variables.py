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

def get_qMODES_INPUT_DATA_DIR():
    return os.getenv("QMODES_INPUT_DATA_DIR")

def get_qMODES_OUTPUT_DATA_DIR():
    return os.getenv("QMODES_OUTPUT_DATA_DIR")

def get_qMODES_TEST_INPUT_DATA_DIR():
    return os.getenv("QMODES_TEST_INPUT_DATA_DIR")

def get_qMODES_TEST_OUTPUT_DATA_DIR():
    return os.getenv("QMODES_TEST_OUTPUT_DATA_DIR")

# Misc ENV Vars

def get_QMODES_SUPPRESS_NEW_USER_WARNINGS():
    if os.getenv("QMODES_SUPPRESS_NEW_USER_WARNINGS") == "True":
        return True
    else:
        return False

#--------------------------------------------------------------------------