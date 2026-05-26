#-----------------------------------------------------------------------------
# IMPORTS
from qMODES import get_QMODES_TEST_PARAMETERS_FILE, get_QMODES_TEST_INPUT_DATA_DIR, get_QMODES_TEST_OUTPUT_DATA_DIR
from qMODES import compute_vsf_int, compute_qk, compute_qmodes
from qMODES import template_qk_with_klb_kub_ktot_fname, template_vsf_int_fname

import os
import yaml
import xarray as xa
import numpy as np
import pytest
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# CHECKING VSF_INT COMPUTATION
def test_computations_vsf_int():
    #----- Perform integration of vsf test data -----
    compute_vsf_int(get_QMODES_TEST_INPUT_DATA_DIR(), get_QMODES_TEST_PARAMETERS_FILE())

    #----- Test assertions -----
    # Check that the output file was created
    vsfint_testfile = template_vsf_int_fname(get_QMODES_TEST_INPUT_DATA_DIR())
    assert os.path.isfile(vsfint_testfile)

    # Check that integrated values are correct
    # Method for generating VSF test data:
    #    vsf(m=0, p) = 0 -> vsf_int(m=0, p) = 0
    #    vsf(m=1, p) = 1 -> vsf_int(m=1, p) = p
    #    vsf(m=2, p) = p -> vsf_int(m=2, p) = p^2 / 2

    vsfint_ds = xa.open_dataset(vsfint_testfile)
    vsf_int = vsfint_ds["vsf_int"].values
    plev = vsfint_ds["vgrid_int"].values
    vmodes = vsfint_ds.sizes["vmodes"]

    nplev = len(plev)
    nM = len(vmodes)

    assert vsf_int[0,:] == pytest.approx( np.zeros(nplev) )
    assert vsf_int[1,:] == pytest.approx( vgrid )
    assert vsf_int[2,:] == pytest.approx( vgrid ** 2 / 2.0 )


    return

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# CHECKING QK COMPUTATION (2 BATCHES)
def test_computations_qk():
    #----- Getting test parameters ------
    with open(get_QMODES_TEST_PARAMETERS_FILE(), 'r') as param_file:
        params = yaml.safe_load(param_file)
    
    test_nK  = params['mode_parameters']['nK']
    testdate = params['grid_parameters']['test_date']

    #----- parameter setup for 2 batches ------
    k_lb1 = 0
    k_ub1 = test_nK // 2 - 1
    k_lb2 = test_nK // 2 
    k_ub2 = test_nK - 1

    #----- qk_computations batch 1 -----
    compute_qk("EIG", testdate, k_lb1, k_ub1, test_nK, 
               input_data_dir=get_QMODES_TEST_INPUT_DATA_DIR(),
               output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
               parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
    compute_qk("WIG", testdate, k_lb1, k_ub1, test_nK, 
               input_data_dir=get_QMODES_TEST_INPUT_DATA_DIR(),
               output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
               parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
    compute_qk("BAL", testdate, k_lb1, k_ub1, test_nK, 
               input_data_dir=get_QMODES_TEST_INPUT_DATA_DIR(),
               output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
               parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
    
    #----- qk_computations batch 2 -----
    compute_qk("EIG", testdate, k_lb2, k_ub2, test_nK,
               input_data_dir=get_QMODES_TEST_INPUT_DATA_DIR(),
               output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
               parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
    compute_qk("WIG", testdate, k_lb2, k_ub2, test_nK,
               input_data_dir=get_QMODES_TEST_INPUT_DATA_DIR(),
               output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
               parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
    compute_qk("BAL", testdate, k_lb2, k_ub2, test_nK,
               input_data_dir=get_QMODES_TEST_INPUT_DATA_DIR(),
               output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
               parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
    
    #----- test assertions -----

    # Checking that output files from each of the 2 batches were created
    qk_testfile1 = template_qk_with_klb_kub_ktot_fname(get_QMODES_TEST_OUTPUT_DATA_DIR(), testdate, k_lb1, k_ub1, test_nK)
    qk_testfile2 = template_qk_with_klb_kub_ktot_fname(get_QMODES_TEST_OUTPUT_DATA_DIR(), testdate, k_lb2, k_ub2, test_nK)

    assert os.path.isfile(qk_testfile1)
    assert os.path.isfile(qk_testfile2)

    # Checking that the files have all of the modes (qk_EIG, qk_WIG, qk_BAL)
    qk_testds1 = xa.open_dataset(qk_testfile1)
    qk_testds2 = xa.open_dataset(qk_testfile2)

    assert set("qk_EIG", "qk_WIG", "qk_BAL") == set(qk_testds1.data_vars)
    assert set("qk_EIG", "qk_WIG", "qk_BAL") == set(qk_testds2.data_vars)

    return
#------------------------------------------------------------------------------



# #-----------------------------------------------------------------------------
# #TEST PARAMETER FILE IMPORTS
# 
# 
# 
# #-----------------------------------------------------------------------------
# 
# 
# 
# #-----------------------------------------------------------------------------
# # RUNNING qMDOES COMPUTATION AND AGGREGATION FUNCTIONS END TO END
# 
# # Parameters for running tests in parallel in 2 batches.
# 
# 
# 
# 
# #Running functions over test data end-to-end
# 
# # Running vsf_int computations
# 
# # Running qk computations over 2 batches
# 
# 
# # qk_computations batch 2
# compute_qk("EIG", "testdata", k_lb2, k_ub2, test_nK,
#            input_data_dir=get_QMODES_TEST_INPUT_DATA_DIR(),
#            output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
#            parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
# compute_qk("WIG", "testdata", k_lb2, k_ub2, test_nK,
#            input_data_dir=get_QMODES_TEST_INPUT_DATA_DIR(),
#            output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
#            parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
# compute_qk("BAL", "testdata", k_lb2, k_ub2, test_nK,
#            input_data_dir=get_QMODES_TEST_INPUT_DATA_DIR(),
#            output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
#            parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
# 
# # # aggreagte qk data 
# # combine_qk_files_from_list()
# # 
# # # Running qmodes computations using qk data
# # compute_qmodes("EIG", "testdata", k_lb1, k_ub1, test_nK) # "testdata" is a dummy variable
# # compute_qmodes("WIG", "testdata", k_lb1, k_ub1, test_nK) # "testdata" is a dummy variable
# # compute_qmodes("BAL", "testdata", k_lb1, k_ub1, test_nK) # "testdata" is a dummy variable
# # 
# # compute_qmodes("EIG", "testdata", k_lb2, k_ub2, test_nK) # "testdata" is a dummy variable
# # compute_qmodes("WIG", "testdata", k_lb2, k_ub2, test_nK) # "testdata" is a dummy variable
# # compute_qmodes("BAL", "testdata", k_lb2, k_ub2, test_nK) # "testdata" is a dummy variable
# # 
# # # Aggregating qmodes data
# # combine_qmodes_files_from_list()
# 
# #-----------------------------------------------------------------------------
# 
# 
# 
# #-----------------------------------------------------------------------------
# # FUNCTIONS TO CHECK OUTPUT OF RUNNING COMPUA
# 
# # def test_compute_qk():
# #     
# #     assert 1 == 1
# 
# #-----------------------------------------------------------------------------