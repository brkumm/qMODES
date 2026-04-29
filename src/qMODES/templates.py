#--------------------------------------------------------------------------
# File:          templates.py
# Author:        Bradley Kumm (brkumm@gmail.com) 
# Last Modified: 2026/01/14 (YYYY/MM/DD)
# Description:   Script that defines templates, such as hough function 
#                filename conventions, used by the rest of the qMODES 
#                package.
#
# Notes:         To add later:
#					- 
#
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# FILE NAMING TEMPLATES

# k_str variables should be a string of length 3 (padd with zeros in front)
# date variables should be string with format 'YYYYMMDD'

# Input data file names
def template_vsf_fname():
	return "vsf.data.nc"

def template_vsf_int_fname():
	return "vsf_int.data.nc"

def template_hough_fname(k_str):
	return f"hough_F320_M60.wn00{k_str}.nc"

def template_coef_fname(date):
	return f"Hough_coeff_M60_F320_{date}0000000.nc"

def template_freq_fname(k_str):
	return f"freq_F320_M60.data.wn00{k_str}"

#Output Data filenames and patterns
def template_qk_fname(date):
	return f"qk_{date}0000000.nc"

def template_qk_with_klb_kub_ktot_fname(date, klb_str, kub_str, ktot_str):
	return f"qk_{date}0000000_klb-{klb_str}_kub-{kub_str}_ktot-{ktot_str}.nc"

def template_combine_qk_file_pattern(date, ktot_str):
    return f"qk_{date}0000000_klb-*_kub-*_ktot-{ktot_str}.nc"

def template_qmodes_fname(date):
	return f"qmodes_{date}0000000.nc"

def template_qmodes_with_klb_kub_ktot_fname(date, klb_str, kub_str, ktot_str):
	return f"qmodes_{date}0000000_klb-{klb_str}_kub-{kub_str}_ktot-{ktot_str}.nc"

def template_combine_qmodes_file_pattern(date, ktot_str):
    return f"qmodes_{date}0000000_klb-*_kub-*_ktot-{ktot_str}.nc"

def template_ERA_fname(date):
	return f"ERA5_{date}_q-t_pl_data.nc"

def template_ERA_uv_fname(date):
	return f"ERA5_{date}_u-v_pl_data.nc"

# Test data filenames
def template_testdata_vsf_fname():
	return "testdata_vsf.nc"

def template_testdata_hough_fname(k_str):
	return f"testdata_hough_{k_str}.nc"

def template_testdata_coef_fname():
	return "testdata_coef.nc"

def template_testdata_vsf_int_fname():
	return "testdata_vsf_int.nc"

def template_testdata_qk_fname():
	return "testdata_qk.nc"

def template_testdata_qmodes_fname():
	return "testdata_qmodes.nc"

#--------------------------------------------------------------------------
