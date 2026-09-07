#-----------------------------------------------------------------------------
# IMPORTS
from qMODES import get_QMODES_REPO_DIR, get_QMODES_SUPPRESS_NEW_USER_WARNINGS 

import os

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# PYTEST FUNCTIONS FOR UNIT TESTING

def test_get_QMODES_REPO_DIR():
    # Test that the function returns a non-empty string
    repo_dir = get_QMODES_REPO_DIR()
    assert isinstance(repo_dir, str)
    assert os.path.isdir(repo_dir)  # Check if the returned path is a directory

def test_get_QMODES_SUPPRESS_NEW_USER_WARNINGS():
    # Test that the function returns a boolean value
    suppress_warnings = get_QMODES_SUPPRESS_NEW_USER_WARNINGS()
    assert isinstance(suppress_warnings, bool)

#-----------------------------------------------------------------------------