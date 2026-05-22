#--------------------------------------------------------------------------
# File:          templates.py
# Author:        Bradley Kumm (brkumm@gmail.com) 
# Last Modified: 2026/05/14 (YYYY/MM/DD)
# Description:   Script that defines templates, such as hough function 
#                filename conventions, used by the rest of the qMODES 
#                package.
#
# Notes:         To add later:
#					- 
#
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# DIRECTORY STRUCTURE TEMPLATES

# NOTES:
# - Directory input vars for these functions should should be obtained using
#   the functions in get_environment_variables module which retrieve the
#   input, output, test_input, and test_output directories specified by the 
#   qMODES environment variables

# Input Data Directories
def get_QMODES_ERA_DIR(env_var_input_data_dir: str) -> str:
	return f"{env_var_input_data_dir}/ERA_data"

def get_QMODES_MODES_DIR(env_var_input_data_dir: str) -> str:
	return f"{env_var_input_data_dir}/MODES_data"

def get_QMODES_VSF_DIR(env_var_input_data_dir: str) -> str:
    return f"{env_var_input_data_dir}/MODES_data/vsf"

def get_QMODES_VSFINT_DIR(env_var_input_data_dir: str) -> str:
    return f"{env_var_input_data_dir}/MODES_data/vsf"

def get_QMODES_COEF_DIR(env_var_input_data_dir: str) -> str:
	return f"{env_var_input_data_dir}/MODES_data/coef"

def get_QMODES_HOUGH_DIR(env_var_input_data_dir: str) -> str:
	return f"{env_var_input_data_dir}/MODES_data/hough"

def get_QMODES_FREQ_DIR(env_var_input_data_dir: str) -> str:
	return f"{env_var_input_data_dir}/MODES_data/hough"


# Output Data Directories
def get_QMODES_QKDATA_DIR(env_var_output_data_dir: str) -> str:
	return f"{env_var_output_data_dir}/qk_data"

def get_QMODES_QMODESDATA_DIR(env_var_output_data_dir: str) -> str:
	return f"{env_var_output_data_dir}/qmodes_data"

def get_QMODES_PLOTS_DIR(env_var_output_data_dir: str) -> str:
	return f"{env_var_output_data_dir}/plots"
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# FILE NAMING TEMPLATES

# NOTES:
# - Directory input vars for these functions should should be obtained using
#   the functions in get_environment_variables module which retrieve the
#   input, output, test_input, and test_output directories.
# - The 'k_str', 'klb_str', 'kub_str', and 'ktot_str' input variable should be 
#   strings of three numbers. Add leading 0's if need be.
# - The 'date' input variable should be a string in YYYYMMDD format.


# Input data filenames
def template_ERA_q_fname(env_var_input_data_dir: str, date: str) -> str:
	return f"{get_QMODES_ERA_DIR(env_var_input_data_dir)}/ERA5_{date}_q-t_pl_data.nc"

def template_ERA_uv_fname(env_var_input_data_dir: str, date:str) -> str:
	return f"{get_QMODES_ERA_DIR(env_var_input_data_dir)}/ERA5_{date}_u-v_pl_data.nc"

def template_vsf_fname(env_var_input_data_dir: str) -> str:
	return f"{get_QMODES_VSF_DIR(env_var_input_data_dir)}/vsf.data.nc"

def template_vsf_int_fname(env_var_input_data_dir: str) -> str:
	return f"{get_QMODES_VSFINT_DIR(env_var_input_data_dir)}/vsf_int.data.nc"

def template_hough_fname(env_var_input_data_dir: str, k_str: str) -> str:
	return f"{get_QMODES_HOUGH_DIR(env_var_input_data_dir)}/hough_F320_M60.wn00{k_str}.nc"

def template_coef_fname(env_var_input_data_dir: str, date: str) -> str:
	return f"{get_QMODES_COEF_DIR(env_var_input_data_dir)}/Hough_coeff_M60_F320_{date}0000000.nc"

def template_freq_fname(env_var_input_data_dir: str, k_str: str) -> str:
	return f"{get_QMODES_FREQ_DIR(env_var_input_data_dir)}/freq_F320_{k_str}0000000.nc"


# Output data filenames
def template_qk_fname(env_var_output_data_dir: str, date: str) -> str:
	return f"{get_QMODES_QKDATA_DIR(env_var_output_data_dir)}/qk_{date}0000000.nc"

def template_qk_with_klb_kub_ktot_fname(env_var_output_data_dir: str, date: str, klb_str: str, kub_str: str, ktot_str: str) -> str:
	return f"{get_QMODES_QKDATA_DIR(env_var_output_data_dir)}/qk_{date}0000000_klb-{klb_str}_kub-{kub_str}_ktot-{ktot_str}.nc"

def template_qmodes_fname(env_var_output_data_dir: str, date: str) -> str:
	return f"{get_QMODES_QMODESDATA_DIR(env_var_output_data_dir)}/qmodes_{date}0000000.nc"

def template_qmodes_with_klb_kub_ktot_fname(env_var_output_data_dir: str, date: str, klb_str: str, kub_str: str, ktot_str: str) -> str:
	return f"{get_QMODES_QMODESDATA_DIR(env_var_output_data_dir)}/qmodes_{date}0000000_klb-{klb_str}_kub-{kub_str}_ktot-{ktot_str}.nc"


# File patterns (used by scripts to combine files computed in parallel)
def template_combine_qk_file_pattern(env_var_output_data_dir: str, date: str, ktot_str: str) -> str:
    return f"{get_QMODES_QKDATA_DIR(env_var_output_data_dir)}/qk_{date}0000000_klb-*_kub-*_ktot-{ktot_str}.nc"

def template_combine_qmodes_file_pattern(env_var_output_data_dir: str, date: str, ktot_str: str) -> str:
    return f"{get_QMODES_QMODESDATA_DIR(env_var_output_data_dir)}/qmodes_{date}0000000_klb-*_kub-*_ktot-{ktot_str}.nc"
#--------------------------------------------------------------------------
