#------------------------------------------------------------------------------
# IMPORTS
from qMODES import compute_qk, compute_qmodes, compute_vsf_int
from qMODES import combine_qk_files_from_list
from qMODES import combine_qmodes_files_from_list
from qMODES import parameters as params

import pytest
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
# RUNNING qMDOES COMPUTATION AND AGGREGATION FUNCTIONS END TO END

# Parameters for running tests
k_lb1 = 0
k_ub1 = params.test_nK // 2

k_lb2 = params.test_nK // 2 + 1
k_ub2 = params.test_nK

ktot  = params.test_nK 


#Running functions over test data end-to-end

# Running vsf_int computations

# Running qk computations
compute_qk("EIG", "testdata", k_lb1, k_ub1, ktot) # "testdata" is a dummy variable
compute_qk("WIG", "testdata", k_lb1, k_ub1, ktot) # "testdata" is a dummy variable
compute_qk("BAL", "testdata", k_lb1, k_ub1, ktot) # "testdata" is a dummy variable

compute_qk("EIG", "testdata", k_lb2, k_ub2, ktot) # "testdata" is a dummy variable
compute_qk("WIG", "testdata", k_lb2, k_ub2, ktot) # "testdata" is a dummy variable
compute_qk("BAL", "testdata", k_lb2, k_ub2, ktot) # "testdata" is a dummy variable

# # aggreagte qk data 
# combine_qk_files_from_list()
# 
# # Running qmodes computations using qk data
# compute_qmodes("EIG", "testdata", k_lb1, k_ub1, ktot) # "testdata" is a dummy variable
# compute_qmodes("WIG", "testdata", k_lb1, k_ub1, ktot) # "testdata" is a dummy variable
# compute_qmodes("BAL", "testdata", k_lb1, k_ub1, ktot) # "testdata" is a dummy variable
# 
# compute_qmodes("EIG", "testdata", k_lb2, k_ub2, ktot) # "testdata" is a dummy variable
# compute_qmodes("WIG", "testdata", k_lb2, k_ub2, ktot) # "testdata" is a dummy variable
# compute_qmodes("BAL", "testdata", k_lb2, k_ub2, ktot) # "testdata" is a dummy variable
# 
# # Aggregating qmodes data
# combine_qmodes_files_from_list()

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
# FUNCTIONS TO CHECK OUTPUT OF RUNNING COMPUA

# def test_compute_qk():
#     
#     assert 1 == 1

#------------------------------------------------------------------------------