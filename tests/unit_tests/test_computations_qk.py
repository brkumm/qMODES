#-----------------------------------------------------------------------------
# IMPORTS 
from qMODES import get_QMODES_TEST_PARAMETERS_FILE, get_QMODES_TEST_INPUT_DATA_DIR, get_QMODES_TEST_OUTPUT_DATA_DIR
from qMODES import template_vsf_int_fname
from qMODES import compute_qk
from qMODES import template_qk_with_klb_kub_ktot_fname
from qMODES import convert_pos_int_to_padded_str

import os
import yaml
import xarray as xa
import pytest
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# CHECKING QK COMPUTATION (2 BATCHES)
def test_compute_qk() -> None:
    #----- Retrieving test parameters ------
    with open(get_QMODES_TEST_PARAMETERS_FILE(), 'r') as param_file:
        params = yaml.safe_load(param_file)
    
    test_nK  = params['mode_parameters']['nK']
    testdate = params['grid_parameters']['test_date']

    #----- parameter setup for 2 batches ------
    modes = ["EIG", "WIG", "BAL"]
    k_lb1 = 0
    k_ub1 = test_nK // 2 - 1
    k_lb2 = test_nK // 2 
    k_ub2 = test_nK - 1

    k_lb1_str   = convert_pos_int_to_padded_str(k_lb1)
    k_ub1_str   = convert_pos_int_to_padded_str(k_ub1)
    k_lb2_str   = convert_pos_int_to_padded_str(k_lb2)
    k_ub2_str   = convert_pos_int_to_padded_str(k_ub2)
    test_nK_str = convert_pos_int_to_padded_str(test_nK)

    #----- qk computations -----

    for imode in modes:
        # batch 1 computation
        print(f"(imode, testdate, k_lb1, k_ub1, test_nK) = ({imode}, {testdate}, {k_lb1}, {k_ub1}, {test_nK})")
        compute_qk(imode, testdate, k_lb1, k_ub1, test_nK, 
                   input_data_dir=get_QMODES_TEST_INPUT_DATA_DIR(),
                   output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
                   parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
        # batch 2 computation
        compute_qk(imode, testdate, k_lb2, k_ub2, test_nK,
                   input_data_dir=get_QMODES_TEST_INPUT_DATA_DIR(),
                   output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
                   parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
    
    
    #----- computations used for PyTest assertions -----
    qk_testfile1 = template_qk_with_klb_kub_ktot_fname(get_QMODES_TEST_OUTPUT_DATA_DIR(), testdate, k_lb1_str, k_ub1_str, test_nK_str)
    qk_testfile2 = template_qk_with_klb_kub_ktot_fname(get_QMODES_TEST_OUTPUT_DATA_DIR(), testdate, k_lb2_str, k_ub2_str, test_nK_str)

    qk_testds1 = xa.open_dataset(qk_testfile1)
    qk_testds2 = xa.open_dataset(qk_testfile2)

    # qk indexing (REIM, kval, inplev, inlat)
    # EIG -> k = 5 & 9 turned on w/ coef amp of 1 & 0.1 
    # WIG -> k = 4 & 8 turned on w/ coef amp of 1 & 0.1 
    # BAL -> k = 1 & 2 turned on w/ coef amp of 1 & 0.1
    
    #----- test assertions -----
    # Checking that output files from each of the 2 batches were created
    assert os.path.isfile(qk_testfile1)
    assert os.path.isfile(qk_testfile2)

    # Checking that the files have all of the modes (qk_EIG, qk_WIG, qk_BAL)
    qk_modes = ["qk_EIG", "qk_WIG", "qk_BAL"]
    
    assert set(qk_modes) == set(qk_testds1.data_vars)
    assert set(qk_modes) == set(qk_testds2.data_vars)

    #----- Checking values by hand -----
    # The EIG, WIG, and BAL modes should take on the following values
    # based on the test coefficient choices.
    #
    # qk Indexing (Re+Im, k_mode, vgrid_int, lat)
    #
    # qk_EIG[0,5,:,0] = 1.0 * vsf_int[m=1,:]
    # qk_WIG[0,4,:,0] = 1.0 * vsf_int[m=1,:]
    # qk_BAL[0,1,:,0] = 1.0 * vsf_int[m=1,:]
    # 
    # qk_WIG[0,8,:,0] = 0.1 * vsf_int[m=1,:] -> m=1 for vsf_int because these are the only coef vals turned on in sum
    # qk_BAL[0,2,:,0] = 0.1 * vsf_int[m=1,:] -> m=1 for vsf_int because these are the only coef vals turned on in sum
    # qk_EIG[0,9,:,0] = 0.1 * vsf_int[m=1,:] -> m=1 for vsf_int because these are the only coef vals turned on in sum

    # retrieving the vsf_int values
    vsf_int_file = template_vsf_int_fname(get_QMODES_TEST_INPUT_DATA_DIR())
    vsf_int_ds = xa.open_dataset(vsf_int_file)
    vsf_int = vsf_int_ds["vsf_int"].values

    # nonzero qk values computed by hand based on test data
    # key:value -> "qk_mdoe" : List of tups (k_mode, coef_amp)
    qk_nonzeros = {"qk_EIG":[(5, 1.0), (9, 0.1)],
                   "qk_WIG":[(4, 1.0), (8, 0.1)],
                   "qk_BAL":[(1, 1.0), (2, 0.1)]}
    
    batches = [(0,4), (5,9)]
    
    # for each mode with nonzero qk vals
    for qk_mode, tups in qk_nonzeros.items():

        # for each kval, amp combo of that mode
        for (kval, amp) in tups:
            # retrieve filename and index in that file for each kval
            (qk_filename, file_index) = _get_qkfile_and_index_from_kval_and_batch_list(kval, batches, testdate, test_nK_str)

            # retrieve nonzero qk data:
            dummy_ds = xa.open_dataset(qk_filename)
            qk_mode_vals = dummy_ds[qk_mode].values

            # check that the values match
            assert (qk_mode_vals[0,file_index, :, 0] == amp * vsf_int[1,:]).all()
        
    return
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# HELPER FUNCTIONS

def _get_qkfile_and_index_from_kval_and_batch_list(kval: int, batches: list[tuple[int,int]], testdate: str, ktot_str: str) -> tuple[str, int]:
    # This function is used to avoid needing to use the "combine_qk.py" functions
    # to keep the scope of the test smaller
    #
    # Inputs:
    #   kval -> the kval  you would like to find the file and file index for
    #   batches -> list of tuples containing the lower and upper bound,
    #              inclusive, for each qk file.
    # Outputs:
    #

    for tup in batches:
        if kval >= tup[0] and kval <= tup[1]:
            klb_str = convert_pos_int_to_padded_str(tup[0])
            kub_str = convert_pos_int_to_padded_str(tup[1])
            output_file = template_qk_with_klb_kub_ktot_fname(get_QMODES_TEST_OUTPUT_DATA_DIR(), testdate, klb_str, kub_str, ktot_str)
            output_index = kval - tup[0]
            return (output_file, output_index)

#-----------------------------------------------------------------------------