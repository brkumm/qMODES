#-----------------------------------------------------------------------------
# IMPORTS
from qMODES import load_qmodes_config, get_QMODES_REPO_DIR

import os
import glob
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# PYTEST FUNCTIONS FOR UNIT TESTING
def test_load_qmodes_config():
    # Load the configuration from the YAML file
    config = load_qmodes_config(f"{get_QMODES_REPO_DIR()}/tests/config_test.yaml")

    # Check that the values from the test YAML file are correctly loaded into 
    # the qMODES_config_parameters instance. 
    # NOTE: Values to check agains are hard coded in below based on the values
    # in config file at the time of writing this pytest script.
    assert config.input_data_dir == "tests/test_data/test_input_data/"
    assert config.output_data_dir == "tests/test_data/test_output_data/"
    assert config.t_start == "20010101"
    assert config.delta_t == 1
    assert config.nT == 1
    assert config.nplev == 11
    assert config.nlat == 180
    assert config.nlon == 360
    assert config.nK == 10
    assert config.nM == 3
    assert config.nN == 5
    assert config.ps0 == 101325
    assert config.omega == 7.2722e-05

    # NOTE: The tests below will be run assuming that all of the test data has
    # been setup in the 'tests' directory. The 'tests/test_data_manager.py' 
    # can be easily used to generate data, and remove it after the tests are 
    # run.

    # Check that the input and output data directories of the test config file exist.
    assert os.path.exists( config.input_data_dir  )
    assert os.path.exists( config.output_data_dir )

    # Check that the get_default_data_dir method returns the correct paths for
    # each valid data_type input.
    assert os.path.exists( config.get_default_data_dir("ERA")     )
    assert os.path.exists( config.get_default_data_dir("coef")    )
    assert os.path.exists( config.get_default_data_dir("hough")   )
    assert os.path.exists( config.get_default_data_dir("freq")    )
    assert os.path.exists( config.get_default_data_dir("vsf")     )
    assert os.path.exists( config.get_default_data_dir("vsf_int") )
    assert os.path.exists( config.get_default_data_dir("qk")      )
    assert os.path.exists( config.get_default_data_dir("qmodes")  )

    # Check that the get_default_file_path method returns the correct paths
    # for each valid file_type input value.
    assert os.path.isfile( config.get_default_file_path("ERA_q_fname")   )
    assert os.path.isfile( config.get_default_file_path("ERA_uv_fname")  )
    assert os.path.isfile( config.get_default_file_path("coef_fname")    )
    assert os.path.isfile( config.get_default_file_path("vsf_fname")     )
    assert os.path.isfile( config.get_default_file_path("vsf_int_fname") )
    assert os.path.isfile( config.get_default_file_path("hough_fname")   )
    assert os.path.isfile( config.get_default_file_path("freq_fname")    )


#    # Check that the get_default_file_pattern method returns a correct 
#    # These checks should be ignored unless you have already performed the  
#    # qk and qmodes computations for the test input data. 
#    # For this reason these tests will be commented out by default.
#
#    assert os.path.isfile( config.get_default_file_path("qk_fname")      )
#    assert os.path.isfile( config.get_default_file_path("qmodes_fname")  )
#
#    # "not not list" is a quick method to check if a list is empty
#    assert not not glob.glob( config.get_default_file_pattern( "qk_file_pattern")     )
#    assert not not glob.glob( config.get_default_file_pattern( "qmodes_file_pattern") )

#-----------------------------------------------------------------------------