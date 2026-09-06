#--------------------------------------------------------------------------
# IMPORTS

import os
#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
# FUNCTIONS THAT READ IN ENV VARS

def get_QMODES_REPO_DIR() -> str:
    """Returns the path to the qMODES repository base directory."""
    return os.getenv("QMODES_REPO_DIR")

def get_QMODES_SUPPRESS_NEW_USER_WARNINGS() -> bool:
    """Returns the value of the QMODES_SUPPRESS_NEW_USER_WARNINGS environment variable."""
    if os.getenv("QMODES_SUPPRESS_NEW_USER_WARNINGS") == "True":
        return True
    else:
        return False

# Old ENVVAR retrieval functions (deprecated, but left for comparison)
# # functions to retrieve directories
# def get_QMODES_INPUT_DATA_DIR() -> str:
#     return os.getenv("QMODES_INPUT_DATA_DIR")
# 
# def get_QMODES_OUTPUT_DATA_DIR() -> str:
#     return os.getenv("QMODES_OUTPUT_DATA_DIR")
# 
# def get_QMODES_TEST_INPUT_DATA_DIR() -> str:
#     return os.getenv("QMODES_TEST_INPUT_DATA_DIR")
# 
# def get_QMODES_TEST_OUTPUT_DATA_DIR() -> str:
#     return os.getenv("QMODES_TEST_OUTPUT_DATA_DIR")
# 
# # Functions to retrieve parameter files
# def get_QMODES_PARAMETERS_FILE() -> str:
#     return os.getenv("QMODES_PARAMETERS_FILE")
# 
# def get_QMODES_TEST_PARAMETERS_FILE() -> str:
#     return os.getenv("QMODES_TEST_PARAMETERS_FILE")
# 
# # Other ENV Vars
# def get_QMODES_SUPPRESS_NEW_USER_WARNINGS() -> bool:
#     if os.getenv("QMODES_SUPPRESS_NEW_USER_WARNINGS") == "True":
#         return True
#     else:
#         return False

#--------------------------------------------------------------------------