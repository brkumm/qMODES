#-----------------------------------------------------------------------------
# IMPORTS
from qMODES import get_QMODES_PARAMETERS_FILE, get_QMODES_INPUT_DATA_DIR, get_QMODES_OUTPUT_DATA_DIR
from qMODES import get_QMODES_TEST_PARAMETERS_FILE, get_QMODES_TEST_INPUT_DATA_DIR, get_QMODES_TEST_OUTPUT_DATA_DIR

import pytest
import yaml
import os
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# CHECKING THAT ALL OF THE QMODES ENVIRONMENT VARS ARE DECLARED.
def test_check_all_env_vars_exist() -> None:
    
    required_vars = ["QMODES_PARAMETERS_FILE", 
                     "QMODES_INPUT_DATA_DIR",
                     "QMODES_OUTPUT_DATA_DIR",
                     "QMODES_TEST_PARAMETERS_FILE",
                     "QMODES_TEST_INPUT_DATA_DIR",
                     "QMODES_TEST_OUTPUT_DATA_DIR"]
    
    for var in required_vars:
        assert var in os.environ, f"{var} is not declared env var. Make sure to define QMODES env vars."

    return
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# CHECKING REGULAR RUN ENV VARS

def test_get_QMODES_PARAMETERS_FILE() -> None:
    # Check that the file exists
    assert os.path.isfile(get_QMODES_PARAMETERS_FILE())

    # Check that the file has the necessary variables stored in it
    with open(get_QMODES_PARAMETERS_FILE(), 'r') as param_file:
        params = yaml.safe_load(param_file)
    
        parameter_vars_dict = { "grid_parameters":[("nplev", int),
                                                   ("nlat", int),
                                                   ("nlon", int)],
                                "mode_parameters":[("nK", int),
                                                   ("nM", int),
                                                   ("nN", int)],
                                "physical_constants":[("ps0", int, float),
                                                      ("Omega", int, float)],
                                "sample_files":[("grid_file", str)] }
        
        for key, var_list in parameter_vars_dict.items():
            for tup in var_list:
                assert  type(params[key][tup[0]]) in tup[1:]

    return

def test_get_QMODES_INPUT_DATA_DIR() -> None:
    # Check that the directory exists
    assert os.path.isdir(get_QMODES_INPUT_DATA_DIR())

    # Check that the directory has the correct structure
    assert os.path.isdir(f"{get_QMODES_INPUT_DATA_DIR()}/ERA_data")
    assert os.path.isdir(f"{get_QMODES_INPUT_DATA_DIR()}/MODES_data")
    assert os.path.isdir(f"{get_QMODES_INPUT_DATA_DIR()}/MODES_data/coef")
    assert os.path.isdir(f"{get_QMODES_INPUT_DATA_DIR()}/MODES_data/hough")
    assert os.path.isdir(f"{get_QMODES_INPUT_DATA_DIR()}/MODES_data/vsf")

    return

def test_get_QMODES_OUTPUT_DATA_DIR() -> None:
    # Check that the directory exists
    assert os.path.isdir(get_QMODES_OUTPUT_DATA_DIR())

    # Check that the directory has the correct structure
    assert os.path.isdir(f"{get_QMODES_OUTPUT_DATA_DIR()}/plots")
    assert os.path.isdir(f"{get_QMODES_OUTPUT_DATA_DIR()}/qk_data")
    assert os.path.isdir(f"{get_QMODES_OUTPUT_DATA_DIR()}/qmodes_data")

    return
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
#CHECKING TEST RUN ENV VARS

def test_get_QMODES_TEST_PARAMETERS_FILE() -> None:
    # Check that the file exists
    assert os.path.isfile(get_QMODES_TEST_PARAMETERS_FILE())

    # Check that the file has the necessary variables stored in it
    with open(get_QMODES_TEST_PARAMETERS_FILE(), 'r') as param_file:
        params = yaml.safe_load(param_file)
    
        parameter_vars_dict = { "grid_parameters":[("nplev", int),
                                                   ("nlat", int),
                                                   ("nlon", int), 
                                                   ("test_plev", list),
                                                   ("test_date", int, str)],
                                "mode_parameters":[("nK", int),
                                                   ("nM", int),
                                                   ("nN", int)],
                                "physical_constants":[("ps0", int, float),
                                                      ("Omega", int, float)],
                                "sample_files":[("grid_file", str)] }
        
        for key,var_list in parameter_vars_dict.items():
            for tup in var_list:
                print(tup)
                print(type(params[key][tup[0]]))
                assert  type(params[key][tup[0]]) in tup[1:]

    return

def test_get_QMODES_TEST_INPUT_DATA_DIR() -> None:
    # Check that the directory exists
    assert os.path.isdir(get_QMODES_TEST_INPUT_DATA_DIR())

    # Check that the directory has the correct structure
    assert os.path.isdir(f"{get_QMODES_TEST_INPUT_DATA_DIR()}/ERA_data")
    assert os.path.isdir(f"{get_QMODES_TEST_INPUT_DATA_DIR()}/MODES_data")
    assert os.path.isdir(f"{get_QMODES_TEST_INPUT_DATA_DIR()}/MODES_data/coef")
    assert os.path.isdir(f"{get_QMODES_TEST_INPUT_DATA_DIR()}/MODES_data/hough")
    assert os.path.isdir(f"{get_QMODES_TEST_INPUT_DATA_DIR()}/MODES_data/vsf")

    return

def test_get_QMODES_TEST_OUTPUT_DATA_DIR() -> None:
    # Check that the directory exists
    assert os.path.isdir(get_QMODES_TEST_OUTPUT_DATA_DIR())

    # Check that the directory has the correct structure
    assert os.path.isdir(f"{get_QMODES_TEST_OUTPUT_DATA_DIR()}/plots")
    assert os.path.isdir(f"{get_QMODES_TEST_OUTPUT_DATA_DIR()}/qk_data")
    assert os.path.isdir(f"{get_QMODES_TEST_OUTPUT_DATA_DIR()}/qmodes_data")

    return
#-----------------------------------------------------------------------------