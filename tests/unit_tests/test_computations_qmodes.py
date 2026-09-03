#-----------------------------------------------------------------------------
# IMPORTS 
from qMODES import get_QMODES_TEST_PARAMETERS_FILE, get_QMODES_TEST_INPUT_DATA_DIR, get_QMODES_TEST_OUTPUT_DATA_DIR
from qMODES import template_vsf_int_fname
from qMODES import compute_qmodes
from qMODES import template_qmodes_with_klb_kub_ktot_fname
from qMODES import convert_pos_int_to_padded_str

import os
import yaml
import xarray as xa
import pytest
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# CHECKING QMODES COMPUTATIONS (2 batches)

def test_compute_qmodes() -> None:
    #----- Retrieving test parameters ------
    with open(get_QMODES_TEST_PARAMETERS_FILE(), 'r') as param_file:
        params = yaml.safe_load(param_file)
    
    test_nK  = params['mode_parameters']['nK']
    testdate = params['grid_parameters']['test_date']

    #----- parameter setup for 2 batches ------
    modes = ["EIG", "WIG", "BAL"]
    q_modes = ["q_EIG", "q_WIG", "q_BAL"]
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
        #batch 1 computation
        compute_qmodes(imode, testdate, k_lb1, k_ub1, test_nK,
                       output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
                       parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )
        #batch 2 computation
        compute_qmodes(imode, testdate, k_lb1, k_ub1, test_nK,
                       output_data_dir=get_QMODES_TEST_OUTPUT_DATA_DIR(), 
                       parameter_file=get_QMODES_TEST_PARAMETERS_FILE() )

    #----- computations used for PyTest assertions -----
    qmodes_testfile1 = template_qmodes_with_klb_kub_ktot_fname(get_QMODES_TEST_OUTPUT_DATA_DIR(), testdate, k_lb1_str, k_ub1_str, test_nK_str)
    qmodes_testfile2 = template_qmodes_with_klb_kub_ktot_fname(get_QMODES_TEST_OUTPUT_DATA_DIR(), testdate, k_lb2_str, k_ub2_str, test_nK_str)

    qmodes_testds1 = xa.open_dataset(qmodes_testfile1)
    qmodes_testds2 = xa.open_dataset(qmodes_testfile2)

    #----- initial test assertions -----
    # Checking that output files from each of the 2 batches were created
    assert os.path.isfile(qmodes_testfile1)
    assert os.path.isfile(qmodes_testfile2)

    # Checking that the files have all of the modes (q_EIG, q_WIG, q_BAL)
    q_modes = ["q_EIG", "q_WIG", "q_BAL"]
    
    assert set(q_modes) == set(qmodes_testds1.data_vars)
    assert set(q_modes) == set(qmodes_testds2.data_vars)

    #----- Checking values by hand -----
    # The EIG, WIG, and BAL modes should take on the following values
    # based on the test coefficient choices.
    #
    # qk      Indexing (Re+Im, k_mode, vgrid_int, lat)
    # qmodes  Indexing (plev, lat, lon)
    # vsf_int Indexing (m, vgrid_int)
    #
    # qk_EIG[0,5,:,0] = 1.0 * vsf_int[m=1,:]
    # qk_WIG[0,4,:,0] = 1.0 * vsf_int[m=1,:]
    # qk_BAL[0,1,:,0] = 1.0 * vsf_int[m=1,:]
    # 
    # qk_EIG[0,9,:,0] = 0.1 * vsf_int[m=1,:] -> m=1 for vsf_int because these are the only coef vals turned on in sum
    # qk_WIG[0,8,:,0] = 0.1 * vsf_int[m=1,:] -> m=1 for vsf_int because these are the only coef vals turned on in sum
    # qk_BAL[0,2,:,0] = 0.1 * vsf_int[m=1,:] -> m=1 for vsf_int because these are the only coef vals turned on in sum
    #
    # qEIG = 2.0 * vsf_int[m=1,:] * ( 1.0 * np.cos(5.0 * np.radians(lon[ilon])) +  0.1 * np.cos(9.0 * np.radians(lon[ilon])) )
    # qWIG = 2.0 * vsf_int[m=1,:] * ( 1.0 * np.cos(4.0 * np.radians(lon[ilon])) +  0.1 * np.cos(8.0 * np.radians(lon[ilon])) )
    # qBAL = 2.0 * vsf_int[m=1,:] * ( 1.0 * np.cos(1.0 * np.radians(lon[ilon])) +  0.1 * np.cos(2.0 * np.radians(lon[ilon])) )

##    # nonzero qk values put in by hand based on test data 
##    # key:value -> "qk_mdoe" : List of tuples (k_mode, coef_amp)
##    qk_nonzeros = {"qk_EIG":[(5, 1.0), (9, 0.1)],
##                   "qk_WIG":[(4, 1.0), (8, 0.1)],
##                   "qk_BAL":[(1, 1.0), (2, 0.1)]}
##
##    # initializing loop vars
##    qmode_by_hand = 0 
##
##    # for each mode with nonzero qk vals
##    for qk_mode, tups in qk_nonzeros.items():
##
##        #reset qmode_by_hand for each mode
##        qmode_by_hand = 0 
##
##        #for each tuple of (k_mode, coef_amp) for the given qk_mode
##        for k_mode, coef_amp in tups:
##            
##            qmode_by_hand = 2.0 * coef_amp * vsf_int[1,:] * np.cos(float(k_mode) * np.radians(lon[ilon]))


#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# HELPER FUNCTIONS

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# Dev tests (Delete when finished)

test_compute_qmodes()

#-----------------------------------------------------------------------------