#-----------------------------------------------------------------------------
# IMPORTS
from qMODES import get_QMODES_TEST_PARAMETERS_FILE, get_QMODES_TEST_INPUT_DATA_DIR, get_QMODES_TEST_OUTPUT_DATA_DIR
from qMODES import compute_vsf_int, compute_qk, compute_qmodes
from qMODES import template_vsf_int_fname, template_vsf_fname
from qMODES import template_qk_with_klb_kub_ktot_fname
from qMODES import template_qmodes_with_klb_kub_ktot_fname

import os
import yaml
import xarray as xa
import numpy as np
import pytest
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# CHECKING VSF_INT COMPUTATION
def test_computations_vsf_int() -> None:
    #----- Check that vsf test data file exists -----
    if not os.path.isfile(template_vsf_fname(get_QMODES_TEST_INPUT_DATA_DIR())):
        print("ERROR: vsf test data file doesn't exist!!!")
        print("use the script .../tests/test_data_manager.py")
        print("to create the necessary data for running the automated tests.")

    #----- Perform integration of vsf test data -----
    compute_vsf_int(get_QMODES_TEST_INPUT_DATA_DIR(), get_QMODES_TEST_PARAMETERS_FILE())

    #----- Tests -----
    # Check that the output file was created
    vsfint_testfile = template_vsf_int_fname(get_QMODES_TEST_INPUT_DATA_DIR())
    assert os.path.isfile(vsfint_testfile)

    # Check that integrated values are correct
    # Method for generating VSF test data:
    #    vsf(m=0, p) = 0 -> vsf_int(m=0, p) = 0
    #    vsf(m=1, p) = 1 -> vsf_int(m=1, p) = p
    #    vsf(m=2, p) = p -> vsf_int(m=2, p) = p^2 / 2

    # Reading in vsf_int values to compare to hand calculated values
    vsfint_ds = xa.open_dataset(vsfint_testfile)
    vsf_int = vsfint_ds["vsf_int"].values

    # Answers calculated by hand that correspond to values test values created
    # by the script /tests/test_data_manager.py and current method for
    # computing the integrated vsf values (from Zagar group)
    # if those values are ever changed these hand calculated values will have
    # be recalculated by hand as well!!!
    answers_by_hand = np.array([ [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
                                  0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                                  [3.00000000e+00, 7.50000000e+00, 3.00000000e+01, 7.50000000e+01,
                                   3.00000000e+02, 7.50000000e+02, 3.00000000e+03, 7.50000000e+03,
                                   3.00000000e+04, 7.50000000e+04, 1.01325000e+05],
                                  [3.00000000e+00, 2.55000000e+01, 2.50500000e+02, 2.50050000e+03,
                                   2.50005000e+04, 2.50000500e+05, 2.50000050e+06, 2.50000005e+07,
                                   2.50000000e+08, 2.50000000e+09, 5.13250000e+09] ])

    assert vsf_int[0,:] == pytest.approx( answers_by_hand[0,:] )
    assert vsf_int[1,:] == pytest.approx( answers_by_hand[1,:] )
    assert vsf_int[2,:] == pytest.approx( answers_by_hand[2,:] )

    return
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# CHECKING QK COMPUTATION (2 BATCHES)
def test_computations_qk() -> None:
    #----- Retrieving test parameters ------
    with open(get_QMODES_TEST_PARAMETERS_FILE(), 'r') as param_file:
        params = yaml.safe_load(param_file)
    
    test_nK  = params['mode_parameters']['nK']
    testdate = params['grid_parameters']['test_date']

    #----- parameter setup for 2 batches ------
    k_lb1 = 0
    k_ub1 = test_nK // 2 - 1
    k_lb2 = test_nK // 2 
    k_ub2 = test_nK - 1

    k_lb1_str   = "0"*(3-len(str(k_lb1)))   + str(k_lb1) 
    k_ub1_str   = "0"*(3-len(str(k_ub1)))   + str(k_ub1) 
    k_lb2_str   = "0"*(3-len(str(k_lb2)))   + str(k_lb2) 
    k_ub2_str   = "0"*(3-len(str(k_ub2)))   + str(k_ub2) 
    test_nK_str = "0"*(3-len(str(test_nK))) + str(test_nK)

    #----- qk computations batch 1 -----
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
    
    #----- qk computations batch 2 -----
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
    
    #----- computations used by test assertions -----
    qk_testfile1 = template_qk_with_klb_kub_ktot_fname(get_QMODES_TEST_OUTPUT_DATA_DIR(), testdate, k_lb1_str, k_ub1_str, test_nK_str)
    qk_testfile2 = template_qk_with_klb_kub_ktot_fname(get_QMODES_TEST_OUTPUT_DATA_DIR(), testdate, k_lb2_str, k_ub2_str, test_nK_str)

    qk_testds1 = xa.open_dataset(qk_testfile1)
    qk_testds2 = xa.open_dataset(qk_testfile2)

    # qk indexing (REIM, kval, inplev, inlat)
    qk_EIG_nonzeros = {} # k = 5 & 9 turned on w/ coef amp of 1 & 0.1 
    qk_WIG_nonzeros = {} # k = 4 & 8 turned on w/ coef amp of 1 & 0.1 
    qk_BAL_nonzeros = {} # k = 1 & 2 turned on w/ coef amp of 1 & 0.1 
    
    #----- test assertions -----
    # Checking that output files from each of the 2 batches were created
    assert os.path.isfile(qk_testfile1)
    assert os.path.isfile(qk_testfile2)

    # Checking that the files have all of the modes (qk_EIG, qk_WIG, qk_BAL)
    assert set(["qk_EIG", "qk_WIG", "qk_BAL"]) == set(qk_testds1.data_vars)
    assert set(["qk_EIG", "qk_WIG", "qk_BAL"]) == set(qk_testds2.data_vars)

    #----- Checking values by hand -----

    return
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
# Checking qmodes computations
def test_computations_qmodes() -> None:
    #----- Retrieving test parameters ------
    with open(get_QMODES_TEST_PARAMETERS_FILE(), 'r') as param_file:
        params = yaml.safe_load(param_file)
    
    test_nK  = params['mode_parameters']['nK']
    testdate = params['grid_parameters']['test_date']

    #----- Parameter setup for 2 batches -----
    k_lb1 = 0
    k_ub1 = test_nK // 2 - 1
    k_lb2 = test_nK // 2 
    k_ub2 = test_nK - 1

    k_lb1_str   = "0"*(3-len(str(k_lb1)))   + str(k_lb1) 
    k_ub1_str   = "0"*(3-len(str(k_ub1)))   + str(k_ub1) 
    k_lb2_str   = "0"*(3-len(str(k_lb2)))   + str(k_lb2) 
    k_ub2_str   = "0"*(3-len(str(k_ub2)))   + str(k_ub2) 
    test_nK_str = "0"*(3-len(str(test_nK))) + str(test_nK)

    #----- Computing qmodes batch 1 -----
    compute_qmodes("EIG", testdate, k_lb1, k_ub1, test_nK,
                   output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
                   parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
    compute_qmodes("WIG", testdate, k_lb1, k_ub1, test_nK,
                   output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
                   parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
    compute_qmodes("BAL", testdate, k_lb1, k_ub1, test_nK,
                   output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
                   parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )

    #----- Computing qmodes batch 2 -----
    compute_qmodes("EIG", testdate, k_lb2, k_ub2, test_nK,
                   output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
                   parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
    compute_qmodes("WIG", testdate, k_lb2, k_ub2, test_nK,
                   output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
                   parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
    compute_qmodes("BAL", testdate, k_lb2, k_ub2, test_nK,
                   output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
                   parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
    
    #----- computations used by test assertions -----
    qmodes_testfile1 = template_qmodes_with_klb_kub_ktot_fname(get_QMODES_TEST_OUTPUT_DATA_DIR(), testdate, k_lb1_str, k_ub1_str, test_nK_str)
    qmodes_testfile2 = template_qmodes_with_klb_kub_ktot_fname(get_QMODES_TEST_OUTPUT_DATA_DIR(), testdate, k_lb2_str, k_ub2_str, test_nK_str)

    qmodes_testds1 = xa.open_dataset(qmodes_testfile1)
    qmodes_testds2 = xa.open_dataset(qmodes_testfile2)

    # qk indexing (REIM, kval, inplev, inlat)
    qk_EIG_nonzeros = {} # k = 5 & 9 turned on w/ coef amp of 1 & 0.1 
    qk_WIG_nonzeros = {} # k = 4 & 8 turned on w/ coef amp of 1 & 0.1 
    qk_BAL_nonzeros = {} # k = 1 & 2 turned on w/ coef amp of 1 & 0.1 

    #----- test assertions -----
    # Checking that output files from each of the 2 batches were created
    assert os.path.isfile(qmodes_testfile1)
    assert os.path.isfile(qmodes_testfile2)

    # Checking that the files have all of the modes (qk_EIG, qk_WIG, qk_BAL)
    assert set(["q_EIG", "q_WIG", "q_BAL"]) == set(qmodes_testds1.data_vars)
    assert set(["q_EIG", "q_WIG", "q_BAL"]) == set(qmodes_testds2.data_vars)

    #----- Checking values by hand -----

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