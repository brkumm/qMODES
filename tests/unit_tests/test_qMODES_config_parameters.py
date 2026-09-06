#-----------------------------------------------------------------------------
# IMPORTS
from qMODES import load_qmodes_config, get_QMODES_REPO_DIR

import os
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# PYTEST FUNCTIONS FOR UNIT TESTING
def test_load_qmodes_config():
    # Load the configuration from the YAML file
    config = load_qmodes_config(f"{get_QMODES_REPO_DIR()}/tests/config_test.yaml")

    # Check that the values from the test YAML file are correctly loaded into the qMODES_config_parameters instance
    assert config.nplev == 11
    assert config.nlat == 180
    assert config.nlon == 360
    assert config.nK == 10
    assert config.nM == 3
    assert config.nN == 5
    assert config.ps0 == 101325
    assert config.Omega == 7.2722e-05

    # Check that the input and output data directories of the test config file exist.
    assert os.path.exists(config.input_data_dir)
    assert os.path.exists(config.output_data_dir)

    # Check that the get_default_data_dir method returns the correct paths for each data type
    assert os.path.exists( config.get_default_data_dir("ERA"))
    assert os.path.exists( config.get_default_data_dir("coef"))
    assert os.path.exists( config.get_default_data_dir("hough"))
    assert os.path.exists( config.get_default_data_dir("freq"))
    assert os.path.exists( config.get_default_data_dir("vsf"))
    assert os.path.exists( config.get_default_data_dir("vsf_int"))
    assert os.path.exists( config.get_default_data_dir("qk"))
    assert os.path.exists( config.get_default_data_dir("qmodes"))
#-----------------------------------------------------------------------------