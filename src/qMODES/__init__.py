from .get_environment_variables import * 
from .templates                 import *

from .computations_vsf_int import *
from .computations_qk import *


# from .get_environment_variables import get_qMODES_INPUT_DATA_DIR, get_qMODES_OUTPUT_DATA_DIR, get_qMODES_TEST_INPUT_DATA_DIR, get_qMODES_TEST_OUTPUT_DATA_DIR
# from .sample_files import sample_vsf_file, sample_vsf_int_file, sample_coef_file, sample_hough_file, sample_freq_file, sample_ERA_file
# from .parameters import nK, nM, nN, nplev, nlat, nlon, ps0, Omega
# #from .templates import *
# from .math_util import qMODES_deriv, qMODES_deriv_at_point
# 
# from .computations_vsf_int import compute_vsf_int
# from .computations_qk import compute_qk
# from .computations_qmodes import compute_qmodes
# 
# from .combine_qk import get_klb_kub_ktot_from_qk_filename, get_qk_files_with_date_and_ktot, check_qk_files_cover_ktot_range, check_qk_files_have_all_modes, combine_qk_files_from_list
# from .combine_qmodes import get_klb_kub_ktot_from_qmodes_filename, get_qmodes_files_with_date_and_ktot, check_qmodes_files_cover_ktot_range, check_qmodes_files_have_all_modes, combine_qmodes_files_from_list
# from .data_readers import get_full_field_ERA_and_flipped_qmodes_data, get_full_field_ERA_and_flipped_qmodes_data_with_p_and_lat_dependent_background, get_single_plev_ERA_and_flipped_qmodes_data, get_single_plev_ERA_and_flipped_qmodes_data_with_p_and_lat_dependent_background, read_ERA_grid_data

# #-----------------------------------------------------------------------------
# # CUSTOM FUNCTIONS FOR qMODES IMPORTS
# def _check_sample_file_functions(input_list):
#     
#     import os
# 
#     has_thrown_warning = False
#     
#     for sample_func in input_list:
#     
#         #Print warning if file doesn't exist
#         if not os.path.isfile(sample_func()):
# 
#             #line to print upon finding first missing sample file
#             if has_thrown_warning == False:
#                 has_thrown_warning = True
#                 print(f"\nWARNING: The following qMODES \'sample_file\' functions don't produce a file that exists.")
# 
#             # Printing the bad sample function name
#             print(f"\t{sample_func.__name__}")
# 
#     if has_thrown_warning:
#         print("You should check:")
#         print("\t1) That the all required environment variables are setup (see README.md).")
#         print("\t2) The environmen variable readers are setup correctly (read_environment_varialbes.py).")
#         print("\t3) Check that the sample filenames are correct (sample_files.py).\n")
#         print("NOTE: This may also happen if you have not yet downloaded the required data or perfromed")
#         print("the preliminary calculations (VSF function integration).")
#     return
# 
# def _print_bkg_function_warning():
#     """
#     Function that warns the user about qmodes and qk functions not 
#     accounting for the background function in the computation, and 
#     instructs them on where they can see an example on how to properly 
#     account for it.
#     """
# 
#     print("\nIMPORTANT NOTE FOR USING qMODES!!!"                                                  )
#     print("\tThe factor of the background moisture derivative is left out of " )
#     print("\tthe qk and qmodes computations to have extra flexibility in how"  )
#     print("\tto account for this term, latitude dependent vs indepent bkg "    )
#     print("\tetc... This factor needs to be accounted for before you will "    )
#     print("\tobtain correct moisture anomoly values. I recommend using the "   )
#     print("\tqMODES package data reader functions or at least looking at them" )
#     print("\tto see how this is done.\n"                                        )
# 
#     return
# 
# def _check_read_environment_variables_functions(input_function_list):
# 
#     import os
# 
#     has_thrown_warning = False
# 
#     for func in input_function_list:
# 
#         if func() == None:
#             if has_thrown_warning == False:
#                 has_thrown_warning = True
#                 print(f"\nWARNING: The following qMODES \'read_environment_variables\' functions return None.")
# 
#             print(f"\t{func.__name__}")
# 
#     if has_thrown_warning: print("Make sure to set all environment variables.\nSee README.md file for which environment variables need to be set.\n")
#     
#     return
# 
# #-----------------------------------------------------------------------------
# 
# 
# 
# #-----------------------------------------------------------------------------
# # MAIN: CHECKS TO RUN UPON IMPORTING FROM qMODES
# 
# # initializing variables for checks
# 
# read_evn_var_input_list = [get_QMODES_ERA_DIR, get_QMODES_MODES_DIR, 
#                            get_QMODES_COEF_DIR, get_QMODES_VSF_DIR, 
#                            get_QMODES_VSFINT_DIR, get_QMODES_COEF_DIR, 
#                            get_QMODES_QKDATA_DIR, get_QMODES_QMODESDATA_DIR, 
#                            get_QMODES_PLOTS_DIR ]
# 
# 
# sample_file_input_list = [ sample_vsf_file, sample_vsf_int_file, 
#                            sample_coef_file, sample_hough_file, 
#                            sample_freq_file, sample_ERA_file     ]
# 
# 
# # Check that ENV vars are not None (better check later)
# _check_read_environment_variables_functions(read_evn_var_input_list)
# 
# # Check if sample files exist and send warning for each one that doesn't
# _check_sample_file_functions(sample_file_input_list)
# 
# # Print important warnings
# if get_QMODES_SUPPRESS_NEW_USER_WARNINGS == False: _print_bkg_function_warning()
# 
# #-----------------------------------------------------------------------------
# 
