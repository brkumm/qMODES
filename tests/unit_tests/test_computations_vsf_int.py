#-----------------------------------------------------------------------------
# IMPORTS
from qMODES import get_QMODES_TEST_PARAMETERS_FILE, get_QMODES_TEST_INPUT_DATA_DIR, get_QMODES_TEST_OUTPUT_DATA_DIR
from qMODES import compute_vsf_int
from qMODES import template_vsf_int_fname, template_vsf_fname

import os
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